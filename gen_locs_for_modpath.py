# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 06:30:10 2020
This script creates more .loc files for all the wells.
@author: MPedrazas
"""

import pandas as pd

# def Head_AWLN():
ifile = f'../Transport/MODPATH_test1/particle_set.loc'
wells_loc = f'../Transport/obs_well_loc_ijk.xlsx'
# ofile_ins = 'output/pst_ins/Head_AWLN.ins'

df_loc = pd.read_csv(ifile, sep=' ', names = ['i','j','k','x','y','z','7','8','9','10'])
df_loc_lay1 = df_loc[df_loc.k == 1]
df_awln_wells = pd.read_excel(wells_loc, sheet_name='uni_AWLN_well') #sheet_name='AWLN'
layers = [1,2,3,4,5,6] #
df_final=[]

for n, lay in enumerate(layers):
    df_lst = []
    for c, well in enumerate(df_awln_wells['Name']):
        print(well,c)
        df = df_loc_lay1.copy()
        df.i = df_awln_wells.i[c]
        df.j = df_awln_wells.j[c]
        df.k = layers[n]
        df_lst.append(df)
    df_final = pd.concat(df_lst)
    df_final.to_csv('output/modpath/particle_set_lay' + str(lay) + '.loc', index=False, header=False)
