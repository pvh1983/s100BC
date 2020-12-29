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

#%% Create TOB Package
lst_name, lst_i, lst_j,lst_k  = [],[],[],[]
cutoff_len = 144
# Repeat each well, layer, row, col 144 times to collect time-series obs
for n in range(0,cutoff_len):
    for i,row in enumerate(df_ijk.iterrows()):
        lst_name.append(row[1].Name)
        lst_i.append(row[1].i)
        lst_j.append(row[1].j)
        lst_k.append(row[1].k)

df = pd.DataFrame(list(zip(lst_name,lst_k,lst_i,lst_j)), columns=['COBSNAM','LAYER','ROW','COLUMN'])
df.sort_values(['COBSNAM','LAYER'], inplace=True)
df.reset_index(inplace=True, drop=True)
df['iComp'] = 1
lst_times = df_times.days.to_list()
df['TimeObs'] =  lst_times*len(df_ijk)
df['Roff'] = 0.0
df['Coff'] = 0.0
df['weight'] = 1
df['COBS'] = 999

#concatenate into one dataframe and export:
df_p1 = df_p1.iloc[:,0:10] #make same length as df
df_p1.iloc[2,0] = len(df) #update length of observations
# df_p1.iloc[:,1:4] = int(df_p1.iloc[:,1:4]) #will need to update code here
#https://www.reddit.com/r/learnpython/comments/4zn20y/how_to_convert_sparse_pandas_dataframe_with_nan/

df_p1.columns = ['# tob1 for 100-BC Transport Model for AWLN wells', '','','','','','','','','']
df.columns = df_p1.columns 
final_df = pd.concat([df_p1,df])
final_df.to_csv('output/100BC_tob1_v1.tob', index=False, sep="\t", 
                quoting=csv.QUOTE_NONE, quotechar="", escapechar="",
                float_format='%.0f')



