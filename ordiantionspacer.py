import pandas as pd # pyright: ignore[reportMissingModuleSource]
import random
import string
import ordinationbuild
#import traceback


random.seed(1337)



# goal, generate a spacer ordination file and metadata file for spacing plates in one plot

#create random names for spacer vals
def generate_random_suffix(length=7):
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choices(chars, k=length))

def create_string_with_suffix(prefix='spacer', length=7):
    suffix = generate_random_suffix(length)
    return f"{prefix}_{suffix}"

spacer_list = [create_string_with_suffix() for _ in range(16)]

#df for spacer
def spacer_build_parts(spacer_list, i):
    offset = i*14
    column_values = [13+ offset ]*8 + [14+ offset]*8
    row_values = ["8","7","6","5","4","3","2","1"]*2

    spc= {"sample_name": spacer_list, 
            "column": row_values,
            "row": column_values,
            }
    spacer = pd.DataFrame(data=spc)
    
    return spacer

# df for metafile
def metafile_build_parts(spacer_list, i):
    offset = i*14
    column_values = [13+ offset ]*8 + [14+ offset]*8
    letters = ['H', 'G', 'F', 'E', 'D', 'C', 'B', 'A']*2
    
    metaspc = {"sample_name": spacer_list,
            "column": column_values,
            "row": letters
    }
    metafiledf = pd.DataFrame(data=metaspc)
    
    #swap
    temp = metafiledf["column"]
    metafiledf["column"] = metafiledf["row"]
    metafiledf["row"] = temp
    
    #fuse to well_id
    metafiledf["well_id"] = metafiledf["column"].astype(str) + metafiledf["row"].astype(str)
    
    # create df
    metafiledfFinal = {"sample_name": spacer_list,
        "well_id": metafiledf["well_id"].copy()}
    spacerformetafile = pd.DataFrame(data = metafiledfFinal)
    
    return spacerformetafile


def Add_Spacer(i):
    spacer_list = [create_string_with_suffix() for _ in range(16)]

    spacer_df = spacer_build_parts(spacer_list, i)
    metafile_df = metafile_build_parts(spacer_list, i)
    
    # print(f"Iteration {i}:")
    # print("Spacer sample_names (first 5):", spacer_df["sample_name"].head().tolist())
    # print("Metafile sample_names (first 5):", metafile_df["sample_name"].head().tolist())
    # print("Well IDs (first 5):", metafile_df["well_id"].head().tolist())
    # print("---")
    # print(f"Add_Spacer called with i={i}")
    # traceback.print_stack(limit=3)

    
    return spacer_df, metafile_df



