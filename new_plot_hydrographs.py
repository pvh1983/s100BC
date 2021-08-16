# -*- coding: utf-8 -*-
"""
Created on Tue May 11 15:27:54 2021

@author: MPedrazas
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from datetime import datetime, date, time
import matplotlib.cm as cm
from matplotlib.colors import BoundaryNorm, Normalize, LinearSegmentedColormap
from mpl_toolkits.axes_grid1 import make_axes_locatable
import os

plt.rc('xtick', labelsize=12)
plt.rc('ytick', labelsize=12)

def read_file(ifile, delimiter_):
    cols = ['Well Name', 'Date', 'Time', 'Groundwater level (m)']
    # Read

    df = pd.read_csv(ifile, delimiter=delimiter_,
                     skipinitialspace=True, names=cols)
    df['Date'] = pd.to_datetime(df['Date'])
    return df

def calc_rms(sim,obs):
    obs_all = obs['Groundwater level (m)']
    sim_all = sim['Groundwater level (m)']
    if obs_all.shape[0] > 0:
        rmse1220 = round(np.sqrt(mean_squared_error(obs_all, sim_all)), 2)
    else:
        rmse1220 = 'NaN'
    return(rmse1220)

def get_stats(data,yp):
    min_val = min(data[yp])
    max_val = max(data[yp])
    mean_val = data[yp].mean()
    stat_lst = [min_val, max_val, mean_val]
    return stat_lst


stats,names = [],[]
for obs_type in ['manual','AWLN']:#['cell']:
    obs1220 = r'C:\Users\mpedrazas\OneDrive - INTERA Inc\020_100BC\mpedrazas\100BC_GWM\model_files\WLs_forSTOMP_obs'
    sim1220 = r'C:\Users\mpedrazas\OneDrive - INTERA Inc\020_100BC\mpedrazas\100BC_GWM\model_files\WLs_forSTOMP_sim'
    sim_cell = r'C:\Users\mpedrazas\OneDrive - INTERA Inc\020_100BC\mpedrazas\100BC_GWM\model_files\WLs_forSTOMP_sim_cell'

    df_obs = read_file(os.path.join(obs1220,'Bore_Sample_File_in_model_{}.csv'.format(obs_type)),',')
    df_sim = read_file(os.path.join(sim1220,'bore_sample_output_{}.dat'.format(obs_type)),' ')
    df_sim_at_obs = read_file(os.path.join(obs1220,'bore_sample_output_{}.dat'.format(obs_type)),' ')
    # df_sim_cell = read_file(os.path.join(sim_cell,'bore_sample_output_{}.dat'.format(obs_type)),' ')

    yp = 'Groundwater level (m)'
    xp = 'Date'
    
    xmin = datetime(2012, 1, 1)
    xmax = datetime(2020, 9, 30)
    ymin, ymax = 118,128
    
    well_lst = ['199-B3-47','199-B3-1', '199-B2-14', '199-B3-52']
    # well_lst = df_sim_cell['Well Name'].unique()
    # fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8, 6), sharex=True, sharey=True)
    for well in well_lst:
        dfs = df_sim[df_sim['Well Name'] == well]
        dfso = df_sim_at_obs[df_sim_at_obs['Well Name'] == well]
        dfo = df_obs[df_obs['Well Name'] == well]
        # dfc = df_sim_cell[df_sim_cell['Well Name'] == well]
        if len(dfo) > 0:
            print(well)
            rmse1220 = calc_rms(dfso,dfo)
            test = get_stats(dfs, yp) #getting stats for the simulated heads
            stats.append(test)
            names.append(f'{obs_type}_{well}')
            fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8, 6), sharex=True, sharey=True)
            ax.tick_params(labelsize=12, which = 'both')
            plt.grid(color='#e6e6e6', linestyle='-', linewidth=0.5, axis='both')
            dfo.plot.scatter(ax=ax, x=xp, y=yp, color ='green', alpha=1, label='Observed', s = 12)
            dfs.plot(ax=ax, x=xp, y=yp, color = 'darkorange', alpha = 1, label = 'Simulated', linewidth=1.5)
            # dfc.plot(ax=ax, x=xp, y=yp, alpha = 1, linewidth=1.5, label = well) #color = 'darkorange', label = 'Simulated',
            ax.set_xlim([xmin, xmax])
            ax.set_ylim([ymin, ymax])
            ax.set_title(f'{obs_type}: {well}  RMSE = {rmse1220}', fontsize='16') # RMSE = {rmse1220}
            ax.set_xlabel(xp,fontsize=14)
            ax.set_ylabel(yp, fontsize=14)
            # Turn on the minor TICKS, which are required for the minor GRID
            ax.minorticks_on()
        
            # Customize the major grid
            ax.grid(which='major', linestyle='-',linewidth='0.1', color='red')
        
            # Customize the minor grid
            ax.grid(which='minor', linestyle=':',linewidth='0.1', color='black')
            ax.legend()
            ofile = f'output/hydrographs_stomp/Sim_GWL_{obs_type}_{well}.png'
            fig.savefig(ofile, dpi=300, transparent=False, bbox_inches='tight')
    print(f'Saved Cdiff at: {ofile}')
    
df_stats = pd.DataFrame(stats, columns = ['Min', 'Max', 'Mean'])
df_stats['Name'] = names
df_stats = df_stats[['Name', 'Min','Max','Mean']]
# df_stats.to_csv('output/hydrographs_stomp/hydrograph_statistics_{}.csv'.format(obs_type), index=False)    


