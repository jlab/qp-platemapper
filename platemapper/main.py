from platemapper import filehandler
import ordinationbuild
import qiimebuild
import pandas as pd  # pyright: ignore[reportMissingModuleSource]
# -----------------------------
import tkinter
from tkinter import filedialog
# -----------------------------
import shutil
import os
# execute everything

# make folderstructure

filehandler.makefolder()


# create empty variable, important later on
endplate = None


def load_file():
    """
    Selecting a metafile (e.g. meta_plate.tsv). Right now
    this happens via tkinter, but this will be erased soon
    as quita doesnt need this. No idea as how it will have
    to be implemented

    Raises:
        KeyError:   If no File Path exists, there will be no
                    file chosen by user. User has to choose
                    a File.

    Returns:
        df (pd.DataFrame):  metafile as pd.DataFrame for
                            further manipulation

        file_path (str; path):  filepath for copying the metafile
                                into the correct position and
                                for extracting the Foldername.
    """
    window = tkinter.Tk()
    window.minsize(1000, 1000)
    window.withdraw()    # tkinter.Tk().withdraw()
    file_path = filedialog.askopenfilename(parent=window,
                                           filetypes=[("TSV files", "*.tsv")],
                                           title="choose file:")  # choose file

    window.destroy()

    datafr = pd.read_csv(file_path, sep='\t')
    # opy metafile to current directory, really important for emperor later on
    shutil.copyfile(file_path, "./meta_plate.tsv")

    if not file_path:
        raise KeyError("Incorrect folder or filetype.")

    # need: after file is chosen, clean output folder
    return datafr, file_path


df, filepath = load_file()
filtered_plates = ordinationbuild.filter_cols(df)


file_dir = os.path.dirname(filepath)
folder_name = os.path.basename(file_dir)


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
ordinationbuild.ordinationWrite(ordination,
                                foldername=None,
                                outputpath=qiimebuild.OUTPUT_ORDIN)


# build qza and qzv plot
qiimebuild.qzabuildsingle(foldername=None)
qiimebuild.empbuildsingle(foldername=None)

filehandler.clearfolder()


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
