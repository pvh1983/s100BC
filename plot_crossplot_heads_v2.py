# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 14:50:08 2020

@author: MPedrazas
"""

import pandas as pd;
import os;
import platform;
import numpy as np;
import matplotlib.pyplot as plt
from datetime import datetime, date, time

from sklearn.metrics import r2_score 

#%% [1] cross-plot man 2020
plt.rc('xtick', labelsize=18)
plt.rc('ytick', labelsize=18)
sim_MAN_2020 = pd.read_csv(f'../../final_deliverables/Head_Manual/bore_sample_output_manual.dat',names = ["WELL_NAME", "Date","Time", "Head (m)"],delimiter="   ")
obs_MAN_2020 = pd.read_csv(f'../../final_deliverables/Head_Manual/Bore_Sample_File_in_model_manual.csv',names = ["WELL_NAME", "Date","Time", "Head (m)"],delimiter=",")

fig, ax = plt.subplots(nrows=1, ncols = 1, figsize=(10,10)) 
ax.plot(obs_MAN_2020['Head (m)'],sim_MAN_2020['Head (m)'] , 'o', markerfacecolor="steelblue", markeredgecolor='blue', markeredgewidth=1,markersize=10, alpha =0.5, zorder=1)
ax.plot([0, 1], [0, 1], color='red', linewidth=0.5, transform=ax.transAxes, zorder=10)
ax.set_ylim(118,124)
ax.set_xlim(118,124)

#     ax.set_title(well, fontsize=15, fontweight='bold')
ax.set_ylabel('Simulated Head 2012-2020', fontweight='bold', fontsize=18)
ax.set_xlabel('Observed Head 2012-2020', fontweight='bold', fontsize=18)
ax.grid(which='both', alpha = 0.5)
r2 = r2_score(obs_MAN_2020['Head (m)'], sim_MAN_2020['Head (m)']).round(2)
# plt.text(118.2,123.5,'$\mathregular{r^2}$ = '+str(r2), fontsize = 18)
#     ax.legend(fontsize=14)
# plt.savefig('output/crossplots_v2/man-2020.png', bbox_inches='tight') 
plt.show()
plt.close()

#%% [2] cross-plot man 2014
plt.rc('xtick', labelsize=18)
plt.rc('ytick', labelsize=18)
sim_MAN_2014 = pd.read_csv(f'../../final_deliverables/Head_Manual/bore_sample_output_manual_2014.dat',names = ["WELL_NAME", "Date","Time", "Head (m)"],delimiter="   ")
obs_MAN_2014 = pd.read_csv(f'../../final_deliverables/Head_Manual/Bore_Sample_File_in_model_manual_2014.csv',names = ["WELL_NAME", "Date","Time", "Head (m)"],delimiter=",")

fig, ax = plt.subplots(nrows=1, ncols = 1, figsize=(10,10)) 
ax.plot(obs_MAN_2014['Head (m)'],sim_MAN_2014['Head (m)'] , 'o', markerfacecolor="steelblue", markeredgecolor='blue', markeredgewidth=1,markersize=10, alpha =0.5, zorder=1)
ax.plot([0, 1], [0, 1], color='red', linewidth=0.5, transform=ax.transAxes, zorder=10)
ax.set_ylim(118,124)
ax.set_xlim(118,124)

#     ax.set_title(well, fontsize=15, fontweight='bold')
ax.set_ylabel('Simulated Head 2012-2014', fontweight='bold', fontsize=18)
ax.set_xlabel('Observed Head 2012-2014', fontweight='bold', fontsize=18)
ax.grid(which='both', alpha = 0.5)
r2 = r2_score(obs_MAN_2014['Head (m)'], sim_MAN_2014['Head (m)']).round(2)
# plt.text(118.2,123.5,'$\mathregular{r^2}$ = '+str(r2), fontsize = 18)
#     ax.legend(fontsize=14)
# plt.savefig('output/crossplots/man-2014.png', bbox_inches='tight') 
plt.show()
plt.close()
#%% [3] cross-plot awln  2020
plt.rc('xtick', labelsize=18)
plt.rc('ytick', labelsize=18)
# sim_AWLN_2020 = pd.read_csv(f'../../final_deliverables/Head_AWLN/bore_sample_output_AWLN.dat',names = ["WELL_NAME", "Date","Time", "Head (m)"],delimiter="   ")
sim_AWLN_2020 = pd.read_csv(f'../../hpham/100BC_Calibration_model/PEST_2012-2020/bore_sample_output_AWLN_v1.dat',names = ["WELL_NAME", "Date","Time", "Head (m)"],delimiter="   ")
# obs_AWLN_2020 = pd.read_csv(f'../../final_deliverables/Head_AWLN/Bore_Sample_File_in_model_AWLN.csv',names = ["WELL_NAME", "Date","Time", "Head (m)"],delimiter=",")
obs_AWLN_2020 = pd.read_csv(f'../../hpham/100BC_Calibration_model/PEST_2012-2020/Bore_Sample_File_in_model_AWLN_v1.csv',names = ["WELL_NAME", "Date","Time", "Head (m)"],delimiter=",")

fig, ax = plt.subplots(nrows=1, ncols = 1, figsize=(10,10)) 
ax.plot(obs_AWLN_2020['Head (m)'],sim_AWLN_2020['Head (m)'] , 'o', markerfacecolor="steelblue", markeredgecolor='blue', markeredgewidth=1,markersize=10, alpha =0.5, zorder=1)
ax.plot([0, 1], [0, 1], color='red', linewidth=0.5, transform=ax.transAxes, zorder=10)
ax.set_ylim(118,124.5)
ax.set_xlim(118,124.5)

#     ax.set_title(well, fontsize=15, fontweight='bold')
ax.set_ylabel('Simulated Head 2012-2020', fontweight='bold', fontsize=18)
ax.set_xlabel('Observed Head 2012-2020', fontweight='bold', fontsize=18)
ax.grid(which='both', alpha = 0.5)
r2 = r2_score(obs_AWLN_2020['Head (m)'], sim_AWLN_2020['Head (m)']).round(2)
# plt.text(118.2,124,'$\mathregular{r^2}$ = '+str(r2), fontsize = 18)
#     ax.legend(fontsize=14)
plt.savefig('output/crossplots_v2/awln-2020.png', bbox_inches='tight') 
plt.show()
plt.close()

#%% [4] cross-plot awln 2014
plt.rc('xtick', labelsize=18)
plt.rc('ytick', labelsize=18)
sim_AWLN_2014 = pd.read_csv(f'../../final_deliverables/Head_AWLN/bore_sample_output_AWLN_2014.dat',names = ["WELL_NAME", "Date","Time", "Head (m)"],delimiter="   ")
obs_AWLN_2014 = pd.read_csv(f'../../final_deliverables/Head_AWLN/Bore_Sample_File_in_model_AWLN_2014.csv',names = ["WELL_NAME", "Date","Time", "Head (m)"],delimiter=",")

obs_AWLN_2014 = obs_AWLN_2014[obs_AWLN_2014['WELL_NAME'] != '182B-mon']
obs_AWLN_2014 = obs_AWLN_2014[obs_AWLN_2014['WELL_NAME'] != '199-B4-16']
sim_AWLN_2014 = sim_AWLN_2014[sim_AWLN_2014['WELL_NAME'] != '182B-MON']
sim_AWLN_2014 = sim_AWLN_2014[sim_AWLN_2014['WELL_NAME'] != '199-B4-16']

fig, ax = plt.subplots(nrows=1, ncols = 1, figsize=(10,10)) 
ax.plot(obs_AWLN_2014['Head (m)'],sim_AWLN_2014['Head (m)'] , 'o', markerfacecolor="steelblue", markeredgecolor='blue', markeredgewidth=1,markersize=10, alpha =0.5, zorder=1)
ax.plot([0, 1], [0, 1], color='red', linewidth=0.5, transform=ax.transAxes, zorder=10)
ax.set_ylim(118,124.5)
ax.set_xlim(118,124.5)

#     ax.set_title(well, fontsize=15, fontweight='bold')
ax.set_ylabel('Simulated Head 2012-2014', fontweight='bold', fontsize=18)
ax.set_xlabel('Observed Head 2012-2014', fontweight='bold', fontsize=18)
ax.grid(which='both', alpha = 0.5)
r2 = r2_score(obs_AWLN_2014['Head (m)'], sim_AWLN_2014['Head (m)']).round(2)
# plt.text(118.2,124,'$\mathregular{r^2}$ = '+str(r2), fontsize = 18)
#     ax.legend(fontsize=14)
# plt.savefig('output/crossplots/awln-2014.png', bbox_inches='tight') 
plt.show()
plt.close()


#%% [5] Colored plot AWLN 2020 indiivudal plots - three rows
plt.rc('xtick', labelsize=18)
plt.rc('ytick', labelsize=18)

# sim_AWLN_2020 = pd.read_csv(f'../../final_deliverables/Head_AWLN/bore_sample_output_AWLN.dat',names = ["WELL_NAME", "Date","Time", "Head (m)"],delimiter="   ")
sim_AWLN_2020 = pd.read_csv(f'../../hpham/100BC_Calibration_model/PEST_2012-2020/bore_sample_output_AWLN_v1.dat',names = ["WELL_NAME", "Date","Time", "Head (m)"],delimiter="   ")
# obs_AWLN_2020 = pd.read_csv(f'../../final_deliverables/Head_AWLN/Bore_Sample_File_in_model_AWLN.csv',names = ["WELL_NAME", "Date","Time", "Head (m)"],delimiter=",")
obs_AWLN_2020 = pd.read_csv(f'../../hpham/100BC_Calibration_model/PEST_2012-2020/Bore_Sample_File_in_model_AWLN_v1.csv',names = ["WELL_NAME", "Date","Time", "Head (m)"],delimiter=",")

color={'199-B2-14':'darkorange', '199-B3-47':'olive','199-B3-51':'gold','199-B4-7':'navy',
        '199-B4-14':'steelblue','199-B4-18':'limegreen','199-B5-6':'darkblue','199-B5-8':'brown','199-B8-6':'lightgreen',
        '199-B3-46':'magenta',  '199-B3-50':'cyan',
        '199-B4-8':'steelblue', '199-B4-16':'darkorchid', 
       '199-B5-1':'burlywood', '199-B5-13':'darkgrey', 
       '199-B8-9':'cornflowerblue', '199-B9-3':'darkgreen', '699-71-77':'lightpink'}
       
obs_AWLN_2020['color'] = obs_AWLN_2020['WELL_NAME'].map(color)
sim_AWLN_2020['color'] = sim_AWLN_2020['WELL_NAME'].map(color)


wells = obs_AWLN_2020['WELL_NAME'].unique().tolist()

lst_1 = ['199-B2-14',
 '199-B3-46',
 '199-B3-47',
 '199-B3-50',
 '199-B3-51',
 '199-B4-7']

lst_2 = [
 '199-B4-8',
 '199-B4-14',
 '199-B4-16',
 '199-B4-18',
 '199-B5-1',
 '199-B5-6']

lst_3 = [    
 '199-B5-8',
 '199-B5-13',
 '199-B8-6',
 '199-B8-9',
 '199-B9-3',
 '699-71-77']


fig, ax = plt.subplots(nrows=1, ncols=6, figsize=(30,5))
for i, well in enumerate(lst_1):
    df = obs_AWLN_2020[obs_AWLN_2020['WELL_NAME'] ==well]
    df2 = sim_AWLN_2020[sim_AWLN_2020['WELL_NAME'] == well]
    print(well)
    ax[i].plot(df['Head (m)'],df2['Head (m)'], 'o', color=df2['color'].unique()[0], markersize=7,  label = str(well)[4:]) #alpha = 0.9,
    ax[i].plot([0, 1], [0, 1], color='grey',  transform=ax[i].transAxes)
    ax[i].set_ylim(118,124.5)
    ax[i].set_xlim(118,124.5)
    ax[i].set_title(well, fontsize=15, fontweight='bold')
    # ax[i].legend(fontsize=18)
    # ax.set_ylabel('Simulated Head 2012-2020', fontweight='bold', fontsize=18)
    # ax.set_xlabel('Observed Head 2012-2020', fontweight='bold', fontsize=18)
    ax[i].grid(which='both', alpha = 0.5)
plt.savefig('output/crossplots_v2/awln-2020-v4_p1.png', bbox_inches='tight') 
plt.show()

fig, ax = plt.subplots(nrows=1, ncols=6, figsize=(30,5))
for i, well in enumerate(lst_2):
    df = obs_AWLN_2020[obs_AWLN_2020['WELL_NAME'] ==well]
    df2 = sim_AWLN_2020[sim_AWLN_2020['WELL_NAME'] == well]
    print(well)
    ax[i].plot(df['Head (m)'],df2['Head (m)'], 'o', color=df2['color'].unique()[0], markersize=7,  label = str(well)[4:]) #alpha = 0.9,
    ax[i].plot([0, 1], [0, 1], color='grey',  transform=ax[i].transAxes)
    ax[i].set_ylim(118,124.5)
    ax[i].set_xlim(118,124.5)
    ax[i].set_title(well, fontsize=15, fontweight='bold')
    # ax[i].legend(fontsize=18)
    # ax.set_ylabel('Simulated Head 2012-2020', fontweight='bold', fontsize=18)
    # ax.set_xlabel('Observed Head 2012-2020', fontweight='bold', fontsize=18)
    ax[i].grid(which='both', alpha = 0.5)
plt.savefig('output/crossplots_v2/awln-2020-v4_p2.png', bbox_inches='tight') 
plt.show()

fig, ax = plt.subplots(nrows=1, ncols=6, figsize=(30,5))
for i, well in enumerate(lst_3):
    df = obs_AWLN_2020[obs_AWLN_2020['WELL_NAME'] ==well]
    df2 = sim_AWLN_2020[sim_AWLN_2020['WELL_NAME'] == well]
    print(well)
    ax[i].plot(df['Head (m)'],df2['Head (m)'], 'o', color=df2['color'].unique()[0], markersize=7,  label = str(well)[4:]) #alpha = 0.9,
    ax[i].plot([0, 1], [0, 1], color='grey',  transform=ax[i].transAxes)
    ax[i].set_ylim(118,124.5)
    ax[i].set_xlim(118,124.5)
    ax[i].set_title(well, fontsize=15, fontweight='bold')
    # ax[i].legend(fontsize=18)
    # ax.set_ylabel('Simulated Head 2012-2020', fontweight='bold', fontsize=18)
    # ax.set_xlabel('Observed Head 2012-2020', fontweight='bold', fontsize=18)
    ax[i].grid(which='both', alpha = 0.5)
plt.savefig('output/crossplots_v2/awln-2020-v4_p3.png', bbox_inches='tight') 
plt.show()

#%% [6] Plot residuals
plt.rc('xtick', labelsize=18)
plt.rc('ytick', labelsize=18)
sim_AWLN_2020 = pd.read_csv(f'../../final_deliverables/Head_AWLN/bore_sample_output_AWLN.dat',names = ["WELL_NAME", "Date","Time", "Head (m)"],delimiter="   ")
obs_AWLN_2020 = pd.read_csv(f'../../final_deliverables/Head_AWLN/Bore_Sample_File_in_model_AWLN.csv',names = ["WELL_NAME", "Date","Time", "Head (m)"],delimiter=",")


color={'199-B2-14':'darkorange', '199-B3-47':'olive','199-B3-51':'gold','199-B4-7':'navy',
        '199-B4-14':'steelblue','199-B4-18':'limegreen','199-B5-6':'darkblue','199-B5-8':'brown','199-B8-6':'lightgreen',
        '199-B3-46':'magenta',  '199-B3-50':'cyan',
        '199-B4-8':'steelblue', '199-B4-16':'darkorchid', 
       '199-B5-1':'burlywood', '199-B5-13':'darkgrey', 
       '199-B8-9':'cornflowerblue', '199-B9-3':'darkgreen', '699-71-77':'lightpink'}
       
obs_AWLN_2020['color'] = obs_AWLN_2020['WELL_NAME'].map(color)
sim_AWLN_2020['color'] = sim_AWLN_2020['WELL_NAME'].map(color)


wells = obs_AWLN_2020['WELL_NAME'].unique().tolist()

for i, well in enumerate(wells):
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10,5))
    df = obs_AWLN_2020[obs_AWLN_2020['WELL_NAME'] ==well]
    df['Date'] = pd.to_datetime(df['Date'])
    df2 = sim_AWLN_2020[sim_AWLN_2020['WELL_NAME'] == well]

    print(df['Date'])
    ax.plot(df['Date'],df['Head (m)'] - df2['Head (m)'], 'o-', linewidth=2, markersize=5, 
                     color='steelblue', label = str(well), zorder=10)
    ax.axvline(x=pd.to_datetime('2014-07-31'), color = 'r', zorder=2)
    ax.axhline(y=0, color = 'grey', zorder=1, alpha = 0.5)
    ax.set_ylim(-1.06,1.01)
    ax.set_xlim(pd.to_datetime('2012-01-01'),pd.to_datetime('2020-09-30'))
    # ax.set_title(well, fontsize=15, fontweight='bold')
    ax.legend(fontsize=18)
    ax.set_ylabel('Residual (m)', fontweight='bold', fontsize=18)
    ax.set_xlabel('Date', fontweight='bold', fontsize=18)
    ax.grid(which='both', alpha = 0.5)
    # plt.savefig('output/crossplots/awln_residual_' + well+'.png', bbox_inches='tight') 
plt.show()

#%% [7] Compute mean error, RMSE, mean absolute error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error

sim_AWLN_2020 = pd.read_csv(f'../../final_deliverables/Head_AWLN/bore_sample_output_AWLN.dat',names = ["WELL_NAME", "Date","Time", "Head (m)"],delimiter="   ")
obs_AWLN_2020 = pd.read_csv(f'../../final_deliverables/Head_AWLN/Bore_Sample_File_in_model_AWLN.csv',names = ["WELL_NAME", "Date","Time", "Head (m)"],delimiter=",")
wells = obs_AWLN_2020['WELL_NAME'].unique().tolist()
obs_AWLN_2020['Date'] = pd.to_datetime(obs_AWLN_2020['Date'])
sim_AWLN_2020['Date'] = pd.to_datetime(sim_AWLN_2020['Date'])

cutoff_date = datetime(2014, 7, 31)
l1,l2,l3,l4,l5,l6,l7 = [],[],[],[],[],[],[]
for i, well in enumerate(wells):
    print(well)
    df = obs_AWLN_2020[obs_AWLN_2020['WELL_NAME'] ==well]
    df2 = sim_AWLN_2020[sim_AWLN_2020['WELL_NAME'] == well]
    
    # Calculate RMSE 2012-2014 

    df3 = df[df['Date'] <= cutoff_date]['Head (m)']
    df4 = df2[df2['Date'] <= cutoff_date]['Head (m)']

    if df3.shape[0] > 0:
        rmse12_14 = round(np.sqrt(mean_squared_error(df3, df4)), 2)
        mae12_14 = round(mean_absolute_error(df3, df4), 2)
        me12_14 = round(mean_squared_error(df3, df4), 2)
    else:
        rmse12_14 = 'NaN'
        mae12_14 = 'NaN'
        me12_14 = 'NaN'
    print(rmse12_14)

    # Calculate RMSE 2012-2020
    if df.shape[0] > 0:
        rmse12_20 = round(np.sqrt(mean_squared_error(df['Head (m)'], df2['Head (m)'])), 2)
        mae12_20 = round(mean_absolute_error(df['Head (m)'], df2['Head (m)']), 2)
        me12_20 = round(mean_squared_error(df['Head (m)'], df2['Head (m)']), 2)
    else:
        rmse12_20 = 'NaN'
        mae12_20 = 'NaN'
        me12_20 = 'NaN'
    print(rmse12_20)
    l1.append(well)
    l2.append(rmse12_14)
    l3.append(rmse12_20)
    l4.append(mae12_14)
    l5.append(mae12_20)
    l6.append(me12_14)
    l7.append(me12_20)
    
df_lst = pd.DataFrame(
    {'well': l1,
     'root mean square error 2014': l2,
     'root mean square error 2020': l3,
     'mean absolute eror 2014': l4,
     'mean absolute error 2020': l5,
     'mean sq eror 2014': l6,
     'mean sq error 2020': l7
    })
# df_lst.to_csv('output/stats_awln.csv')

