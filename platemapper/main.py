from platemapper import filehandler
from platemapper import ordinationbuild
from platemapper import qiimebuild
import pandas as pd

import shutil
#  import os
# execute everything

# make folderstructure

import qiime2
import qiime2.plugins.emperor.actions as emperor_actions

filehandler.makefolder()





def platemapper_execute(df:pd.DataFrame, fp_output:str, colname_plate_id="plate_id", colname_well_id='well_id'):
    """
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame holding information about technical metadata of samples. One row = one sample. Must contain columns '' and ''.
    fp_output : str
        The filepath of the resulting Qiime2 qzv artifact.
    """

    # create empty variable, important later on
    endplate = None

    filtered_plates = ordinationbuild.filter_cols(df)

    # uhhhh suddenly the vars dont work when in function
    #  file_dir = os.path.dirname(filepath)
    #  folder_name = os.path.basename(file_dir)

    for i in range(len(filtered_plates)):
        # get single plate as variable out of dictionary
        df4 = ordinationbuild.conv_dict(filtered_plates, i)
        # edit plate: well split, well convert
        samplesnotfinal = ordinationbuild.ordinationBuild(df4, i)

        # for multiple plates: offset plate by 14 columns
        samplesnotfinal["row"] += i*13

        combined = samplesnotfinal

        # same song here. This one contains sample name and
        # row/column  e.g 3 8, 7 4 etc...
        if endplate is None:
            endplate = combined.copy()
        else:
            endplate = pd.concat([endplate, combined], ignore_index=True)

    # taking combined plates and spacers
    samples = ordinationbuild.finalDataframeBuild(endplate)
    # write ordination with skbio
    ordination = ordinationbuild.ordinationCreate(samples)

    # convert the ordination into a Qiime2 artifact
    q2_pcoa = qiime2.Artifact.import_data('PCoAResults', ordination)
    # convert the metadata dataframe into a Qiime2 object
    q2_meta = qiime2.Metadata(df)

    # use "plot" of emperor to create the q2 emperor plot
    q2_emp = emperor_actions.plot(pcoa=q2_pcoa, metadata=q2_meta)

    q2_emp.visualization.save(fp_output)

    # ordinationbuild.ordinationWrite(ordination,
    #                                 foldername=None,
    #                                 outputpath=qiimebuild.OUTPUT_ORDIN)
    #
    # # build qza and qzv plot
    # qiimebuild.qzabuildsingle(foldername=None)
    # qiimebuild.empbuildsingle(foldername=None)
    #
    # filehandler.clearfolder()


if __name__ == "__main__":
    platemapper_execute()
"""
im still getting this futurewarning: FutureWarning:
Setting an item of incompatible dtype is deprecated
and will raise an error in a future version of pandas.
Value '[nan nan nan nan nan nan nan nan nan
nan nan nan nan nan nan nan nan nan
nan nan nan nan nan nan nan nan nan
nan nan nan nan nan nan]' has dtype incompatible
with float64, please explicitly cast to a
compatible dtype first.
series[missing.index] = missing

maybe i will eventually find the fix to it, not very high
on the priorities list rn
"""

# for push
