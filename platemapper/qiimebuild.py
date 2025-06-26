from qiime2 import Artifact, Metadata  # pyright: ignore[reportMissingImports]
from qiime2.plugins.emperor.visualizers import plot
import glob
import ordinationbuild


# file paths for saving and loading files
OUTPUT_QZA = "output/artifact_results"
OUTPUT_QZV = "output/emp_results"
OUTPUT_ORDIN = "output/ordination_files"


def qzabuildsingle(foldername):
    filename = f"ordination{foldername}.txt" if foldername else "ordination"
    ordination = Artifact.import_data(
        "PCoAResults",
        f"./{OUTPUT_ORDIN}/{filename}.txt",
        view_type="OrdinationFormat"
    )
    # save .qza file
    ordination.save(f"./{OUTPUT_QZA}/{filename}.qza")

# build the .qza files, needed for building emperor files
# LEGACY: superceded by qzabuildsingle as
# there is no need to output multiple .qza files anymore


def qzabuild():

    # count: important for counting up ordaintion
    # names, e.g ordination1.qza ordination2.qza ...
    count = 1
    # = numbers of dataframes in the dictionary = number of plates
    for key, df in ordinationbuild.filtered_plates.items():
        # build .qza file
        ordination = Artifact.import_data(
            "PCoAResults",
            f"./{OUTPUT_ORDIN}/ordination{key}.txt",
            view_type="OrdinationFormat"
        )

        # save .qza file
        ordination.save(f"./{OUTPUT_QZA}/ordination{count}.qza")
        # NOW count one up
        count += 1


def empbuildsingle(foldername):
    filename = f"ordination{foldername}" if foldername else "ordination"
    # load .qza
    empbuild = Artifact.load(f"./{OUTPUT_QZA}/{filename}.qza")
    # load metadata file
    metadata = Metadata.load("meta_plate.tsv")
    # choose pcoa, important
    vis = plot(pcoa=empbuild,
               metadata=metadata,
               ignore_missing_samples=True)
    # save .qzv file
    vis.visualization.save(f"./{OUTPUT_QZV}/emp_plot.qzv")

# build .qzv file for visual output via emperor
# LEGACY: superceded by empbuildsingle as
# there is no need to output multiple .qzv files anymore


def empbuild():
    # listing all ordination.txt files, that way
    # it does know how many .qzv files to produce
    filelist = glob.glob(f"{OUTPUT_ORDIN}/ordination*.txt")
    anzahl = range(1, len(filelist)+1)

    for i in anzahl:
        # load .qza
        empbuild = Artifact.load(f"./{OUTPUT_QZA}/ordination{i}.qza")
        # load metadata file
        metadata = Metadata.load("meta_plate.tsv")

        # choose pcoa, important
        vis = plot(pcoa=empbuild,
                   metadata=metadata,
                   ignore_missing_samples=True)
        # save .qzv file
        vis.visualization.save(f"./{OUTPUT_QZV}/emp_plot{i}.qzv")
    # no idea why
    return anzahl

# also, maybe if its okay, delete all files except for the
# .qzv files because .qza and ordination no longer needed.
