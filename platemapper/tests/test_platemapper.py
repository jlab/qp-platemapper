from skbio.stats.ordination import OrdinationResults # pyright: ignore[reportMissingImports]
from platemapper import ordinationbuild

import pandas as pd # pyright: ignore[reportMissingModuleSource]
#import numpy as np
import glob
import os




def ordination_no_file(path):
    """_summary_

    Args:
        path (_type_): _description_

    Returns:
        _type_: _description_
    """
    endplate = None
    df = pd.read_csv(path, sep="\t")
    filtered_plates = ordinationbuild.filter_cols(df)

    for i in range(len(filtered_plates)):
        df4 = ordinationbuild.conv_dict(filtered_plates, i)
        samplesnotfinal = ordinationbuild.ordinationBuild(df4, i)
        samplesnotfinal["row"] += i*13
        combined = samplesnotfinal

        if endplate is None:
            endplate = combined.copy()
        else:
            endplate = pd.concat([endplate, combined], ignore_index=True)

    samples = ordinationbuild.finalDataframeBuild(endplate)
    ordination = ordinationbuild.ordinationCreate(samples)

    return ordination

def check_compatability(path):

    df = pd.read_csv(path, sep="\t")
    if "well_id" not in df.columns:
        raise KeyError("No Column named well_id. Please rename fitting Column to well_id")
    if "plate_id" not in df.columns:
        raise KeyError("Column plate_id not found. Please rename fitting Column to plate_id")


def test_foo():
    exp = OrdinationResults.read("platemapper/tests/data/Kurth_JIA/ordination_Kurth_JIA.txt")
    obs = ordination_no_file(path="platemapper/tests/data/Kurth_JIA/meta_plate.tsv")
    print("Expected Ordination")
    print(exp)
    print("Observed ordination")
    print(obs)
    # print(glob.glob("/tests/data/**/*.tsv", recursive=True))
    # print("exp_sample_testfoo")
    # print(exp.samples.values[:8])
    # print("obs_samples_testfoo")
    # print(obs.samples.values[:8])

    #assert np.allclose(exp.samples.values, obs.samples.values)
    assert str(exp) == str(obs)



def test_all():
    for path in glob.glob("platemapper/tests/data/**/meta_plate.tsv"):
        parentFolder = os.path.basename(os.path.dirname(path))
        exp = OrdinationResults.read(f"platemapper/tests/data/{parentFolder}/ordination_{parentFolder}.txt")
        obs = ordination_no_file(path)

        # print(f"exp_sample:{parentFolder}")
        # print(exp.samples.values[:10])
        # print(f"obs_samples:{parentFolder}")
        # print(obs.samples.values[:10])
        #assert np.allclose(exp.samples.values, obs.samples.values)
        assert str(exp) == str(obs)
