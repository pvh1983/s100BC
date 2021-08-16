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
# Read first three lines of TOB package template (TOB input file configuration)
df_p1 = pd.read_excel(ifile, sheet_name='TOB_template', nrows=3)

#Read in AWLN well names and row,column, layer locations
df_ijk = pd.read_excel(ifile, sheet_name='AWLN_ijk')
#Read in times for transport model run
df_times = pd.read_excel(ifile, sheet_name='times')

#%% Update Roff and Coff to df_TOB
ifile2 = f'../../mpedrazas/Transport_Model/T5_TOB_Package/COFF_ROFF/get_COFF_ROFF_v1.xlsx'
# Read in model grid centroids and well coordinates
df_grid = pd.read_excel(ifile2, sheet_name='grid')
df_wells = pd.read_excel(ifile2, sheet_name='wells')
df_wells.dropna(axis=0, inplace=True)
df_wells.iloc[:,3:] = (df_wells.iloc[:,3:]).astype(int)

# merge dataframes based on row column location
df_grid['R_C']=df_grid['row'].astype(str) + "_" +  df_grid['column'].astype(str)
df_wells['R_C']=df_wells['i'].astype(str) + "_" +  df_wells['j'].astype(str)
df = df_wells.merge(df_grid,on=['R_C'], how='left', suffixes=('','_y'))

# Calculate ROFF and COFF
df['ROFF'] = (((df['ycoord'] - df['centroid_y'])/df['dely'])*-1).round(2)
df['COFF'] = ((df['xcoord'] - df['centroid_x'])/df['delx']).round(2)
df = df[['Name','ROFF','COFF']]
df.to_csv('output/ROFF_COFF_forTOB_100BC.csv', index=False)

#%% Create TOB Package
lst_name, lst_i, lst_j,lst_k  = [],[],[],[]
# Repeat each well, layer, row, col 144 times to collect time-series obs
for n in range(0,len(df_times)):
    for i,row in enumerate(df_ijk.iterrows()):
        lst_name.append(row[1].Name)
        lst_i.append(row[1].i)
        lst_j.append(row[1].j)
        lst_k.append(row[1].k)

df2 = pd.DataFrame(list(zip(lst_name,lst_k,lst_i,lst_j)), columns=['COBSNAM','LAYER','ROW','COLUMN'])
df2.sort_values(['COBSNAM','LAYER'], inplace=True)
df2.reset_index(inplace=True, drop=True)
df2['iComp'] = 1
lst_times = df_times.days.to_list()
df2['TimeObs'] =  lst_times*len(df_ijk)
df2['weight'] = 1
df2['COBS'] = 999
df2['COBSNAM_new'] = df2['COBSNAM'].astype(str) + "-" +  df2['LAYER'].astype(str)

df3 = df.merge(df2, how='right', right_on= 'COBSNAM', left_on = 'Name' )
df3 = df3[['COBSNAM_new', 'LAYER', 'ROW', 'COLUMN', 'iComp', 'TimeObs', 'ROFF', 'COFF',
       'weight', 'COBS']]
df3.iloc[:,[1,2,3,4,5,8,9]] = (df3.iloc[:,[1,2,3,4,5,8,9]]).astype(int) #will need to update code here
#%%
#concatenate into one dataframe and export:
# df_p1 = df_p1.iloc[:,0:10] #make same length as df
# df_p1.iloc[2,0] = len(df2) #update length of observations

#https://www.reddit.com/r/learnpython/comments/4zn20y/how_to_convert_sparse_pandas_dataframe_with_nan/

# df_p1.columns = ['# tob1 for 100-BC Transport Model for AWLN wells', '','','','','','','','','']
# df3.columns = df_p1.columns 
# df_TOB = pd.concat([df_p1,df3])

#%%
# df_TOB.to_csv('output/100BC_tob1_v2.tob', index=False, sep="\t", 
#                 quoting=csv.QUOTE_NONE, quotechar="", escapechar="",
#                 float_format='%.0f')
df3.to_csv('output/100BC_tob1_v4.tob', index=False, sep="\t")
#PROBLEM WITH EXPORTING CSV BECAUSE DECIMAL PLACES EXIT FOR COFF and ROFF
check = pd.read_csv('output/100BC_tob1_v4.tob')


