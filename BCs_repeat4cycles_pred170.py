
import os
import shutil
import pandas as pd

cwd = os.getcwd()
#cwd = "C:\Users\MPedrazas\INTERA Inc\Hai Pham - 020_100BC\mpedrazas\scripts_100BC

# [Step 1] Read in files and make a copy of originals by suffixing _pred170:
#  Note. If *_pred170 files exist, they will be replaced.
input_dir = os.path.join(os.path.dirname(cwd),"Update.Predictive.Model","2006-2020_pred170")
cpfiles = ["100bc_2006-2020.ghb","bc100_2006-2020.drn","bc100_2006-2020.riv"]
files = ["100bc_2006-2020_p1_pred170.ghb","bc100_2006-2020_p1_pred170.drn","bc100_2006-2020_p1_pred170.riv"]
for og, f in zip(cpfiles,files):
    print(f"Made copy of {og}, named {f}")
    try:
        if og.endswith('ghb'):
            shutil.copy2(os.path.join(input_dir,"02_genGHB",og), os.path.join(input_dir,"02_genGHB",f))
        else:
            shutil.copy2(os.path.join(input_dir, "01_genRIV", og), os.path.join(input_dir, "01_genRIV", f))
    except:
        print(f'Could not copy {og}')

# [Step 2] Append three times the same values to have 4 cycles of 2006 to 2020 monthly SPs.
for f in files:
    lines = []
    if f.endswith('ghb'):
        file = open(os.path.join(input_dir, "02_genGHB",f),'r+')
    else: #ends with .drn or .riv
        file = open(os.path.join(input_dir, "01_genRIV", f),'r+')
    for idx, line in enumerate(file):
        lines.append(line) #x2
    for i in range(3):
        for j in range(1, len(lines)):   #the first line is a header, do not repeat
            if j == len(lines)-1:
                print(f"Start line to copy:\n", j)
            file.write(lines[j])
    print(f"Updated: {f}\n")
    file.close()
