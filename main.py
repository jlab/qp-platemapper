import testing.filehandler as filehandler
import ordinationbuild 
import qiimebuild
import pandas as pd

#execute everything

filehandler.makefolder() 

# for i in ordinationbuild.filtered_plates:
    
#     df1 = ordinationbuild.conv_dict(ordinationbuild.filtered_plates, i)
    
#     ordinationbuild.ordinationBuild(df1, i)

for i in range(len(ordinationbuild.filtered_plates)):
    df4 = ordinationbuild.conv_dict(ordinationbuild.filtered_plates, i)
    samples = ordinationbuild.ordinationBuild(df4, i)
    endplate = ordinationbuild.Combine_plate_and_spacer(samples, i)
    
pd.DataFrame(endplate).to_csv("iminvain.tsv", sep="\t", index=False)

#ordinationbuild.ordinationBuild(endplate,i)
    
    
# qiimebuild.qzabuild()
# qiimebuild.empbuild()


"""
im still getting this futurewarning: FutureWarning: Setting an item of incompatible dtype is deprecated and will raise an error in a future version of pandas. Value '[nan nan nan nan nan nan nan nan nan nan nan nan nan nan nan nan nan nan
nan nan nan nan nan nan nan nan nan nan nan nan nan nan nan]' has dtype incompatible with float64, please explicitly cast to a compatible dtype first.
series[missing.index] = missing
  
maybe i will eventually find the fix to it, not very high on the priorities list rn
"""