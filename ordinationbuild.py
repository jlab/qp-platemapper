import pandas as pd
from skbio.stats.ordination import OrdinationResults
import tkinter
from tkinter import filedialog

"""
Use tkinter to choose a file conveniently from a file Explorer,
then insert into a dataframe(df2)
"""
tkinter.Tk().withdraw()
folder_path = filedialog.askopenfile()

datafr = pd.read_csv(folder_path, sep='\t')

def ordinationBuild(df2):
    """
    (later to be) main function
    legacy: detect, in case of column name "well_id" missing, which column 
    contains well_id values, then rename the column in case they choose another
    name. Replaced by letting the user rename the column hehe.
    """

    werte = ["A1", "A2"] # Das hier muss noch unbedingt mit regex gemacht werden für den wahrscheinlichen fall dass auf der 
    #plate die ersten beiden wells nicht benutzt werden.


    # Passende Spalte finden und umbenennen
    if "well_id" not in df2.columns:
        for spalte in df2.columns:
            if all(wert in df2[spalte].values for wert in werte):
                print(f"beide Werte in spalte: {spalte}")
                df2 = df2.rename(columns={"spalte": "well_id"})
    else:
        1
    # Andernfalls eine variable mit den wellids erstellen und damit weiterarbeiten

    # testing: nachschauen ob es geklappt hat
    if "well_id" in df2.columns:
        #print("ja")
        1


    """
    Detect, if NaN values were written into well_ids from sample_name,
    then deleting them 
    """
    x = 0
    for val in df2["well_id"].values:
        x += 1
        if type(val) is not str:
            # NaN ist n float
            #print(df2.sample_name.values[x-1])
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

    #finalen dataframe erstellen aus welchem auch die ordination am ende entsteht
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
        # fun fact wenn man proportion_explained im selben stil 
        # wie samples & eigvals schreibt sprengt das komplett die Ordiantion
        # ist wichitg, da normalerweise noch werte zwischen 
        # samples und proportion_explained existieren, die sind aber irrelevant
    )

    with open("ordination.txt", "w") as f:

        ordination.write(f, format="ordination")
        
    

    """
    Now a function, however it HAS to be activated via terminal with e.g python3 ordiantionbuild.py 
    while in a conda qiime environment
    """

ordinationBuild(datafr)