import filehandler
import ordinationbuild 
import qiimebuild

#execute everything

filehandler.makefolder() 

for i in ordinationbuild.filtered_plates:
    df1 = ordinationbuild.conv_dict(ordinationbuild.filtered_plates, i)
    ordinationbuild.ordinationBuild(df1, i)
    
qiimebuild.qzabuild()
qiimebuild.empbuild()


"""
im still getting this futurewarning: FutureWarning: Setting an item of incompatible dtype is deprecated and will raise an error in a future version of pandas. Value '[nan nan nan nan nan nan nan nan nan nan nan nan nan nan nan nan nan nan
nan nan nan nan nan nan nan nan nan nan nan nan nan nan nan]' has dtype incompatible with float64, please explicitly cast to a compatible dtype first.
series[missing.index] = missing
  
maybe i will eventually find the fix to it, not very high on the priorities list rn
"""