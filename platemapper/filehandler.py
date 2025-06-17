import os
import shutil

#filepaths
output_qza = "output/artifact_results"
output_qzv = "output/emp_results"
output_ordin = "output/ordination_files"



#create directories, exist_ok=True so it wont cry if the directories already exist
def makefolder():
    os.makedirs(output_qza, exist_ok=True)
    os.makedirs(output_qzv, exist_ok=True)
    os.makedirs(output_ordin, exist_ok=True)
    
def clearfolder():
   shutil.rmtree(output_qza)
   shutil.rmtree(output_qzv)
