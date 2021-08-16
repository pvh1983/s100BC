import os
import shutil
import pandas as pd
import numpy as np

cwd = os.getcwd()
#cwd = "C:\Users\MPedrazas\INTERA Inc\Hai Pham - 020_100BC\mpedrazas\scripts_100BC

# [Step 1] Read in files
input_dir = os.path.join(os.path.dirname(cwd),"Update.Predictive.Model","2006-2020_pred125")
newfiles = ["100BC_5m_GeoV2_Evaluated_V0_pred170yrs.oc"]

#[STEP 1] Write new file for updated predictive model
monthlySP, yearlySP = 720, 110
for f in newfiles:
    lines, start, end = [], [], []
    with open(os.path.join(input_dir, "05_updateOC", f), 'w') as file:
        file.write("  HEAD SAVE UNIT 30\n")
        file.write("  HEAD PRINT FORMAT 0\n")
        file.write("  DRAWDOWN SAVE UNIT 31\n")
        file.write("  DRAWDOWN PRINT FORMAT 0\n")
        file.write("  COMPACT BUDGET\n")
        for i in np.arange(1,monthlySP+1):
            file.write(f"PERIOD {i} STEP 1\n")
            file.write(" Save HEAD\n")
            file.write(" Save BUDGET\n")
            file.write(" Print BUDGET\n")
        for i in np.arange(monthlySP+1, monthlySP + yearlySP + 1):
            for j in np.arange(1,5+1):
                if j == 5:
                    file.write(f"PERIOD {i} STEP {j}\n")
                    file.write(" Save HEAD\n")
                    file.write(" Save BUDGET\n")
                    file.write(" Print BUDGET\n")
                else: #j != 5
                    file.write(f"PERIOD {i} STEP {j}\n")
                    file.write(" Print BUDGET\n")








