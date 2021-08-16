import os
import shutil
import pandas as pd
import numpy as np

cwd = os.getcwd()
#cwd = "C:\Users\MPedrazas\INTERA Inc\Hai Pham - 020_100BC\mpedrazas\scripts_100BC

# [Step 1] Read in files and make a copy of originals by suffixing p2_pred125:
#  Note. If *p1__pred125 files exist, they will be replaced.
input_dir = os.path.join(os.path.dirname(cwd),"Update.Predictive.Model","2006-2020_pred170")
cpfiles = ["100bc_2006-2020_p1_pred170.ghb","bc100_2006-2020_p1_pred170.drn","bc100_2006-2020_p1_pred170.riv"]
files = ["100bc_2006-2020_p2_pred170.ghb","bc100_2006-2020_p2_pred170.drn","bc100_2006-2020_p2_pred170.riv"]
for og, f in zip(cpfiles,files):
    print(f"Made copy of {og}, named {f}")
    try:
        if og.endswith('ghb'):
            shutil.copy2(os.path.join(input_dir,"02_genGHB",og), os.path.join(input_dir,"02_genGHB",f))
        else:
            shutil.copy2(os.path.join(input_dir, "01_genRIV", og), os.path.join(input_dir, "01_genRIV", f))
    except:
        print(f'Could not copy {og}')

# [Step 2] Append yearly SP and -1s until end of model timespan
SP = 165
for f in files:
    lines, start, end = [], [], []
    if f.endswith('ghb'):
        file = open(os.path.join(input_dir, "02_genGHB", f), 'r+')
    else: #ends with .drn or .riv
        file = open(os.path.join(input_dir, "01_genRIV", f),'r+')
    # read every line in file to get lines related to {SP}
    for idx, line in enumerate(file):
        lines.append((idx, line))
        if f"#sp={SP}" in line:
            start.append((idx, line))
        if f"#sp={SP+1}" in line:
            end.append((idx, line))
    for n in list(np.arange(start[0][0], end[0][0])):
        file.write(lines[n][1])
    print(f"Start line to copy:\n {lines[start[0][0]][1]}")
    file.write("-1\n"*110) #Append -1s for the following 110 SPs
    file.close()
    print(f"Updated: {f}\n")
