# -*- coding: utf-8 -*-
"""
Created on Fri Mar 19 10:15:23 2021

@author: MPedrazas
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 08:47:35 2020

@author: MPedrazas
"""
import os
import pandas as pd
import fileinput
import csv

# Read observation values and wells
df_Cr = pd.read_csv(f'../../final_deliverables/Cr_obs_ALL/Cr_obs_avg_dups_rev.csv')
df_Cr.rename(columns={'SAMP_SITE_NAME':'Well Name',
                                'SAMP_DATE':'Date/Time',
                                'STD_VALUE_RPTD':'Concentration (ug/L)'}, inplace=True)
df_Cr['Date/Time'] = pd.to_datetime(df_Cr['Date/Time']).dt.strftime('%m/%d/%Y %H:%M')
df_Cr.sort_values(by=['Well Name','Date/Time'], inplace=True)

df_tot = []
for well in df_Cr['Well Name'].unique():
    df = df_Cr[df_Cr['Well Name'] == well]
    df.to_csv(os.path.join(os.path.dirname(os.getcwd()),
   'Transport_Model','T07_Preprocess_Cr_Obs','conc_2021','Targets',str(well)+'conc.csv'),
              index=False)
    df_tot.append(df)
    # df.to_csv(os.path.join(os.getcwd(),'output','Targets_conc_2021'),
    #       index=False)

df_tot2 = pd.concat(df_tot)

