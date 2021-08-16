# -*- coding: utf-8 -*-
"""
Created on Thu May  3 14:47:48 2021

@author: MPedrazas
"""

import pandas as pd;
import os;
import platform;
import numpy as np;
import matplotlib.pyplot as plt
from datetime import datetime, date, time
import numpy as np
import flopy.utils.binaryfile as bf
import matplotlib.cm as cm
from matplotlib.colors import BoundaryNorm, Normalize, LinearSegmentedColormap
from mpl_toolkits.axes_grid1 import make_axes_locatable
# import geopandas as gpd
import datetime as dt


plt.rc('xtick', labelsize=12)
plt.rc('ytick', labelsize=12)

def plot_obs(ifile_loc, plt_id, dfObs):
    dfLoc = pd.read_csv(f'./input/{ifile_loc}') 

    fig, ax = plt.subplots(nrows=2, ncols=4, figsize=(16, 9), sharex=True, sharey=False)
    fig_axes = [fig.axes[i-1] for i in plt_id]
    # selected subplot
    for k, ax in enumerate(fig_axes):
        print(k)
        wname = dfLoc['Name'].iloc[k]
        ir, ic, ilay = dfLoc['i'].iloc[k], dfLoc['j'].iloc[k], dfLoc['k'].iloc[k]
        
        dfObsSite = dfObs[dfObs['SAMP_SITE_NAME'] == wname]
        # print(dfObsSite.columns)

        dfObsSite.plot(ax=ax, x='SAMP_DATE', y='STD_VALUE_RPTD',
                    style=['--'], linewidth=0.5,  c = "darkorange", alpha=0.9, legend=False)
        ax.scatter(dfObsSite['SAMP_DATE'],dfObsSite['STD_VALUE_RPTD'], s=15,
                   c = "darkorange", alpha=0.9)

        if wname == '199-B4-14' or wname == '199-B5-10':
            ax.set_ylim([0, 180])
        else:
            ax.set_ylim([0, 100])
        ax.set_xlim([dt.datetime(2012, 1, 1),
                 dt.datetime(2020, 9, 29)])
        ax.set_title(wname)
        ax.set_ylabel('Cr (ug/L)')
        ax.set_xlabel('Time (years)')
    
        # Turn on the minor TICKS, which are required for the minor GRID
        ax.minorticks_on()
    
        # Customize the major grid
        ax.grid(which='major', linestyle='-',
                linewidth='0.1', color='red')
    
        # Customize the minor grid
        ax.grid(which='minor', linestyle=':',
                linewidth='0.1', color='black')
# save fig
    # ofile = 'output/Cr_figures/Cr_obs_new_figs/Conc_obs_{}.png'.format(ifile_loc[:-4])
    # fig.savefig(ofile, dpi=300, transparent=False, bbox_inches='tight')
    # print(f'Saved {ofile}\n')
    
    return fig, ax
    
if __name__ == "__main__":

    # Get observed Cr(IV) concentration -------------------------------
    dfObs = pd.read_csv(r"C:\Users\MPedrazas\OneDrive - INTERA Inc\020_100BC\final_deliverables\Cr_obs_ALL\Cr_obs_avg_dups_rev.csv")
    dfObs['SAMP_DATE'] = pd.to_datetime(dfObs['SAMP_DATE'])
    
    # Generate both time series
    # list_loc = ['AWLN_shallow_wells1.csv','AWLN_shallow_wells2.csv', 'AWLN_deep_wells.csv']
    list_loc = ['AWLN_shallow_wells_near116B11.csv']
    dic_id = {'AWLN_shallow_wells1.csv': [1, 4, 5, 8, 9, 10, 11, 12],
              'AWLN_shallow_wells2.csv': [1, 4, 5, 8, 9, 10, 11, 12],
              'AWLN_deep_wells.csv': [1, 4, 5, 8, 9, 10, 11, 12],
              'AWLN_shallow_wells_near116B11.csv': [1, 4, 5, 8]}
    for ifile_loc in list_loc:
        print(f'\n\n ifile_loc = {ifile_loc}\n')
        plot_obs(ifile_loc, dic_id[ifile_loc], dfObs)
