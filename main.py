import testing.filehandler as filehandler
import ordinationbuild 
import ordiantionspacer
import qiimebuild
import pandas as pd

#execute everything

filehandler.makefolder() 
endplate = None
metaspacer = None


for i in range(len(ordinationbuild.filtered_plates)):
    

    df4 = ordinationbuild.conv_dict(ordinationbuild.filtered_plates, i)
    
    samplesnotfinal = ordinationbuild.ordinationBuild(df4, i)
    samplesnotfinal["row"] += i*14
    
    #create spacer
    spacer_df, metafile_df = ordiantionspacer.Add_Spacer(i)
    #print(f"Before combining, spacer sample_names (first 5): {spacer_df['sample_name'].head().tolist()}")

    combined = ordinationbuild.Combine_plate_and_spacer(samplesnotfinal, spacer_df)
    
    
    
    if metaspacer is None:
        metaspacer = metafile_df.copy()
    else:
        metaspacer = pd.concat([metaspacer, metafile_df], ignore_index=True)
        
        
    if endplate is None:
        endplate = combined.copy()
    else:
        endplate = pd.concat([endplate, combined], ignore_index=True)
    #final dataframe created, has to undergo wll split again
samples = ordinationbuild.finalDataframeBuild(endplate)
ordinationbuild.ordinationWrite(samples)

metafile = pd.concat([ordinationbuild.df, metaspacer], ignore_index=True)






#endplate["row"] = endplate["row"].apply(ordinationbuild.well_convert)

pd.DataFrame(metafile).to_csv("meta_plate.tsv", sep="\t", index=False)
#pd.DataFrame(metaspacer).to_csv("metafilespacers.tsv", sep="\t", index=False)

qiimebuild.qzabuildsingle()
qiimebuild.empbuildsingle()
# qiimebuild.qzabuild()
# qiimebuild.empbuild()


"""
im still getting this futurewarning: FutureWarning: Setting an item of incompatible dtype is deprecated and will raise an error in a future version of pandas. Value '[nan nan nan nan nan nan nan nan nan nan nan nan nan nan nan nan nan nan
nan nan nan nan nan nan nan nan nan nan nan nan nan nan nan]' has dtype incompatible with float64, please explicitly cast to a compatible dtype first.
series[missing.index] = missing
  
maybe i will eventually find the fix to it, not very high on the priorities list rn
"""