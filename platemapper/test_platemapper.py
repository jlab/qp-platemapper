from skbio.stats.ordination import OrdinationResults # pyright: ignore[reportMissingImports]
import ordinationbuild
import pandas as pd # pyright: ignore[reportMissingModuleSource]
import numpy as np
import glob
import os




def ordination_no_file(path):
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


def test_foo(): 
    exp = OrdinationResults.read("tests/data/Kurth_JIA/ordination_Kurth_JIA.txt")
    obs = ordination_no_file(path="tests/data/Kurth_JIA/meta_plate.tsv")
    
    
    print(glob.glob("/tests/data/**/*.tsv", recursive=True))
    print("exp_sample")
    print(exp.samples.values[:8])
    print("obs_samples")
    print(obs.samples.values[:8])
    
    assert np.allclose(exp.samples.values, obs.samples.values)
    


def test_all():
    for path in glob.glob("tests/data/**/meta_plate.tsv"):
        parentFolder = os.path.basename(os.path.dirname(path))
        exp = OrdinationResults.read(f"tests/data/{parentFolder}/ordination_{parentFolder}.txt")
        obs = ordination_no_file(path)
        print(glob.glob("/tests/data/**/*.tsv", recursive=True))
        print("exp_sample")
        print(exp.samples.values[:8])
        print("obs_samples")
        print(obs.samples.values[:8])
        assert np.allclose(exp.samples.values, obs.samples.values)