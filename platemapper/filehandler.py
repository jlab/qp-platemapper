import os
import shutil

# filepaths: global variables
OUTPUT_QZA = "output/artifact_results"
OUTPUT_QZV = "output/emp_results"
OUTPUT_ORDIN = "output/ordination_files"

# create directories, exist_ok=True so it wont cry if the
# directories already exist


def makefolder():
    os.makedirs(OUTPUT_QZA, exist_ok=True)
    os.makedirs(OUTPUT_QZV, exist_ok=True)
    os.makedirs(OUTPUT_ORDIN, exist_ok=True)


def clearfolder():
    shutil.rmtree(OUTPUT_QZA)
    shutil.rmtree(OUTPUT_QZV)
