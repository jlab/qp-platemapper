from qiime2 import Artifact, Metadata
from qiime2.plugins.emperor.visualizers import plot
import glob
import ordinationbuild


output_qza = "output/artifact_results"
output_qzv = "output/emp_results"
output_ordin = "output/ordination_files"

def qzabuild():


    
    
    count = 1
    for key, df in ordinationbuild.filtered_plates.items():
        #count = 1
        ordination = Artifact.import_data(
            "PCoAResults",
            f"./{output_ordin}/ordination{key}.txt", #has to be made dynamic, only works for current test, would love to get the dictionary keys there 
            view_type="OrdinationFormat"
        )
        
        # for i in str(count):
        ordination.save(f"./{output_qza}/ordination{count}.qza")
        count += 1
        # doesnt want to jump to 

    # filecount = glob.glob(f"{output_qza}/*.qza")
    # count = range(1, len(filecount+1))

def empbuild():
    filelist = glob.glob(f"{output_ordin}/ordination*.txt")# for qza
    anzahl =range(1, len(filelist)+1)
    
     
    for i in anzahl:
        empbuild = Artifact.load(f"./{output_qza}/ordination{i}.qza")
        metadata = Metadata.load("meta_plate.tsv")

        vis = plot(pcoa = empbuild, metadata = metadata, ignore_missing_samples=True)
        vis.visualization.save(f"./{output_qzv}/emp_plot{i}.qzv")
    
    return anzahl


qzabuild()
empbuild()  
"""

    """