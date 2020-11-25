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

#%% cross-plot man 2020
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
plt.text(118.2,123.5,'$\mathregular{r^2}$ = '+str(r2), fontsize = 18)
#     ax.legend(fontsize=14)
plt.savefig('output/crossplots/man-2020.png', bbox_inches='tight') 
plt.show()
plt.close()
#%% cross-plot man 2014
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
plt.text(118.2,123.5,'$\mathregular{r^2}$ = '+str(r2), fontsize = 18)
#     ax.legend(fontsize=14)
plt.savefig('output/crossplots/man-2014.png', bbox_inches='tight') 
plt.show()
plt.close()
#%% cross-plot awln  2020
plt.rc('xtick', labelsize=18)
plt.rc('ytick', labelsize=18)
sim_AWLN_2020 = pd.read_csv(f'../../final_deliverables/Head_AWLN/bore_sample_output_AWLN.dat',names = ["WELL_NAME", "Date","Time", "Head (m)"],delimiter="   ")
obs_AWLN_2020 = pd.read_csv(f'../../final_deliverables/Head_AWLN/Bore_Sample_File_in_model_AWLN.csv',names = ["WELL_NAME", "Date","Time", "Head (m)"],delimiter=",")

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
plt.text(118.2,124,'$\mathregular{r^2}$ = '+str(r2), fontsize = 18)
#     ax.legend(fontsize=14)
plt.savefig('output/crossplots/awln-2020.png', bbox_inches='tight') 
plt.show()
plt.close()

#%% cross-plot awln 2014
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
plt.text(118.2,124,'$\mathregular{r^2}$ = '+str(r2), fontsize = 18)
#     ax.legend(fontsize=14)
plt.savefig('output/crossplots/awln-2014.png', bbox_inches='tight') 
plt.show()
plt.close()

#%% Colored plot to reproduce MPR figure...in progress...
# plt.rc('xtick', labelsize=18)
# plt.rc('ytick', labelsize=18)
# disc_sim_MAN_2014 = pd.read_csv(os.path.join(outputdir,"hydrographs","2012-2014","bore_sample_output_AWLN.dat"),names = ["WELL_NAME", "Date","Time", "Head (m)"],delimiter="   ")
# obs_MAN_2014 = pd.read_csv(os.path.join(outputdir,"hydrographs","2012-2014","Bore_Sample_File_in_model_AWLN.csv"),names = ["WELL_NAME", "Date","Time", "Head (m)"],delimiter=",")

# obs_MAN_2014 = obs_MAN_2014[obs_MAN_2014['WELL_NAME'] != '182B-mon']
# obs_MAN_2014 = obs_MAN_2014[obs_MAN_2014['WELL_NAME'] != '199-B4-16']
# disc_sim_MAN_2014 = disc_sim_MAN_2014[disc_sim_MAN_2014['WELL_NAME'] != '182B-MON']
# disc_sim_MAN_2014 = disc_sim_MAN_2014[disc_sim_MAN_2014['WELL_NAME'] != '199-B4-16']

# color={'199-B2-14':'darkorange', '199-B3-47':'olive','199-B3-51':'gold','199-B4-7':'navy',
#         '199-B4-14':'steelblue','199-B4-18':'limegreen','199-B5-6':'darkblue','199-B5-8':'brown','199-B8-6':'lightgreen'}
# obs_MAN_2014['color'] = obs_MAN_2014['WELL_NAME'].map(color)
# disc_sim_MAN_2014['color'] = disc_sim_MAN_2014['WELL_NAME'].map(color)

# fig, ax = plt.subplots(nrows=1, ncols = 1, figsize=(10,10))  #15,10
# wells = obs_MAN_2014['WELL_NAME'].unique().tolist()
# for well in wells:
#     df = obs_MAN_2014[obs_MAN_2014['WELL_NAME'] == well]
#     df2 = disc_sim_MAN_2014[disc_sim_MAN_2014['WELL_NAME'] == well]
#     #ax.scatter(df['Head (m)'],df2['Head (m)'] , c=df2['color'], s=50, alpha = 0.8, label = str(well)[4:])
#     ax.plot(obs_MAN_2014['Head (m)'],disc_sim_MAN_2014['Head (m)'] , 'o', alpha = 0.5, markerfacecolor="steelblue", markeredgecolor='blue', markeredgewidth=1,markersize=10)
#     #ax.legend(fontsize=18)
#     ax.plot([0, 1], [0, 1], color='red', transform=ax.transAxes)
#     ax.set_ylim(119,124)
#     ax.set_xlim(119,124)
#     #ax.set_title(well, fontsize=15, fontweight='bold')
#     ax.set_ylabel('Simulated Head 2012-2014', fontweight='bold', fontsize=18)
#     ax.set_xlabel('Observed Head 2012-2014', fontweight='bold', fontsize=18)
#     ax.grid(which='both', alpha = 0.5)
#     plt.savefig('Figures_2020/crossplots/awln-2014-v2.png', bbox_inches='tight') 
# plt.show()
