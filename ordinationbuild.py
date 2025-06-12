import pandas as pd # pyright: ignore[reportMissingModuleSource]
#import numpy as np
from skbio.stats.ordination import OrdinationResults # pyright: ignore[reportMissingImports]
#import tkinter
#from tkinter import filedialog
#import shutil # for copying metafile to main folder
#import os



"""
Use tkinter to choose a file conveniently from a file Explorer,
then insert into a dataframe(datafr). Will get scrapped.
"""
# # will be changed for other workflow
# def load_file():
#     window = tkinter.Tk()
#     window.minsize(1000, 1000)
#     window.withdraw()    #tkinter.Tk().withdraw()
#     file_path = filedialog.askopenfilename(parent= window, 
#                                            filetypes=[("TSV files", "*.tsv")],
#                                            title= "choose file:")# choose file
    
#     window.destroy()
    
#     datafr = pd.read_csv(file_path, sep='\t')
#     shutil.copyfile(file_path, "./meta_plate.tsv")# copy metafile to current directory, really important for emperor later on
    
#     if not file_path:
#         raise KeyError("Incorrect folder or filetype, or maybe no file selected?")
    
#     # need: after file is chosen, clean output folder
#     return datafr, file_path

def filter_cols(dictdataframe):
    

    if "plate_id" not in dictdataframe.columns:
        raise KeyError("Column plate_id not found. Please rename fitting Column to plate_id")
        
    grouped = dictdataframe.groupby("plate_id")# split metafile by plates
    
    df_dict = {}# dictionary for temporarily holding grouped plates
    
    for name, group in grouped:# check if plate names contain spaces, then read them into the dictionary
        name = str(name)
        clean_name = name.replace("", "")  
        df_dict[f"df_{clean_name}"] = group  
    # for name in df_dict.values():
    #     print(name)
    
    numbered_dict = {i: v for i, v in enumerate(df_dict.values())}
    
    return numbered_dict
    
def conv_dict(df1, i): #converting one dictoinary key into a variable because skbio does not like dataframes in dictionaries
    
    for key, df in df1.items():
        if "plate_id" in df.columns:
            df.drop(columns=["plate_id"], inplace=True)
            
    variabledf = df1[i]
    return variabledf

#fuse plate and spacer
#def Combine_plate_and_spacer(plates, spacer):
    #return pd.concat([plates, spacer], ignore_index=True)
    
def ordinationBuild(df2, i):
    """
    (later to be) main function
    legacy: detect, in case of column name "well_id" missing, which column 
    contains well_id values, then rename the column in case they choose another
    name. Replaced by letting the user rename the column hehe.
    """

    if "well_id" not in df2.columns:
        raise KeyError("No Column named well_id. Please rename fitting Column to well_id")

    """
    Detect, if NaN values were written into well_ids from sample_name,
    then deleting them 
    """
    # check for same well id on same plate
    x = 0
    for val in df2["well_id"].values:
        x += 1
        if type(val) is not str: # NaN is float
            #df2 = df2.drop(df2.index[x - 1])
            df2 = df2.drop(x - 1, errors="ignore") #shit errors=ignore is important, shouldnt be that way
            # filters 1st, 2nd plate etc...., 

    """
    split well_ids into letter and numbers: A1 --> A 1
    """
    def well_split(s):
        return pd.Series([str(s)[0],str(s)[1:]])
    df2[["row", "column"]] = df2["well_id"].apply(well_split)

    """
    convert letters from column x into their coordination numbers.
    IMPORTANT: A gets 8 while H gets 1 due to how wellplates are organised
    i could turn it around again by mirroring emperors axis, not planned yet
    """

    def well_convert(wl): 
        ch = "HGFEDCBA"
        if wl not in ch:
            return wl
        else:
            return ch.index(wl)+1
    df2["row"] = df2["row"].apply(well_convert)
    
    df2 = df2[pd.to_numeric(df2["column"], errors="coerce").notna()]# converts all wellid values into numbers, even nan values (they are still nan)
    
    
    #swap row and column, has to be swapped for ordination
    temp = df2["row"]
    df2["row"] = df2["column"].astype(float)
    df2["column"] = temp.astype(float)
    
    #create 3rd dataframe, trust me on this one
    whatever = {"sample_name": df2["sample_name"],
                "row": df2["row"],
                "column": df2 ["column"]}
    df3 = pd.DataFrame(data=whatever)
    return df3

#build final dataframe which does the ordination
def finalDataframeBuild(df2):
    df2["row"].astype(float)
    df2["column"].astype(float)
    
    samples = pd.DataFrame(
        data=df2[["row", "column"]].values,
        index=df2["sample_name"],
        columns=["row", "column"]
    )
    return samples

def ordinationWrite(samples, foldername, outputpath):
    # MAKE UP VALUES 
    eigvals = pd.Series([0.13, 0.37])# MADE UP VALUES
    proportion_explained = pd.Series([0.5758, 0.4242])#MADE UP VALUES

    """
    Finally the ordination building. Also writing the Ordination into the
    ordiantion.txt file
    """

    ordination = OrdinationResults(
        "Manual",
        "Parsed well ID ordination",
        eigvals,
        samples, 
        proportion_explained = proportion_explained
    )
    """
    fun fact if proportion explained wont be written the way it does it nukes
    the Ordination, because i am not giving all arguments to the ordination function as
    i dont need it here (there are more arguments between samples and proportion_explained).
    """
   
    with open(f"{outputpath}/ordination_{foldername}_.txt", "w") as f:

        ordination.write(f, format="ordination")
        
        
# def function_for_main():

#     df, filepath = load_file()
#     filtered_plates = filter_cols(df)

#     #for ordination names
#     file_dir = os.path.dirname(filepath)
#     folder_name = os.path.basename(file_dir)
#     return filtered_plates, folder_name
# filtered_plates, filepath = function_for_main()


# file paths for saving
output_qza = "output/artifact_results"
output_qzv = "output/emp_results"
output_ordin = "output/ordination_files"



"""
cd ~
for terminal: conda activate qiime2-amplicon-2024.10
"""
