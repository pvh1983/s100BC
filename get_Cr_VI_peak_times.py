# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 09:42:15 2020

@author: MPedrazas
"""
import pandas as pd;
import os;
import platform;
import numpy as np;
import matplotlib.pyplot as plt
from datetime import datetime, date, time


database = pd.read_excel(f'../Transport/T1_EDA_Cr_concentration/EDA-Hexavalent-Cr-concentration-data-100-BC.xlsx', skiprows=0) #,names = ["WELL_NAME", "Date","Time", "Head (m)"],delimiter="   ")
df_Cr_comments = database[['SAMP_SITE_NAME', 'SAMP_DATE_TIME','STD_VALUE_RPTD',
                'STD_ANAL_UNITS_RPTD','FILTERED_FLAG', 'LAB_QUALIFIER',
                'REVIEW_QUALIFIER','SAMP_COMMENT', 'RESULT_COMMENT']]

df_Cr = database[['SAMP_SITE_NAME', 'SAMP_DATE_TIME','STD_VALUE_RPTD']]

df_Cr['SAMP_DATE_TIME'] = pd.to_datetime(df_Cr['SAMP_DATE_TIME'])
df_Cr['SAMP_DATE'] = df_Cr['SAMP_DATE_TIME'].dt.date

AWLN_wells = ['199-B2-14', '199-B3-46', '199-B3-47', '199-B3-50',
 '199-B3-51', '199-B4-7', '199-B4-8', '199-B4-14', '199-B4-16', 
 '199-B4-18', '199-B5-1', '199-B5-6', '199-B5-8', '199-B5-13',
 '199-B8-6', '199-B8-9', '199-B9-3','699-71-77']

df_Cr_AWLN =df_Cr[df_Cr['SAMP_SITE_NAME'].isin(AWLN_wells)]
df_Cr_AWLN = df_Cr_AWLN[(df_Cr_AWLN['SAMP_DATE_TIME'] <= datetime(2020, 9, 29))]
df_Cr_AWLN = df_Cr_AWLN[(df_Cr_AWLN['SAMP_DATE_TIME'] >= datetime(2012, 1, 1))]

#%% Plot concentration vs time to identify peaks visually
plt.rc('xtick', labelsize=18)
plt.rc('ytick', labelsize=18)

wells = df_Cr['SAMP_SITE_NAME'].unique().tolist()

for i, well in enumerate(AWLN_wells):
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10,5))
    df = df_Cr[df_Cr['SAMP_SITE_NAME'] ==well]
    df = df[(df['SAMP_DATE_TIME'] <= datetime(2020, 9, 29))]
    df = df[(df['SAMP_DATE_TIME'] >= datetime(2012, 1, 1))]
    ax.plot(df['SAMP_DATE_TIME'],df['STD_VALUE_RPTD'], 'o-', markersize=10, markeredgecolor='k', 
                     color='steelblue', label = str(well), zorder=10)
    ax.axvline(x=pd.to_datetime('2012-01-01'), color = 'grey', zorder=2, alpha = 0.5)
    ax.axhline(y=2,color = 'r', linestyle='--', zorder=1, alpha = 0.5)
    ax.set_xlim(pd.to_datetime('2012-01-01'),pd.to_datetime('2020-09-30'))
    # ax.set_ylim(min(df_Cr['STD_VALUE_RPTD']),max(df_Cr['STD_VALUE_RPTD']))
    ax.set_title(well, fontsize=15, fontweight='bold')
    ax.legend(fontsize=18)
    ax.set_ylabel('Cr (VI) Concentration (ug/L)', fontweight='bold', fontsize=18)
    ax.set_xlabel('Date', fontweight='bold', fontsize=18)
    ax.grid(which='both', alpha = 0.5)
    # if (well == '199-B5-2' or '199-B4-1'):
        # plt.savefig('output/Cr_figures/Cr_' + well+'_manual_v2.png', bbox_inches='tight')  #needs fixing
    # else:
        # plt.savefig('output/Cr_figures/Cr_' + well+'_v2.png', bbox_inches='tight') 
plt.show()

#%% Together all the data

lst_1 = ['199-B2-14',
 '199-B3-46',
 '199-B3-47',
 '199-B3-50',
 '199-B3-51', 
 '699-71-77']

lst_2 = [ '199-B4-7',
 '199-B4-8',
 '199-B4-16',
 '199-B4-18',
 '199-B5-8',
  '199-B9-3',
  '199-B8-9']

lst_3 = [
 '199-B4-14',
 '199-B5-13',
 '199-B8-6',
 '199-B5-1',
 '199-B5-6',
]


fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(20,10))
for i, well in enumerate(lst_1):
    df = df_Cr[df_Cr['SAMP_SITE_NAME'] ==well]
    df = df[(df['SAMP_DATE_TIME'] <= datetime(2020, 9, 29))]
    df = df[(df['SAMP_DATE_TIME'] >= datetime(2012, 1, 1))]
    ax.plot(df['SAMP_DATE_TIME'],df['STD_VALUE_RPTD'], 'o-', markersize=10, markeredgecolor='k', 
    label = str(well), zorder=10)
    ax.axvline(x=pd.to_datetime('2012-01-01'), color = 'grey', zorder=2, alpha = 0.5)
    ax.axhline(y=2,color = 'r', linestyle='--', zorder=1, alpha = 0.5)
    ax.set_xlim(pd.to_datetime('2012-01-01'),pd.to_datetime('2020-09-30'))
    # ax.set_ylim(min(df_Cr['STD_VALUE_RPTD']),max(df_Cr['STD_VALUE_RPTD']))
    ax.set_title('Wells Near River', fontsize=18, fontweight='bold')
    ax.legend(fontsize=18)
    ax.set_ylabel('Cr (VI) Concentration (ug/L)', fontweight='bold', fontsize=18)
    ax.set_xlabel('Date', fontweight='bold', fontsize=18)
    ax.grid(which='both', alpha = 0.5)
    # plt.savefig('output/Cr_figures/Cr_near_river.png', bbox_inches='tight') 
plt.show()

fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(20,10))
for i, well in enumerate(lst_2):
    df = df_Cr[df_Cr['SAMP_SITE_NAME'] ==well]
    df = df[(df['SAMP_DATE_TIME'] <= datetime(2020, 9, 29))]
    df = df[(df['SAMP_DATE_TIME'] >= datetime(2012, 1, 1))]
    ax.plot(df['SAMP_DATE_TIME'],df['STD_VALUE_RPTD'], 'o-', markersize=10, markeredgecolor='k', 
    label = str(well), zorder=10)
    ax.axvline(x=pd.to_datetime('2012-01-01'), color = 'grey', zorder=2, alpha = 0.5)
    ax.axhline(y=2,color = 'r', linestyle='--', zorder=1, alpha = 0.5)
    ax.set_xlim(pd.to_datetime('2012-01-01'),pd.to_datetime('2020-09-30'))
    # ax.set_ylim(min(df_Cr['STD_VALUE_RPTD']),max(df_Cr['STD_VALUE_RPTD']))
    ax.set_title('Wells Far East', fontsize=18, fontweight='bold')
    ax.legend(fontsize=18)
    ax.set_ylabel('Cr (VI) Concentration (ug/L)', fontweight='bold', fontsize=18)
    ax.set_xlabel('Date', fontweight='bold', fontsize=18)
    ax.grid(which='both', alpha = 0.5)
    # plt.savefig('output/Cr_figures/Cr_far_east.png', bbox_inches='tight') 
plt.show()

fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(20,10))
for i, well in enumerate(lst_3):
    df = df_Cr[df_Cr['SAMP_SITE_NAME'] ==well]
    df = df[(df['SAMP_DATE_TIME'] <= datetime(2020, 9, 29))]
    df = df[(df['SAMP_DATE_TIME'] >= datetime(2012, 1, 1))]
    ax.plot(df['SAMP_DATE_TIME'],df['STD_VALUE_RPTD'], 'o-', markersize=10, markeredgecolor='k', 
    label = str(well), zorder=10)
    ax.axvline(x=pd.to_datetime('2012-01-01'), color = 'grey', zorder=2, alpha = 0.5)
    ax.axhline(y=2,color = 'r', linestyle='--', zorder=1, alpha = 0.5)
    ax.set_xlim(pd.to_datetime('2012-01-01'),pd.to_datetime('2020-09-30'))
    ax.set_ylim(-1,75)
    ax.set_title('Wells Far West', fontsize=18, fontweight='bold')
    ax.legend(fontsize=18)
    ax.set_ylabel('Cr (VI) Concentration (ug/L)', fontweight='bold', fontsize=18)
    ax.set_xlabel('Date', fontweight='bold', fontsize=18)
    ax.grid(which='both', alpha = 0.5)
    # plt.savefig('output/Cr_figures/Cr_far_west_v2.png', bbox_inches='tight') 
plt.show()

#%% Calculate peak times quantitatively 

df_lst,peak_lst, well_lst, date_lst = [],[],[],[]
for i, well in enumerate(AWLN_wells):
    df = df_Cr[df_Cr['SAMP_SITE_NAME'] ==well]
    df = df[(df['SAMP_DATE_TIME'] <= datetime(2020, 9, 29))]
    df = df[(df['SAMP_DATE_TIME'] >= datetime(2012, 1, 1))]
    peak = max(df['STD_VALUE_RPTD'])
    peak_date = df.loc[df['STD_VALUE_RPTD'] == peak, 'SAMP_DATE_TIME'].iloc[0]
    # df.loc[df['B'] == 3, 'A'].iloc[0]
    print(well,peak)
    peak_lst.append(peak)
    well_lst.append(well)
    date_lst.append(peak_date)
df_lst = pd.DataFrame({'well': well_lst,'peak value between 2012-2020': peak_lst,'peak date': date_lst})
# df_lst.to_csv('output/cr_peak_times_EDA.csv', index=False)

#%% Plot of distance from river vs peak time.


#%% Average repetitive observations from the same day

df_Cr_AWLN['Time'] = pd.to_datetime(0, format='%H')
df_Cr_AWLN['Time'] = df_Cr_AWLN['Time'].dt.time
df_Cr_AWLN['SAMP_DATE'] = pd.to_datetime(df_Cr_AWLN['SAMP_DATE'])
df_Cr_AWLN['SAMP_DATE'] = df_Cr_AWLN['SAMP_DATE'].dt.date
dates = df_Cr_AWLN['SAMP_DATE']; times = df_Cr_AWLN['Time']
datetimes = pd.to_datetime(dates.astype(str)+ ' ' + times.astype(str))
df_Cr_AWLN['Datetime'] = datetimes
df_Cr_AWLN['Datetime'] = pd.to_datetime(datetimes)

lst_dups =[]
for i, well in enumerate(AWLN_wells):
    df = df_Cr_AWLN[df_Cr_AWLN['SAMP_SITE_NAME'] ==well]
    dups = df.duplicated(subset = ['Datetime'], keep=False)
    dups = dups.to_frame()
    print(dups)
    lst_dups.append(dups)
df_dups = pd.concat(lst_dups, axis=0)
df_dups = df_dups[df_dups[0] ==True]
print(df_dups)
# df_dups = df_dups.to_frame()

df_Cr_dups = df_Cr_AWLN.copy()
# df_Cr_dups = df_Cr_dups.iloc[df_dups.index,:]
df_Cr_dups =df_Cr_dups[df_Cr_dups.index.isin(df_dups.index)]

# Find average for duplicates:
date_lst, well_lst,conc_lst = [],[],[]
for well in AWLN_wells:
    df = df_Cr_dups[df_Cr_dups['SAMP_SITE_NAME'] == well]
    print(well)
    for date in df['Datetime'].unique():
        df2 = df[df['Datetime'] == date]
        print(date)
        # print(df2['STD_VALUE_RPTD'].mean())
        date_lst.append(date)
        conc_lst.append(df2['STD_VALUE_RPTD'].mean())
        well_lst.append(well)
df_dups_avg = pd.DataFrame({'SAMP_SITE_NAME': well_lst,'SAMP_DATE': date_lst,'STD_VALUE_RPTD': conc_lst})
        
df_Cr_no_dups = df_Cr_AWLN.drop(axis=0, index=df_Cr_dups.index, inplace=False)
df_Cr_w_avg_dups = df_Cr_no_dups.append(df_dups_avg)
df_Cr_w_avg_dups = df_Cr_w_avg_dups[df_Cr_w_avg_dups['SAMP_SITE_NAME'].isin(AWLN_wells)]
df_Cr_w_avg_dups = df_Cr_w_avg_dups[['SAMP_SITE_NAME','SAMP_DATE','STD_VALUE_RPTD']]
# df_Cr_w_avg_dups.to_csv('output/Cr_concentration_with_avg_dups.csv', index=False)

 # QC: Plot duplicates to look at range of values, color-coded by well
fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(20,15))
for well in AWLN_wells:
    df = df_Cr_dups[df_Cr_dups['SAMP_SITE_NAME'] == well]
    ax[0].plot(df['SAMP_DATE'],df['STD_VALUE_RPTD'], 'o', markersize=10, markeredgecolor='k', label= well)
    ax[0].set_ylabel('Cr (VI) Concentration (ug/L)', fontweight='bold', fontsize=18)
    ax[0].set_xlabel('Date', fontweight='bold', fontsize=18)
    ax[0].grid(which='both', alpha = 0.5)
    ax[0].set_title('Duplicates', fontsize=20, fontweight='bold')
    ax[0].legend(fontsize=16,bbox_to_anchor=(1.03, 1), loc='upper left')

    df2 = df_dups_avg[df_dups_avg['SAMP_SITE_NAME'] ==well]
    ax[1].plot(df2['SAMP_DATE'],df2['STD_VALUE_RPTD'], 'o', markersize=10, markeredgecolor='k', label= well)
    ax[1].set_ylabel('Cr (VI) Concentration (ug/L)', fontweight='bold', fontsize=18)
    ax[1].set_xlabel('Date', fontweight='bold', fontsize=18)
    ax[1].grid(which='both', alpha = 0.5)
    ax[1].set_title('Mean of duplicates', fontsize=20, fontweight='bold')
    ax[1].legend(fontsize=16, bbox_to_anchor=(1.03, 1), loc='upper left')
# plt.savefig('output/Cr_figures/Cr_duplicates_avg.png', bbox_inches='tight') 
