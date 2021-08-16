import os
import shutil
import pandas as pd
import numpy as np

cwd = os.getcwd()
#cwd = "C:\Users\MPedrazas\INTERA Inc\Hai Pham - 020_100BC\mpedrazas\scripts_100BC

# [Step 1] Read in files
input_dir = os.path.join(os.path.dirname(cwd),"Update.Predictive.Model","2006-2020_pred170")
oldfiles = ["100BC_5m_GeoV2_Evaluated_V3.rch"]
newfiles = ["100BC_5m_GeoV2_Evaluated_V0_pred170.rch"]

# for og, f in zip(cpfiles,files):
#     try:
#         shutil.copy2(os.path.join(os.path.dirname(input_dir),"2006-2015_pred125",og),
#                      os.path.join(input_dir,"04_updateRCH",f))
#         print(f"Made copy of {og}, named {f}")
#     except:
#         print(f'Could not copy {og}')

# [Step 2] Find three recharge rates, get rid of 1st rch rate (before 2021)
for og, f in zip(oldfiles, newfiles):
    lines, start, end = [], [], []
    file = open(os.path.join(os.path.dirname(input_dir),"2006-2015_pred125", og), 'r')
    file2 = open(os.path.join(input_dir, "04_updateRCH", f), 'w') #write new file for updated predictive model
    # read every line in file to get lines related to {SP}
    for idx, line in enumerate(file):
        lines.append((idx, line))
        if "        18" in line:
            start.append((idx, line))
    for n in list(np.arange(0, start[0][0])): #write lines until before 1st rch rate
        file2.write(lines[n][1])
    for n in list(np.arange(start[1][0], lines[-1][0]+1)): #write lines after 2nd rch rate until eof
        file2.write(lines[n][1])
    file.close()
    file2.close()
    print(f"Updated: {f}\n")

# [Step 3]
### Append -1s at eof to account for new extended model that goes farther in time:
#old model ended in 2140, updated model ends in 2190.
# Recharge rates changed in 2011, 2021, 2051
#old model transition from monthly to yearly is 2066, so after 2051.
#Checked that there are (30 years x 12 = 360) 360 -1(actual rch rate) = 359 SPs
# Therefore 359 -1s appended between 2nd and 3rd rch rate.
#there should be (2066-2051= 15 yrs) 15 x 12 SPs = 180 monthly SPs, + (2140-2066 = 75) 75 yearly SPs
#total of at least 255 SPs = -1s appended after third rch rate. There is 1225 SPs appended at eof.