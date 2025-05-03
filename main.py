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


