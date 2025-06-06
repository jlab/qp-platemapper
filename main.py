import testing.filehandler as filehandler
import ordinationbuild 
import ordiantionspacer
import qiimebuild
import pandas as pd # pyright: ignore[reportMissingModuleSource]

#execute everything

# make folderstructure
filehandler.makefolder() 

#create empty variables, important later on
endplate = None
metaspacer = None


for i in range(len(ordinationbuild.filtered_plates)):
    # get single plate as variable out of dictionary
    df4 = ordinationbuild.conv_dict(ordinationbuild.filtered_plates, i)
    #edit plate: well split, well convert
    samplesnotfinal = ordinationbuild.ordinationBuild(df4, i)
    
    #for multiple plates: offset plate by 14 columns
    samplesnotfinal["row"] += i*13
    
    #create spacer
    #spacer_df, metafile_df = ordiantionspacer.Add_Spacer(i)
    # combine spacer and plate for the ordination file
    #combined = ordinationbuild.Combine_plate_and_spacer(samplesnotfinal)
    combined = samplesnotfinal
    
    # insert spacer data for metafile into df. This one contains sample_name and well_id e.g F8, B4 etc.
    # if metaspacer is None:
    #     metaspacer = metafile_df.copy()
    # else:
    #     metaspacer = pd.concat([metaspacer, metafile_df], ignore_index=True)
        
    # same song here. This one contains sample name and row/column  e.g 3 8, 7 4 etc...  
    if endplate is None:
        endplate = combined.copy()
    else:
        endplate = pd.concat([endplate, combined], ignore_index=True)

#taking combined plates and spacers
samples = ordinationbuild.finalDataframeBuild(endplate)
#write ordination with skbio 
ordinationbuild.ordinationWrite(samples)

#fuse metafile with metadata for spacers
#metafile = pd.concat([ordinationbuild.df, metaspacer], ignore_index=True)
#save new metafile as .tsv for emperor building
#pd.DataFrame(metafile).to_csv("meta_plate.tsv", sep="\t", index=False)

#build qza and qzv plot
qiimebuild.qzabuildsingle()
qiimebuild.empbuildsingle()

"""
im still getting this futurewarning: FutureWarning: Setting an item of incompatible dtype is deprecated and will raise an error in a future version of pandas. Value '[nan nan nan nan nan nan nan nan nan nan nan nan nan nan nan nan nan nan
nan nan nan nan nan nan nan nan nan nan nan nan nan nan nan]' has dtype incompatible with float64, please explicitly cast to a compatible dtype first.
series[missing.index] = missing
  
maybe i will eventually find the fix to it, not very high on the priorities list rn
"""