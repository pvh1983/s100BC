# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 08:47:35 2020

@author: MPedrazas
"""
import os
import pandas as pd
import fileinput
import csv

ifile = f'../../mpedrazas/Transport_Model/T5_TOB_Package/100BC_TOB_v1.xlsx'
#Read in AWLN well names and row,column, layer locations
df_ijk = pd.read_excel(ifile, sheet_name='AWLN_ijk')

# Read observation values and wells
df_Cr = pd.read_csv(f'../../final_deliverables/Cr_obs_AWLN/Cr_concentration_with_avg_dups.csv')

df_Cr_sp = pd.read_csv(f'../Transport_Model/T7_Preprocess_Cr_Obs/conc_2020/targets.csv')

#%%
df_p1 = df_Cr.merge(df_ijk, how = 'left', left_on = 'SAMP_SITE_NAME',  right_on = 'Name')
# df_p1.to_csv('output/ijk_for_TOB.csv', index=False)


df_p2 = df_Cr_sp.merge(df_ijk, how = 'left', left_on = 'well',  right_on = 'Name')
df_p2.rename(columns={'well':'Well Name',
                                'sp':'SP',
                                'target':'Concentration (ug/L)'}, inplace=True)
df_p2.drop(['Name'],axis=1, inplace=True)
df_p2.to_csv('output/ijk_for_TOB_sp.csv', index=False)

