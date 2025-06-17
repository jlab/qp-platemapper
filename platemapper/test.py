import ordinationbuild
import os
import pandas as pd # pyright: ignore[reportMissingModuleSource]
import filecmp
#import sys




# remove hard paths
base_dir = "tests/data"
file_name = "meta_plate.tsv"
output_dir = "tests/ordinationtest"
test_dir = "tests/testordinations"
os.makedirs(output_dir, exist_ok=True)

endplate = None




for folder in os.listdir(base_dir):
    folder_path = os.path.join(base_dir, folder)
    
    if os.path.isdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        # file_dir = os.path.dirname(file_path)
        # folder_name
        dataframe = pd.read_csv(file_path, sep="\t")
        filterplates = ordinationbuild.filter_cols(dataframe)
        
        for i in range(len(filterplates)):
            # get single plate as variable out of dictionary
            df4 = ordinationbuild.conv_dict(filterplates, i)
            #edit plate: well split, well convert
            samplesnotfinal = ordinationbuild.ordinationBuild(df4, i)

            #for multiple plates: offset plate by 14 columns
            samplesnotfinal["row"] += i*13

            combined = samplesnotfinal

            if endplate is None:
                endplate = combined.copy()
            else:
                endplate = pd.concat([endplate, combined], ignore_index=True)
        samples = ordinationbuild.finalDataframeBuild(endplate)
        ordinationbuild.ordinationWrite(samples, folder, output_dir)
        endplate = None
    print(f"{folder}: Ordination loaded.")

for filename in os.listdir(test_dir):
    path1 = os.path.join(output_dir, filename)
    path2 = os.path.join(test_dir, filename)

    if filecmp.cmp(path1, path2, shallow=False):
        print(f"{filename}:Dateien sind identisch")
    else:
        print(f"{filename}: Error")