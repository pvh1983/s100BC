import pandas as pd
import os

###### prepare Bore_Sample_File_in_model_dirns.csv for 2012-2020
### Select certain wells from mod2obs wells to use in dirn operations.
def prep_file_for_mod2obs(path2mod2obs,wells, ofilename):
    lines = []
    for well in wells:
        print(well)
        with open(path2mod2obs, 'r') as file:
            for idx, line in enumerate(file):
                if line.startswith(well + ','): #comma added at the end to avoid confusion between B5-1 and B5-14 for example.
                    lines.append(line)
    with open(os.path.join(inputDir,f"Bore_Sample_File_in_model_{ofilename}_v2.csv"), 'w') as file2:
        for n in range(len(lines)):
            file2.write(lines[n])
    return None

if __name__ == "__main__":
    cwd = os.getcwd()
    inputDir = os.path.join(os.path.dirname(cwd), "Update.Predictive.Model", "2006-2020_pred170", "03_evalGrad")
    path2mod2obs = os.path.join(inputDir, 'Bore_Sample_File_in_model_AWLN.csv')
    wellDict = {'NorthWells': ['199-B5-1', '199-B3-51', '199-B3-50'],
                'SouthWells': ['199-B4-14', '199-B5-8', '199-B8-6'],
                'CenterWells': ['199-B5-1', '199-B4-16', '199-B3-50']}
    for key in list(wellDict.keys()):
        prep_file_for_mod2obs(path2mod2obs, wellDict[key], key)

########## Helal meeting
# C:\Users\MPedrazas\INTERA Inc\Hai Pham - 020_100BC\final_deliverables\preprocess\Truex_well_network_2020