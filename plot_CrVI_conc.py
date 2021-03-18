# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 08:47:35 2020

@author: MPedrazas
"""
import os
import pandas as pd
import fileinput
import csv
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, date, time
import flopy
import flopy.utils.binaryfile as bf
import flopy.utils as fu
import time
from datetime import date
import glob
import shutil
import sys

#%% USING TOB file:
    
ifile = f'../../hpham/transport/tob/STUFF_OCN.txt'
dfocn=pd.read_csv(ifile, delimiter=' *, *', engine='python', header=None, names=['WELLID-LAY','TIME_DELTA','CALCULATED']) # use "WELLID", "CALCULATED" concentration, "TIME_ELAPSED" in days  
dfocn['WELLID-LAY'].str.strip() #strip extra whitespace from well names    
dfocn['WELLID'] = dfocn['WELLID-LAY'].str.rsplit(pat="-", n=1).str[0]
dfocn['LAY'] = dfocn['WELLID-LAY'].str.rsplit(pat="-", n=1).str[1].astype(int)

# there are only ten faulty values in 30 days (check on them later)
df_sim = dfocn.copy()
df_sim.CALCULATED = pd.to_numeric(df_sim.CALCULATED, errors = 'coerce')
df_sim = df_sim.dropna()
df_sim.TIME_DELTA = pd.to_timedelta(df_sim.TIME_DELTA, unit="days")
df_sim['DATE'] = df_sim.TIME_DELTA + pd.to_datetime('2012-01-01')
# table=pd.pivot_table(dfocn,index='WELLID', columns='TIME_ELAPSED', values='CALCULATED')
df_obs = pd.read_csv('output/Cr_observations.csv')
df_obs['SAMP_DATE'] = pd.to_datetime(df_obs['SAMP_DATE'])

# Check units:
#     df_obs is in ug/L
#     df_sim might just be in ug

#%% Plot simulated vs observed
plt.rc('xtick', labelsize=18)
plt.rc('ytick', labelsize=18)

for i, well in enumerate(df_sim['WELLID'].unique()):
    sim = df_sim[(df_sim['WELLID'] == well)]
    obs = df_obs[df_obs['SAMP_SITE_NAME'] == well]
    for j, lay in enumerate(sim['LAY'].unique()):
        sim2 = sim[sim['LAY'] == lay]
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10,5))
        ax.plot(sim2['DATE'],sim2['CALCULATED']/1000, '--', markersize=10, markeredgecolor='k', 
                color='grey',  zorder=3, label = 'Layer ' + str(lay))
        ax.scatter(obs['SAMP_DATE'],obs['STD_VALUE_RPTD'], s=70, edgecolor='k',
                c='r', zorder=10)
        ax.axvline(x=pd.to_datetime('2012-01-01'), color = 'grey', zorder=2, alpha = 0.5)
        ax.axhline(y=2,color = 'r', linestyle='--', zorder=1, alpha = 0.5)
        ax.set_xlim(pd.to_datetime('2012-01-01'),pd.to_datetime('2020-09-30'))
        # ax.set_ylim(min(df_obs['STD_VALUE_RPTD']),max(df_obs['STD_VALUE_RPTD']))
        ax.set_title(well, fontsize=15, fontweight='bold')
        ax.legend(fontsize=18)
        ax.set_ylabel('Cr (VI) Concentration (ug/L)', fontweight='bold', fontsize=18)
        ax.set_xlabel('Date', fontweight='bold', fontsize=18)
        ax.grid(which='both', alpha = 0.5)
        plt.savefig('output/Cr_figures/sim_vs_obs/Cr_' + str(well)+'-lay' + str(lay) + '.png', bbox_inches='tight') 
        plt.show()

#%% Now try plotting with UCN file
## start code Timer
t0 = time.time()
ucn_filename = f'../../hpham/transport/model_2012_2020/100BC_2012_2020_transport_ver0.ucn'
ucnobj = bf.UcnFile(ucn_filename, precision="double")
times = ucnobj.get_times()
spucn=ucnobj.get_kstpkper()
# # convert tuples
dfspt=pd.DataFrame(spucn, columns=['ts','sp'])
## add times to dfspt, get one dataframe with ts,sp,and times
se_times=pd.Series(times)   # make series
dfspt["days"]=se_times.values
# dfspt.to_csv(ucn_filename[:-4] + '_UCN_dfspt.csv', index=False)

#%%
#Read in AWLN well names and row,column, layer locations
ifile2 = f'../../mpedrazas/Transport_Model/T5_TOB_Package/100BC_TOB_v1.xlsx'
df_ijk = pd.read_excel(ifile2, sheet_name='AWLN_ijk')

# Checking with well '199-B3-47': ijk = 72,198,[1,2]
conc_lst, conc_lst2= [],[]
for t in range(0,len(times)):
    conc = ucnobj.get_data(totim = times[t])[1,72,198]
    conc2 = ucnobj.get_data(totim = times[t])[2,72,198]
    conc_lst.append(conc)
    conc_lst2.append(conc2)
    conc_lst = [float(item) for item in conc_lst]
    conc_lst2 = [float(item) for item in conc_lst2]
    

df_ucn = pd.DataFrame({'conc':conc_lst, 'conc2': conc_lst2, 'times':times}) 

df_ucn.times = pd.to_timedelta(df_ucn.times, unit="days")
df_ucn.times = df_ucn.times+ pd.to_datetime('2012-01-01')
df_ucn.times = pd.to_datetime(df_ucn.times)
    # temp = conc[1,99,140] #layer, row, column slice of concentration

# lst_name, lst_i, lst_j,lst_k  = [],[],[],[]
# # Repeat each well, layer, row, col 144 times to collect time-series obs
# for n in range(0,len(df_times)):
#     for i,row in enumerate(df_ijk.iterrows()):
#         lst_name.append(row[1].Name)
#         lst_i.append(row[1].i)
#         lst_j.append(row[1].j)
#         lst_k.append(row[1].k)

#%% Plot from UCN File
well_lst = ['199-B3-47']
for i,well in enumerate(well_lst):
    print(well)
    sim = df_sim[(df_sim['WELLID'] == well)]
    obs = df_obs[df_obs['SAMP_SITE_NAME'] == well]
    # for j, lay in enumerate(sim['LAY'].unique()):
    sim2 = sim[sim['LAY'] == 1]
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10,5))
    ax.plot(df_ucn.times,df_ucn.conc/1000, '--', markersize=10, markeredgecolor='k', 
            color='grey',  zorder=3, label = 'UCN Layer ' + str(1))
    ax.plot(sim2['DATE'],sim2['CALCULATED']/1000, '--', markersize=10, markeredgecolor='k', 
            color='blue',  zorder=3, label = 'TOB Layer ' + str(1))
    # ax.scatter(obs['SAMP_DATE'],obs['STD_VALUE_RPTD'], s=70, edgecolor='k',
    #         c='r', zorder=10)
    ax.axvline(x=pd.to_datetime('2012-01-01'), color = 'grey', zorder=2, alpha = 0.5)
    ax.axhline(y=2,color = 'r', linestyle='--', zorder=1, alpha = 0.5)
    ax.set_xlim(pd.to_datetime('2012-01-01'),pd.to_datetime('2020-09-30'))
    # ax.set_ylim(min(df_obs['STD_VALUE_RPTD']),max(df_obs['STD_VALUE_RPTD']))
    ax.set_title(well, fontsize=15, fontweight='bold')
    ax.legend(fontsize=18)
    ax.set_ylabel('Cr (VI) Concentration (ug/L)', fontweight='bold', fontsize=18)
    ax.set_xlabel('Date', fontweight='bold', fontsize=18)
    ax.grid(which='both', alpha = 0.5)
    # plt.savefig('output/Cr_figures/sim_vs_obs/Cr_UCN_' + str(well)+'-lay' + str(1) + '.png', bbox_inches='tight') 
    plt.show()
    
for i,well in enumerate(well_lst):
    print(well)
    sim = df_sim[(df_sim['WELLID'] == well)]
    obs = df_obs[df_obs['SAMP_SITE_NAME'] == well]
    # for j, lay in enumerate(sim['LAY'].unique()):
    sim2 = sim[sim['LAY'] == 2]
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10,5))
    ax.plot(df_ucn.times,df_ucn.conc2/1000, '--', markersize=10, markeredgecolor='k', 
            color='grey',  zorder=3, label = 'UCN Layer ' + str(2))
    ax.plot(sim2['DATE'],sim2['CALCULATED']/1000, '--', markersize=10, markeredgecolor='k', 
            color='blue',  zorder=3, label = 'TOB Layer ' + str(2))
    # ax.scatter(obs['SAMP_DATE'],obs['STD_VALUE_RPTD'], s=70, edgecolor='k',
    #         c='r', zorder=10)
    ax.axvline(x=pd.to_datetime('2012-01-01'), color = 'grey', zorder=2, alpha = 0.5)
    ax.axhline(y=2,color = 'r', linestyle='--', zorder=1, alpha = 0.5)
    ax.set_xlim(pd.to_datetime('2012-01-01'),pd.to_datetime('2020-09-30'))
    # ax.set_ylim(min(df_obs['STD_VALUE_RPTD']),max(df_obs['STD_VALUE_RPTD']))
    ax.set_title(well, fontsize=15, fontweight='bold')
    ax.legend(fontsize=18)
    ax.set_ylabel('Cr (VI) Concentration (ug/L)', fontweight='bold', fontsize=18)
    ax.set_xlabel('Date', fontweight='bold', fontsize=18)
    ax.grid(which='both', alpha = 0.5)
    # plt.savefig('output/Cr_figures/sim_vs_obs/Cr_UCN_' + str(well)+'-lay' + str(2) + '.png', bbox_inches='tight') 
    plt.show()
#%% UCN vs TOB

# fig, ax = plt.subplots(nrows=1, ncols = 1, figsize=(10,10)) 
# ax.plot(obs_MAN_2020['Head (m)'],conc_lst , 'o', markerfacecolor="steelblue", markeredgecolor='blue', markeredgewidth=1,markersize=10, alpha =0.5, zorder=1)
# ax.plot([0, 1], [0, 1], color='red', linewidth=0.5, transform=ax.transAxes, zorder=10)