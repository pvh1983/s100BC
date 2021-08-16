# -*- coding: utf-8 -*-
"""
Created on Thu Dec 31 09:28:14 2020

@author: MPedrazas
"""
# -*- coding: utf-8 -*-

import os
import pandas as pd
import fileinput
import csv

#%% Update Roff and Coff to df_TOB
ifile = f'../../mpedrazas/Transport_Model/T5_TOB_Package/COFF_ROFF/get_COFF_ROFF.xlsx'
# Read in model grid centroids and well coordinates
df_grid = pd.read_excel(ifile, sheet_name='grid')
df_wells = pd.read_excel(ifile, sheet_name='wells')
df_wells.dropna(axis=0, inplace=True)
df_wells.iloc[:,3:] = (df_wells.iloc[:,3:]).astype(int)

#%% merge dataframes based on row column location
df_grid['R_C']=df_grid['row'].astype(str) + "_" +  df_grid['column'].astype(str)
df_wells['R_C']=df_wells['i'].astype(str) + "_" +  df_wells['j'].astype(str)
df2 = df_wells.merge(df_grid,on=['R_C'], how='left', suffixes=('','_y'))

#%% Calculate ROFF and COFF
df2['ROFF'] = (((df2['ycoord'] - df2['centroid_y'])/df2['dely'])*-1).round(2)
df2['COFF'] = ((df2['xcoord'] - df2['centroid_x'])/df2['delx']).round(2)

df3 = df2[['Name','ROFF','COFF']]
# df2.to_csv('output/ROFF_COFF_forTOB_100BC.csv', index=False)

