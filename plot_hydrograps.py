import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error

# cd c:\Users\hpham\OneDrive - INTERA Inc\projects\020_100BC\hpham\scripts\


def read_file(ifile, delimiter_):
    cols = ['Well Name', 'Date', 'Time', 'Groundwater level (m)']
    # Read

    df = pd.read_csv(ifile, delimiter=delimiter_,
                     skipinitialspace=True, names=cols)
    df['Date'] = pd.to_datetime(df['Date'])
    return df


def plot_scatter(xp, yp, df, ofile, xmin, ymin, xmax, ymax, obs_type):
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(
        6, 6), sharex=True, sharey=True)
    plt.grid(color='#e6e6e6', linestyle='-', linewidth=0.5, axis='both')
    df.plot.scatter(ax=ax, x=xp, y=yp, alpha=0.6)
    ax.set_xlim([xmin, xmax])
    ax.set_ylim([ymin, ymax])
    ax.set_title(f'Observation network: {obs_type}')
    # Add a diag line
    ax.plot([119, 124], [119, 124], 'r', alpha=0.6)

    ax.grid()
    # Save figure (to have scale bar)
    fig.savefig(ofile, dpi=300, transparent=False, bbox_inches='tight')
    print(f'Saved Cdiff at: {ofile}')


def plot_line(df1214, df1220, wname):
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(
        6, 6), sharex=True, sharey=True)
    df1 = df1214[df1214['Well Name'] == wname]
    df1.plot(ax=ax, x='Date', y='2012-2014 Sim. GWL (m)', alpha=0.8)

    df2 = df1220[df1220['Well Name'] == wname]
    df2.plot(ax=ax, x='Date', y='2012-2020 Sim. GWL (m)',
             style=[':'], alpha=0.8)

    # Calculate RMSE
    h1 = df1['2012-2014 Sim. GWL (m)']
    h2 = df2['2012-2020 Sim. GWL (m)']
    rmse = round(np.sqrt(mean_squared_error(h1, h2)), 4)

    ax.set_title(f'{wname}, RMSE={rmse} m')
    ofile = f'output/check_gwlevels_{wname}.png'
    fig.savefig(ofile, dpi=300, transparent=False, bbox_inches='tight')
    print(f'Save {ofile}\n')


def read_data(obs_type):

    # 2012-2014 model
    ip1214 = f'../100BC_Calibration_model/slave_2012_2014/'  # path to file
    df0obs = read_file(
        f'{ip1214}/Bore_Sample_File_in_model_{obs_type}.csv', ',')
    df0sim = read_file(
        f'{ip1214}/bore_sample_output_{obs_type}.dat', ' ')

    # 2012-2020 model
    ip1220 = f'../100BC_Calibration_model/slave_2012_2020/'
    df1obs = read_file(
        f'{ip1220}/Bore_Sample_File_in_model_{obs_type}.csv', ',')
    df1sim = read_file(f'{ip1220}/bore_sample_output_{obs_type}.dat', ' ')

    # Create a new df for 2012-2014 data
    df1214 = pd.DataFrame()
    df1214['Date'] = df0obs['Date']
    df1214['Well Name'] = df0obs['Well Name']
    df1214['2012-2014 observed GWL (m)'] = df0obs['Groundwater level (m)']
    df1214['2012-2014 Sim. GWL (m)'] = df0sim['Groundwater level (m)']

    # Create a new df for 2012-2020 data
    df1220 = pd.DataFrame()
    df1220['Date'] = df1obs['Date']
    df1220['Well Name'] = df1obs['Well Name']
    df1220['2012-2020 observed GWL (m)'] = df1obs['Groundwater level (m)']
    df1220['2012-2020 Sim. GWL (m)'] = df1sim['Groundwater level (m)']
    return df1214, df1220


if __name__ == "__main__":

    obs_type = 'manual'  # 'AWLN' vs. 'manual'

    # [00] Reading data -------------------------------------------------------
    df1214, df1220 = read_data(obs_type)
    # Column names
    opt_obs_sim_scatter_plot = False
    opt_valid_sim = True  # Compare Sim. 2012-2014 vs 2012-2020

    #

    cols2plt = [
        '2012-2014 Sim. GWL (m)', '2012-2020 Sim. GWL (m)']

    if opt_valid_sim:
        list_wells = df1214['Well Name'].unique()
        for wname in list_wells:
            plot_line(df1214, df1220, wname)

    if opt_obs_sim_scatter_plot:
        xp = '2012-2014 observed GWL (m)'  # col to plot
        yp = '2012-2014 Sim. GWL (m)'  # col to plot
        ofile = f'output/check_scatter_obs_sim_{obs_type}.png'

        # get cols to plot
        col2plt = ['199-B2-14', '199-B3-47', '199-B3-51', '199-B4-7',
                   '199-B4-14',  '199-B4-18', '199-B5-6',  # '199-B4-16'
                   '199-B5-8', '199-B8-6']  # '182B-mon'
        df2plot = pd.DataFrame()
        for i in col2plt:
            df2plot = pd.concat(
                [df2plot, df1214[df1214['Well Name'] == i]], axis=0)
        if obs_type == 'AWLN':
            xmin, ymin, xmax, ymax = [119, 119, 124, 124]
        elif obs_type == 'manual':
            xmin, ymin, xmax, ymax = [118, 118, 124, 124]

        plot_scatter(xp, yp, df2plot, ofile, xmin, ymin, xmax, ymax, obs_type)
