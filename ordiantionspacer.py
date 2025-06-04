import pandas as pd # pyright: ignore[reportMissingModuleSource]
import random
import string

def generate_random_suffix(length=5):
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choices(chars, k=length))

def create_string_with_suffix(prefix='spacer', length=5):
    suffix = generate_random_suffix(length)
    return f"{prefix}_{suffix}"

spacer_list = [create_string_with_suffix() for _ in range(24)]
# Passende Spaltenwerte (z. B. 13 achtmal, 14 achtmal, 15 achtmal), muss noch dynamisch gemacht werden, z.b. zwischen plate 1 und 2 muss dann col 13+15, 14+15,16+15 sein, dann bei 2 und 3 muss es 13 +30, 14+30usw...
column_values = [13]*8 + [14]*8 + [15]*8
row_values = ["A","B","C","D","E","F","G","H"]*3

# Sicherstellen, dass beide Listen gleich lang sind
assert len(spacer_list) == len(column_values)


spc= {"sample_name": spacer_list, 
      "column": column_values,
      "row": row_values,
      }
spacer = pd.DataFrame(data=spc)
# end of dataframe

# for pd metafile
temp = spacer["column"]
spacer["column"] = spacer["row"]
spacer["row"] = temp
spacer["well_id"] = spacer["column"].astype(str) + spacer["row"].astype(str)
metafiledf = {"sample_name": spacer_list,
              "well_id": spacer["well_id"]
}
spacerformetafile = pd.DataFrame(data = metafiledf)
spacer = spacer.drop("well_id", axis=1)
#
# converting back
temp = spacer["column"]
spacer["column"] = spacer["row"]
spacer["row"] = temp
print(spacer)



#result: 
#       spacer = for ordination
#       spacerformetafile = containing sample name and well_id, needed for metafile 
