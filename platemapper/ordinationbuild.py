import pandas as pd # pyright: ignore[reportMissingModuleSource]
from skbio.stats.ordination import OrdinationResults # pyright: ignore[reportMissingImports]

def filter_cols(dictdataframe):
    """
    Filtering metafile (e.g. meta_plate.tsv) by column "plate_id" in order to split one big pd.Dataframe 
    into smaller ones, filtered by plate number (e.g plate1, plate2, ...)

    Args:
        dictdataframe (pd.DataFrame): Dataframe, added by inserting path, Original Dataframe from metafile 

    Raises:
        KeyError:   Searching for "plate_id" in Dataframe Column names. Raises KeyError if "plate_id" is 
                    not found or missing, prompts User to create Column names "plate_id" 

    Returns:
        numbered_dict (Dictionary): Dictionary containing all of the split plates. Plate name gets replaced
                                    by index numbers (plate1 = 0, ...), important for later assembly
    """

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
    
def conv_dict(df_fromDict, i): 
    """
    Converting one dictionary key into a variable because skbio does not like dataframes in dictionaries

    Args:
        df_fromDict (Dictionary): The i'th index from the Dictionary created in ordinationbuild.filter_cols
                                    The key contains the according pd.DataFrame  
                                    
        i (int): Iteration: Counts how many plates have been passed and processed. Max: Number of plates present.

    Returns:
        variabledf (pd.DataFrame): DataFrame containing the corresponding Dictionary Key according to i.
    """
    # drop plate_id Column, no longer important
    for key, df in df_fromDict.items():
        if "plate_id" in df.columns:
            df.drop(columns=["plate_id"], inplace=True)
            
    variabledf = df_fromDict[i]
    return variabledf
    
def ordinationBuild(df2, i):
    """
    Build Dataframe to be ready for processing through skbio.stats.ordination. 
        Actions contain:
            1. Checking for Column name
            2. Deleting unnecessary NaN's
            3. Splitting well_id Coordinates into Letter and Number
            4. Converting well_id Chars into Numbers to be used for Coordination
            5. Positioning Axes correctly as well as changing variable types
            6. Creating the final ready to be used Dataframe.        
    Args:
        df2 (pd.DataFrame): pd.DataFrame given by ordinationbuild.conv_dict. 
        i (int): Iteration: Counts how many plates have been passed and processed. Max: Number of plates present.
    Raises:
        KeyError:  Searching for "well_id" in Dataframe Column names. Raises KeyError if "well_id" is 
                    not found or missing, prompts User to create Column names "well_id" 


    Returns:
        df3 (pd.DataFrame): Dataframe ready for ordinationbuilding through skbio.stats.ordination.
                            Only contains "sample_name", "row" and "column" as other columns are not important. 
    """
    
    if "well_id" not in df2.columns:
        raise KeyError("No Column named well_id. Please rename fitting Column to well_id")

    
    #Detect, if NaN values were written into well_ids from sample_name,
    #then deleting them 
    x = 0
    for val in df2["well_id"].values:
        x += 1
        if type(val) is not str: # NaN is float
            df2 = df2.drop(x - 1, errors="ignore") #shit errors=ignore is important, shouldnt be that way

    
    #split well_ids into letter and numbers: A1 --> A 1
    def well_split(s):
        return pd.Series([str(s)[0],str(s)[1:]])
    df2[["row", "column"]] = df2["well_id"].apply(well_split)
    
    #Convert Chars from "well_id" to Numbers
    #Important: A has to be counted as 8 and H as 1, well_plates count from up -> down 
    #while emperor counts down -> up
    def well_convert(wl): 
        ch = "HGFEDCBA"
        if wl not in ch:
            return wl
        else:
            return ch.index(wl)+1
    df2["row"] = df2["row"].apply(well_convert)
    
    # converts all wellid values into numbers, even nan values (they are still nan)
    df2 = df2[pd.to_numeric(df2["column"], errors="coerce").notna()]
    
    #swap row and column, has to be swapped for ordination
    temp = df2["row"]
    df2["row"] = df2["column"].astype(float)
    df2["column"] = temp.astype(float)
    
    #create 3rd and final dataframe
    whatever = {"sample_name": df2["sample_name"],
                "row": df2["row"],
                "column": df2 ["column"]}
    df3 = pd.DataFrame(data=whatever)
    return df3

def finalDataframeBuild(finaldataframe):
    """
    Sets Type float for Values in "row" and "column". Might throw this one away ngl

    Args:
        finaldataframe (pd.DataFrame): dataframe from ordinationbuild.ordinationbuild

    Returns:
        samples (pd.DataFrame): Final Dataframe for Ordination,
    """
    finaldataframe["row"].astype(float)
    finaldataframe["column"].astype(float)
    
    samples = pd.DataFrame(
        data=finaldataframe[["row", "column"]].values,
        index=finaldataframe["sample_name"],
        columns=["row", "column"]
    )
    return samples

def ordinationCreate(samples):
    """
    Creates PCoA Ordination file for creating visual plots through Emperor. 

    Variables:
        eigvals (pd.Series):    Made up Values. Its still necessary to give skbio some eigenvalues in order for 
                                the Ordination to build 
        
        proportion_explained (pd:series):   Made up Values. Its still necessary to give skbio some values in order for 
                                            the Ordination to build 
            
        Note:   I really cannot stress enough about how these Values are completely made up. 
                If you want you can alter the Numbers to your personal liking, it doesn't matter at all,
                as long as only 2 Numbers are assigned to each eigenvals and proportion_explained.
        
    Args:
        samples (pd.DataFrame): DataFrame containing all the interesting Infos for an Ordination

    Returns:
        ordination (skbio Ordinationfile):  ordination. Can be converted into a .txt file with 
                                            ordinationbuild.ordinationWrite for plotting via Emperor.
    """
    # MADE UP VALUES 
    eigvals = pd.Series([0.13, 0.37])# MADE UP VALUES
    proportion_explained = pd.Series([0.5758, 0.4242])#MADE UP VALUES

    # finally build Ordination
    ordination = OrdinationResults(
        "",
        "",
        eigvals = eigvals,
        samples = samples, 
        proportion_explained = proportion_explained
    )    
    return ordination

def ordinationWrite(ordination, foldername, outputpath):
    """
    Writing Ordination into a .txt file

    Args:
        ordination (skbio Ordination): Ordination as a Result of ordinationbuild.ordinationCreate
        foldername (str):   Foldername of Test/Study which contains the meta_plate.tsv file.  
                            OPTIONAL: Doesnt need to be used, just do foldername=None
        outputpath (str; path): Path in which the .txt file should be put in
    
    "Returns":
        Ordination.txt file for further use in Emperor.
    """
    
    filename = f"ordination{foldername}.txt" if foldername else "ordination.txt"
    with open(f"{outputpath}/{filename}", "w") as f:

        ordination.write(f, format="ordination")
        
# file paths for saving
output_qza = "output/artifact_results"
output_qzv = "output/emp_results"
output_ordin = "output/ordination_files"