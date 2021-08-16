"""
# reads PST file produced by TOB package
# copies "getit_dp.exe" to COC directory 
# runs GR's script "getit_dp.exe" in COC directory to produce 

# INPUT:  
#        binary file of time series of concentration: 'STUFF.PST', derived from *.OCN output of TOB
#        text file telling the program to the name of input and output files: ' inputfile_UCL95.txt'
# OUTPUT: 
#        "STUFF_OCN.txt" - same data as text file (non-binary)
"""

import os
import pandas as pd
import subprocess
import shutil
import time
import sys
import platform

print('python: {}'.format(".".join(map(str, sys.version_info[:3]))))    # 2.7.10
if ('python version: 2') != ('python version: {}'.format(platform.python_version()[0])):
    print("WRONG Python version used for this script. This script requires python version 2.")
    sys.exit()     
print('pandas version: {}'.format(pd.__version__))                      # 0.21.0


wd1=os.getcwd()
basedir = os.path.dirname(wd1)

## start code Timer 
t0 = time.time()

# copy getit_dp.exe into current directory
#f1=os.path.join(basedir,'INPUT_files','getit_dp.exe')
#shutil.copy2(f1,wd1)
#f2=os.path.join(basedir,'INPUT_files','inputfile_UCL95.txt')   
#shutil.copy2(f2,wd1)                
#https://stackoverflow.com/questions/15167603/using-files-as-stdin-and-stdout-for-subprocess
# run GR's *.exe here
#     print wd2
myinput=open('inputfile_UCL95.txt'))
p = subprocess.Popen('getit_dp.exe', stdin=myinput)
time.sleep(10)
print os.getcwd()
     
## stop code timer
t1 = time.time()
total = (t1-t0)/60
print "Time elapsed : {} minutes".format(total)
#%%     