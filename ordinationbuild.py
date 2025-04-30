import pandas as pd
from skbio.stats.ordination import OrdinationResults
import tkinter
from tkinter import filedialog
import os

"""
Use tkinter to choose a file conveniently from a file Explorer,
then insert into a dataframe(datafr). Will get scrapped.
"""

def load_file():
    
    tkinter.Tk().withdraw()
    folder_path = filedialog.askopenfilename(filetypes=[("TSV files", "*.tsv")])
    datafr = pd.read_csv(folder_path, sep='\t')
    if not folder_path:
        print("ERROR")
    else:
        0
    return datafr

def filter_cols(dictdataframe):
    
    
    grouped = dictdataframe.groupby("plate_id")

    df_dict = {}
    
    for name, group in grouped:
        clean_name = name.replace(" ", "")  
        df_dict[f"df_{clean_name}"] = group  

        
    return df_dict

def conv_dict(df1, i):
    #maybe fusing filter_cols and conv_dict together, lets see
    for key, df in df1.items():
        if "plate_id" in df.columns:
            df.drop(columns=["plate_id"], inplace=True)
            # probably not of use since i create a clean dataframe for the ordinatio
    
    variabledf = df1[i]
    return variabledf

def ordinationBuild(df2):
    """
    (later to be) main function
    legacy: detect, in case of column name "well_id" missing, which column 
    contains well_id values, then rename the column in case they choose another
    name. Replaced by letting the user rename the column hehe.
    """

    if "well_id" in df2.columns:
        1
    else:
        print("ERROR: Columnn name well_id not found in Metafile. Please rename the fitting Column to well_id.")


    """
    Detect, if NaN values were written into well_ids from sample_name,
    then deleting them 
    """
    
    
    
    x = 0
    for val in df2["well_id"].values:
        x += 1
        if type(val) is not str: # NaN is float
            df2 = df2.drop(x - 1)

    """
    split well_ids into letter and numbers: A1 --> A 1
    """
    def well_split(s):
        return pd.Series([s[0],s[1:]])

    df2[["x", "y"]] = df2["well_id"].apply(well_split)

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

    df2["x"] = df2["x"].apply(well_convert)

    """
    Swap the x and y axis as the values with former letters have to be on the
    y Axis, i WILL change the Axis names somethime in the Future (i promise).
    And while im at it, im converting all values to floats as building the ordination
    get less stressing if the values are floats.
    """

    temp = df2["x"]
    df2["x"] = df2["y"].astype(float)
    df2["y"] = temp.astype(float)

    #create final dataframe for Ordination
    samples = pd.DataFrame(
        data=df2[["x", "y"]].values,
        index=df2["sample_name"],
        columns=["x", "y"]
    )

    """
    Ordination prep: invent Eigenvalues and proportion explained as they are
    Useless in our application.
    """

    eigvals = pd.Series([0.13, 0.37])
    proportion_explained = pd.Series([0.5758, 0.4242])

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
   
    with open(f"{output_ordin}/ordination{i}.txt", "w") as f:

        ordination.write(f, format="ordination")# has to be written in  a way that outputs multiple ordination.txt files
        
    

    """
    Now a function, however it HAS to be activated via terminal with e.g python3 ordiantionbuild.py 
    while in a conda qiime environment
    """


df = load_file()
filtered_plates = filter_cols(df)



output_ordin = "output/ordination_files"
os.makedirs(output_ordin, exist_ok=True)

for i in filtered_plates:
    df1 = conv_dict(filtered_plates, i)
    ordinationBuild(df1)


"""
for terminal: conda activate qiime2-amplicon-2024.10
"""
