from qiime2 import Artifact, Metadata
from qiime2.plugins.emperor.visualizers import plot
import glob
import os
import time

output_qza = "output/artifact_results"
output_qzv = "output/emp_results"
output_ordin = "output/ordination_files"
os.makedirs(output_qza, exist_ok=True)
os.makedirs(output_qzv, exist_ok=True)


filelist = glob.glob(f"{output_ordin}/ordination*.txt")# for qza

anzahl =range(1, len(filelist)+1)

for i in anzahl:
    ordination = Artifact.import_data(
        "PCoAResults",
        f"./{output_ordin}/ordinationdf_plate{i}.txt", #has to be made dynamic, only works for current test
        view_type="OrdinationFormat"
    )
    ordination.save(f"./{output_qza}/ordination{i}.qza")
    
# filecount = glob.glob(f"{output_qza}/*.qza")
# count = range(1, len(filecount+1))

   
for i in anzahl:
    empbuild = Artifact.load(f"./{output_qza}/ordination{i}.qza")
    metadata = Metadata.load("meta_plate.tsv")

    vis = plot(pcoa = empbuild, metadata = metadata, ignore_missing_samples=True)
    vis.visualization.save(f"./{output_qzv}/emp_plot{i}.qzv")
