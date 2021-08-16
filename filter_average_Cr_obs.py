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


database = pd.read_excel(f'../Transport_Model/T01_EDA_Cr_concentration/EDA-Hexavalent-Cr-concentration-data-100-BC.xlsx', skiprows=0) #,names = ["WELL_NAME", "Date","Time", "Head (m)"],delimiter="   ")
df_Cr_comments = database[['SAMP_SITE_NAME', 'SAMP_DATE_TIME','STD_VALUE_RPTD',
            'STD_ANAL_UNITS_RPTD','FILTERED_FLAG', 'LAB_QUALIFIER',
            'REVIEW_QUALIFIER','SAMP_COMMENT', 'RESULT_COMMENT','COLLECTION_PURPOSE_DESC']]
df_Cr = database[['SAMP_SITE_NAME', 'SAMP_DATE_TIME','STD_VALUE_RPTD','REVIEW_QUALIFIER','COLLECTION_PURPOSE_DESC', 'LAB_CODE']]

df_Cr['SAMP_DATE_TIME'] = pd.to_datetime(df_Cr['SAMP_DATE_TIME'])
df_Cr['SAMP_DATE'] = df_Cr['SAMP_DATE_TIME'].dt.date
# color = {float('nan') : 'green', 'P': 'red', 'Y':'red', 'A':'green', 'H':'red', 'G':'green', 'PQ':'red', 'Q':'green',
#           'QP':'red', 'R':'red', 'AP':'red', 'APQ':'red',
#           'AQ':'green', 'PA':'red'}
color = {'WSCF':'green', 'TARL':'green', 'GEL':'green', '222-S':'green', 'PNL1':'green', 'MOBILE':'green', 'FIELD':'red',
    'USTEST':'green', 'RFWLVL':'green'}
# df_Cr['color'] = df_Cr['REVIEW_QUALIFIER'].map(color)
df_Cr['color'] = df_Cr['LAB_CODE'].map(color)

df_Cr = df_Cr[(df_Cr['SAMP_DATE_TIME'] <= datetime(2020, 9, 29))]
df_Cr = df_Cr[(df_Cr['SAMP_DATE_TIME'] >= datetime(2012, 1, 1))]
flags = ['R', 'H', 'P', 'R','Y','PQ' ,'QP','AP','APQ','PA']
for f in flags:
    df_Cr = df_Cr[(df_Cr['REVIEW_QUALIFIER'] != f)] #drop datapoints with "R" flag in review qualifier
df_Cr = df_Cr[(df_Cr['COLLECTION_PURPOSE_DESC'] != 'Characterization')] #drop datapoints used for characterization
obs_MAN_wells = pd.read_csv(f'../../final_deliverables/Head_Manual/Bore_Sample_File_in_model_manual.csv',names = ["WELL_NAME", "Date","Time", "Head (m)"],delimiter=",")
obs_AWLN_wells = pd.read_csv(f'../../final_deliverables/Head_AWLN/Bore_Sample_File_in_model_AWLN.csv',names = ["WELL_NAME", "Date","Time", "Head (m)"],delimiter=",")

wells = list(obs_MAN_wells.WELL_NAME.unique()) + list(obs_AWLN_wells.WELL_NAME.unique())
wells = list(set(wells))
df_Cr =df_Cr[df_Cr['SAMP_SITE_NAME'].isin(wells)]
df_Cr = df_Cr[(df_Cr['SAMP_DATE_TIME'] <= datetime(2020, 9, 29))]
df_Cr = df_Cr[(df_Cr['SAMP_DATE_TIME'] >= datetime(2012, 1, 1))]

lst = [] #find wells without data in model time period:
for i, well in enumerate(wells):
    df = df_Cr[df_Cr['SAMP_SITE_NAME'] == well]
    if len(df['STD_VALUE_RPTD']) == 0:
        print("This well doesn't have data in time period of interest:\n ", well)
        lst.append(well)
for i in lst: #drop wells without data in model time period:
    df_Cr = df_Cr[(df_Cr['SAMP_SITE_NAME'] != i)]
#export data
df_Cr.to_csv('output/Cr_data/Cr_obs_all_rev.csv', index=False)
wells = list(df_Cr.SAMP_SITE_NAME.unique())

#%% Plot concentration vs time to identify peaks visually
# plt.rc('xtick', labelsize=18)
# plt.rc('ytick', labelsize=18)

# for i, well in enumerate(wells):
#     fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10,5))
#     df = df_Cr[df_Cr['SAMP_SITE_NAME'] == well]
#     if len(df['STD_VALUE_RPTD']) > 0:
#         df = df[(df['SAMP_DATE_TIME'] <= datetime(2020, 9, 29))]
#         df = df[(df['SAMP_DATE_TIME'] >= datetime(2012, 1, 1))]
#         ax.plot(df['SAMP_DATE_TIME'],df['STD_VALUE_RPTD'], '--', markersize=10, markeredgecolor='k', 
#                    color='grey',  zorder=3)
#         ax.scatter(df['SAMP_DATE_TIME'],df['STD_VALUE_RPTD'], s=70, edgecolor='k',
#                 c=df['color'], label = str(well), zorder=10)
#         ax.axvline(x=pd.to_datetime('2012-01-01'), color = 'grey', zorder=2, alpha = 0.5)
#         ax.axhline(y=2,color = 'r', linestyle='--', zorder=1, alpha = 0.5)
#         ax.set_xlim(pd.to_datetime('2012-01-01'),pd.to_datetime('2020-09-30'))
#         # ax.set_ylim(min(df_Cr['STD_VALUE_RPTD']),max(df_Cr['STD_VALUE_RPTD']))
#         ax.set_title(well, fontsize=15, fontweight='bold')
#         ax.legend(fontsize=18)
#         ax.set_ylabel('Cr (VI) Concentration (ug/L)', fontweight='bold', fontsize=18)
#         ax.set_xlabel('Date', fontweight='bold', fontsize=18)
#         ax.grid(which='both', alpha = 0.5)
#         plt.savefig('output/Cr_figures/Cr_obs_data_QC/Cr_' + well+'_QC.png', bbox_inches='tight') 
#     plt.show()

# #%% Together all the data - AWLN
# plt.rc('xtick', labelsize=22)
# plt.rc('ytick', labelsize=22)

# lst_1 = ['199-B3-1',
#   '199-B3-47',
#   '199-B3-51', 
#     '199-B3-52']

# lst_2 = [ '199-B5-2',
#           '199-B4-1',
#           '199-B4-8']

# lst_3 = [
#   '199-B4-14',
#   # '199-B4-18',
#   '199-B4-7',
#   '199-B4-4',
#   '199-B5-13',
#   # '199-B5-6',
#   # '199-B5-9',
#   '199-B5-10',
#   # '199-B5-11',
#   '199-B5-12',
#   '199-B8-9',
# ]


# fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(20,10))
# for i, well in enumerate(lst_1):
#     df = df_Cr[df_Cr['SAMP_SITE_NAME'] ==well]
#     df = df[(df['SAMP_DATE_TIME'] <= datetime(2020, 9, 29))]
#     df = df[(df['SAMP_DATE_TIME'] >= datetime(2012, 1, 1))]
#     ax.plot(df['SAMP_DATE_TIME'],df['STD_VALUE_RPTD'], 'o-', markersize=10, markeredgecolor='k', 
#     label = str(well), zorder=10, linestyle='--')
#     ax.axvline(x=pd.to_datetime('2012-01-01'), color = 'grey', zorder=2, alpha = 0.5)
#     ax.axhline(y=2,color = 'r', linestyle='--', zorder=1, alpha = 0.5)
#     ax.set_xlim(pd.to_datetime('2012-01-01'),pd.to_datetime('2020-09-30'))
#     # ax.set_ylim(min(df_Cr['STD_VALUE_RPTD']),max(df_Cr['STD_VALUE_RPTD']))
#     ax.set_title('Wells Near River Source', fontsize=18, fontweight='bold')
#     ax.legend(fontsize=18)
#     ax.set_ylabel('Cr (VI) Concentration (ug/L)', fontweight='bold', fontsize=18)
#     ax.set_xlabel('Date', fontweight='bold', fontsize=18)
#     ax.grid(which='both', alpha = 0.5)
#     plt.savefig('output/Cr_figures/Cr_near_116B11.png', bbox_inches='tight') 
# plt.show()

# fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(20,10))
# for i, well in enumerate(lst_2):
#     df = df_Cr[df_Cr['SAMP_SITE_NAME'] ==well]
#     df = df[(df['SAMP_DATE_TIME'] <= datetime(2020, 9, 29))]
#     df = df[(df['SAMP_DATE_TIME'] >= datetime(2012, 1, 1))]
#     ax.plot(df['SAMP_DATE_TIME'],df['STD_VALUE_RPTD'], 'o-', markersize=10, markeredgecolor='k', 
#     label = str(well), zorder=10, linestyle='--')
#     ax.axvline(x=pd.to_datetime('2012-01-01'), color = 'grey', zorder=2, alpha = 0.5)
#     ax.axhline(y=2,color = 'r', linestyle='--', zorder=1, alpha = 0.5)
#     ax.set_xlim(pd.to_datetime('2012-01-01'),pd.to_datetime('2020-09-30'))
#     # ax.set_ylim(min(df_Cr['STD_VALUE_RPTD']),max(df_Cr['STD_VALUE_RPTD']))
#     ax.set_title('Wells Upgradient', fontsize=18, fontweight='bold')
#     ax.legend(fontsize=18)
#     ax.set_ylabel('Cr (VI) Concentration (ug/L)', fontweight='bold', fontsize=18)
#     ax.set_xlabel('Date', fontweight='bold', fontsize=18)
#     ax.grid(which='both', alpha = 0.5)
#     plt.savefig('output/Cr_figures/Cr_upgradient.png', bbox_inches='tight') 
# plt.show()

# fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(20,10))
# for i, well in enumerate(lst_3):
#     df = df_Cr[df_Cr['SAMP_SITE_NAME'] ==well]
#     df = df[(df['SAMP_DATE_TIME'] <= datetime(2020, 9, 29))]
#     df = df[(df['SAMP_DATE_TIME'] >= datetime(2012, 1, 1))]
#     ax.plot(df['SAMP_DATE_TIME'],df['STD_VALUE_RPTD'], 'o-', markersize=10, markeredgecolor='k', 
#     label = str(well), zorder=10, linestyle='--')
#     ax.axvline(x=pd.to_datetime('2012-01-01'), color = 'grey', zorder=2, alpha = 0.5)
#     ax.axhline(y=2,color = 'r', linestyle='--', zorder=1, alpha = 0.5)
#     ax.set_xlim(pd.to_datetime('2012-01-01'),pd.to_datetime('2020-09-30'))
#     ax.set_ylim(-1,180)
#     ax.set_title('Wells Near Big Dig', fontsize=18, fontweight='bold')
#     ax.legend(fontsize=18)
#     ax.set_ylabel('Cr (VI) Concentration (ug/L)', fontweight='bold', fontsize=18)
#     ax.set_xlabel('Date', fontweight='bold', fontsize=18)
#     ax.grid(which='both', alpha = 0.5)
#     plt.savefig('output/Cr_figures/Cr_near_bigdig.png', bbox_inches='tight') 
# plt.show()

# #%% Calculate peak times quantitatively 

# df_lst,peak_lst, well_lst, date_lst = [],[],[],[]
# for i, well in enumerate(wells):
#     df = df_Cr[df_Cr['SAMP_SITE_NAME'] ==well]
#     df = df[(df['SAMP_DATE_TIME'] <= datetime(2020, 9, 29))]
#     df = df[(df['SAMP_DATE_TIME'] >= datetime(2012, 1, 1))]
#     if len(df['STD_VALUE_RPTD']) > 0:
#         peak = max(df['STD_VALUE_RPTD'])
#         peak_date = df.loc[df['STD_VALUE_RPTD'] == peak, 'SAMP_DATE_TIME'].iloc[0]
#         # df.loc[df['B'] == 3, 'A'].iloc[0]
#         print(well,peak)
#         peak_lst.append(peak)
#         well_lst.append(well)
#         date_lst.append(peak_date)
# df_lst = pd.DataFrame({'well': well_lst,'peak value between 2012-2020': peak_lst,'peak date': date_lst})
# df_lst.to_csv('output/Cr_data/cr_peak_times_EDA.csv', index=False)

#%% Average repetitive observations from the same day

df_Cr['Time'] = pd.to_datetime(0, format='%H')
df_Cr['Time'] = df_Cr['Time'].dt.time
df_Cr['SAMP_DATE'] = pd.to_datetime(df_Cr['SAMP_DATE'])
df_Cr['SAMP_DATE'] = df_Cr['SAMP_DATE'].dt.date
dates = df_Cr['SAMP_DATE']; times = df_Cr['Time']
datetimes = pd.to_datetime(dates.astype(str)+ ' ' + times.astype(str))
df_Cr['Datetime'] = datetimes
df_Cr['Datetime'] = pd.to_datetime(datetimes)

lst_dups =[]
for i, well in enumerate(wells):
    df = df_Cr[df_Cr['SAMP_SITE_NAME'] == well]
    dups = df.duplicated(subset = ['Datetime'], keep=False)
    dups = dups.to_frame()
    print(dups)
    lst_dups.append(dups)
df_dups = pd.concat(lst_dups, axis=0)
df_dups = df_dups[df_dups[0] ==True]
print(df_dups)
# df_dups = df_dups.to_frame()

df_Cr_dups = df_Cr.copy()
# df_Cr_dups = df_Cr_dups.iloc[df_dups.index,:]
df_Cr_dups =df_Cr_dups[df_Cr_dups.index.isin(df_dups.index)]

# Find average for duplicates:
date_lst, well_lst,conc_lst = [],[],[]
for well in wells:
    df = df_Cr_dups[df_Cr_dups['SAMP_SITE_NAME'] == well]
    # print(well)
    for date in df['Datetime'].unique():
        df2 = df[df['Datetime'] == date]
        # print(date)
        # print(df2['STD_VALUE_RPTD'].mean())
        date_lst.append(date)
        conc_lst.append(df2['STD_VALUE_RPTD'].mean())
        well_lst.append(well)
df_dups_avg = pd.DataFrame({'SAMP_SITE_NAME': well_lst,'SAMP_DATE': date_lst,'STD_VALUE_RPTD': conc_lst})
        
df_Cr_no_dups = df_Cr.drop(axis=0, index=df_Cr_dups.index, inplace=False)
df_Cr_w_avg_dups = df_Cr_no_dups.append(df_dups_avg)
df_Cr_w_avg_dups = df_Cr_w_avg_dups[df_Cr_w_avg_dups['SAMP_SITE_NAME'].isin(wells)]
df_Cr_w_avg_dups = df_Cr_w_avg_dups[['SAMP_SITE_NAME','SAMP_DATE','STD_VALUE_RPTD']]
df_Cr_w_avg_dups.to_csv('output/Cr_data/Cr_obs_avg_dups_rev.csv', index=False)

 # QC: Plot duplicates to look at range of values, color-coded by well
fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(20,15))
for well in wells:
    df = df_Cr_dups[df_Cr_dups['SAMP_SITE_NAME'] == well]
    ax[0].plot(df['SAMP_DATE'],df['STD_VALUE_RPTD'], 'o', markersize=10, markeredgecolor='k', label= well)
    ax[0].set_ylabel('Cr (VI) Concentration (ug/L)', fontweight='bold', fontsize=18)
    ax[0].set_xlabel('Date', fontweight='bold', fontsize=18)
    ax[0].grid(which='both', alpha = 0.5)
    ax[0].set_title('Duplicates', fontsize=20, fontweight='bold')
    ax[0].legend(fontsize=16,bbox_to_anchor=(1.03, 1), loc='upper left')

    df2 = df_dups_avg[df_dups_avg['SAMP_SITE_NAME'] == well]
    ax[1].plot(df2['SAMP_DATE'],df2['STD_VALUE_RPTD'], 'o', markersize=10, markeredgecolor='k', label= well)
    ax[1].set_ylabel('Cr (VI) Concentration (ug/L)', fontweight='bold', fontsize=18)
    ax[1].set_xlabel('Date', fontweight='bold', fontsize=18)
    ax[1].grid(which='both', alpha = 0.5)
    ax[1].set_title('Mean of duplicates', fontsize=20, fontweight='bold')
    ax[1].legend(fontsize=16, bbox_to_anchor=(1.03, 1), loc='upper left')
plt.savefig('output/Cr_figures/Cr_duplicates_avg_rev.png', bbox_inches='tight') 

#%% Export csv file with well names and locations in x,y
# wells_xy_man  = pd.read_csv(r'C:/Users/MPedrazas/OneDrive - INTERA Inc/020_100BC/final_deliverables/Head_manual/Bore_coordinates_manual.csv', names = ['NAME','X','Y','Lay'])
# wells_xy_awln  = pd.read_csv(r'C:/Users/MPedrazas/OneDrive - INTERA Inc/020_100BC/final_deliverables/Head_AWLN/Bore_coordinates_AWLN.csv', names = ['NAME','X','Y','Lay'])
# wells_xy = pd.concat([wells_xy_man, wells_xy_awln])
# wells_xy.drop_duplicates(inplace=True)
# dfxy = df_Cr.merge(wells_xy, how='left',right_on='NAME', left_on='SAMP_SITE_NAME')
# dfxy = dfxy[['NAME', 'X', 'Y']]
# dfxy.drop_duplicates(subset='NAME',inplace=True) #drop columns and rows, only unique wellids
# dfxy.to_csv('output/Cr_data/Cr_wells_xy_v2.csv', index=False)
