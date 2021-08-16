# -*- coding: utf-8 -*-
"""
Created on Wed May 12 16:34:52 2021

@author: MPedrazas
"""
import pandas as pd;
import os;
import platform;
import numpy as np;
import matplotlib.pyplot as plt
from datetime import datetime, date, time


#%% ###### create dumy values for 2012-2014 AWLN input file for mod2obs in order to get continuous simulated hds
sp = pd.read_csv(r"C:\Users\MPedrazas\OneDrive - INTERA Inc\020_100BC\final_deliverables\preprocess\head_2020\stress_periods.csv", delimiter=',')
sp['end'] = pd.to_datetime(sp['end'],format='%y%m%d')

dfs = []
wells = ['N-RC93-198','C-RC93-198','S-RC93-198'] 
for i, well in enumerate(wells):
    print(well)
    df_new = pd.DataFrame(columns = ['WELL_NAME','Date','Time','Head (m)'])
    df_new['Date'] = sp['end']
    df_new['WELL_NAME'] = well
    df_new['Time'] = pd.to_datetime(0, format='%H')
    df_new['Time'] = df_new['Time'].dt.time
    df_new['Head (m)'] = -9999
    dfs.append(df_new)
df_final = pd.concat(dfs)
outputDir=r'C:\Users\MPedrazas\OneDrive - INTERA Inc\020_100BC\mpedrazas\100BC_GWM\model_files\WLs_forSTOMP_sim_cell'
df_final.to_csv(os.path.join(outputDir,'Bore_Sample_File_in_model_cell.csv'), index=False) #csv file for mod2obs

print('Saved {}'.format('Bore_Sample_File_in_model_cell.csv'))
print('Remember to delete column names/n')