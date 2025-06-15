from qiime2 import Artifact, Metadata # pyright: ignore[reportMissingImports]
from qiime2.plugins.emperor.visualizers import plot # pyright: ignore[reportMissingImports]
import glob
import ordinationbuild


# file paths for saving and loading files
output_qza = "output/artifact_results"
output_qzv = "output/emp_results"
output_ordin = "output/ordination_files"






def qzabuildsingle(foldername):
    ordination = Artifact.import_data(
        "PCoAResults",
        f"./{output_ordin}/ordination_{foldername}_.txt",
        view_type="OrdinationFormat"
    )
      #save .qza file
    ordination.save(f"./{output_qza}/ordination_{foldername}_.qza")
# build the .qza files, needed for building emperor files
def qzabuild():

    #count: important for counting up ordaintion names, e.g ordination1.qza ordination2.qza ...
    count = 1
    # = numbers of dataframes in the dictionary = number of plates
    for key, df in ordinationbuild.filtered_plates.items():
        # build .qza file
        ordination = Artifact.import_data(
            "PCoAResults",
            f"./{output_ordin}/ordination{key}.txt",
            view_type="OrdinationFormat"
        )
        
        #save .qza file
        ordination.save(f"./{output_qza}/ordination{count}.qza")
        #NOW count one up 
        count += 1
        


def empbuildsingle(foldername):
    #load .qza
    empbuild = Artifact.load(f"./{output_qza}/ordination_{foldername}_.qza")
    #load metadata file
    metadata = Metadata.load("meta_plate.tsv")
    # choose pcoa, important
    vis = plot(pcoa = empbuild, metadata = metadata, ignore_missing_samples=True)
    #save .qzv file
    vis.visualization.save(f"./{output_qzv}/emp_plot_{foldername}_.qzv")
    
#build .qzv file for visual output via emperor
def empbuild():
    # listing all ordination.txt files, that way it does know how many .qzv files to produce
    filelist = glob.glob(f"{output_ordin}/ordination*.txt")# for qza, could change it to the .qza directory
    anzahl =range(1, len(filelist)+1)
    
     
    for i in anzahl:
        #load .qza
        empbuild = Artifact.load(f"./{output_qza}/ordination{i}.qza")
        #load metadata file
        metadata = Metadata.load("meta_plate.tsv")

        # choose pcoa, important
        vis = plot(pcoa = empbuild, metadata = metadata, ignore_missing_samples=True)
        #save .qzv file
        vis.visualization.save(f"./{output_qzv}/emp_plot{i}.qzv")
    # no idea why
    return anzahl

# also, maybe if its okay, delete all files except for the .qzv files because .qza and ordination no longer needed.
# Introducing the ability to save emperor plots as .png, no need to always import them to view.qiime2. thats more complex then i thought
