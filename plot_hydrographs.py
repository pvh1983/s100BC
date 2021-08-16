import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from datetime import datetime, date, time

# cd c:\Users\hpham\OneDrive - INTERA Inc\projects\020_100BC\hpham\scripts\
'''
1. Run get_continuous_awln.bat to get new simulated head data for AWLN
2. 

'''


def read_file(ifile, delimiter_):
    cols = ['Well Name', 'Date', 'Time', 'Groundwater level (m)']
    # Read

    df = pd.read_csv(ifile, delimiter=delimiter_,
                     skipinitialspace=True, names=cols)
    df['Date'] = pd.to_datetime(df['Date'])
    return df


def read_data(obs_type):
    if obs_type == 'AWLN':
        # 2012-2014 model
        # ip1214 = f'../100BC_Calibration_model/slave_2012_2014/'  # path to file
        ip1214 = f'../../final_deliverables/Head_{obs_type}/'
        df0obs = read_file(
            f'{ip1214}/Bore_Sample_File_in_model_{obs_type}.csv', ',')

        ip1214 = f'../100BC_Calibration_model/slave_2012_2014/'
        df0sim = read_file(
            f'{ip1214}/bore_sample_output_{obs_type}.dat', ' ')

        # 2012-2020 model (continuouse_data, including -9999)
        #ip1220 = f'../100BC_Calibration_model/slave_2012_2020/'
        ip1220 = f'../../final_deliverables/Head_{obs_type}/continuous {obs_type}/'
        old_parameter = False
        if old_parameter:
            df1sim = read_file(
                f'{ip1220}/bore_sample_output_{obs_type}_v2.dat', ' ')
        else:
            # ip1220_new = f'../100BC_Calibration_model/PEST_2012-2020/run4_opt6th/'  # 111 pars
            # ip1220_new = f'../100BC_Calibration_model/PEST_2012-2020/run5_5par_new/' # 5 pars
            # ip1220_new = f'../100BC_Calibration_model/PEST_2012-2020/master_run6_4newpar/'  # 4 hk pp only
            # 6 pars (4hk, 1riv_cond, 1 Right ghb)
            #ip1220_new = f'../100BC_Calibration_model/PEST_2012-2020/master_run6_4newpar/'
            # master_run8_5newpar_no_riv_cond: 4hk, 1 ghb, 3 wells only [no new par for riv cond]
            ip1220_new = f'../100BC_Calibration_model/PEST_2012-2020/master_run8_5newpar_no_riv_cond/'

            df1sim = read_file(
                f'{ip1220_new}/bore_sample_output_{obs_type}.dat', ' ')  # re-cali, 4 iterations

        df1obs = read_file(
            f'{ip1220}/Bore_Sample_File_in_model_{obs_type}_v2.csv', ',')

        # if obs_type == 'AWLN':
        ip1220 = f'../../final_deliverables/Head_{obs_type}/'
        ifile = f'{ip1220}/Bore_Sample_File_in_model_{obs_type}.csv'
        df2obs = read_file(ifile, ',')
    # else:
        #    ip1220 = f'../100BC_Calibration_model/slave_2012_2020/'
        #    df2obs = read_file(  # obs not including -9999 values
        #        f'{ip1220}/Bore_Sample_File_in_model_{obs_type}_no9999.csv', ',')

        df2obs['2012-2020 Obs. GWL (m)'] = df2obs['Groundwater level (m)']
        df2obs = df2obs[df2obs['2012-2020 Obs. GWL (m)'] != -9999]

    else:  # 'manual'
        # 2012-2014 model
        # ip1214 = f'../100BC_Calibration_model/slave_2012_2014/'  # path to file

        ip1214 = f'../../final_deliverables/Head_{obs_type}/continuous_manual/'
        #ip1214 = f'../100BC_Calibration_model/slave_2012_2014/'
        df0obs = read_file(
            f'{ip1214}/Bore_Sample_File_in_model_{obs_type}_v4.csv', ',')

        ip1214 = f'../100BC_Calibration_model/slave_2012_2014/'
        df0sim = read_file(
            f'{ip1214}/bore_sample_output_{obs_type}_2014.dat', ' ')

        # 2012-2020 model
        #ip1220 = f'../100BC_Calibration_model/slave_2012_2020/'
        ip1220 = f'../../final_deliverables/Head_{obs_type}/'
        df1sim = read_file(
            f'{ip1220}/continuous_manual/bore_sample_output_{obs_type}_v2.dat', ' ')
        df1obs = read_file(
            f'{ip1220}/continuous_manual/Bore_Sample_File_in_model_{obs_type}_v4.csv', ',')

        # if obs_type == 'AWLN':
        ip1220 = f'../../final_deliverables/Head_{obs_type}/'
        ifile = f'{ip1220}/Bore_Sample_File_in_model_{obs_type}.csv'
        df2obs = read_file(ifile, ',')
        # else:
        #    ip1220 = f'../100BC_Calibration_model/slave_2012_2020/'
        #    df2obs = read_file(  # obs not including -9999 values
        #        f'{ip1220}/Bore_Sample_File_in_model_{obs_type}_no9999.csv', ',')

        df2obs['2012-2020 Obs. GWL (m)'] = df2obs['Groundwater level (m)']
        df2obs = df2obs[df2obs['2012-2020 Obs. GWL (m)'] != -9999]

    # Create a new df for 2012-2014 data
    df1214 = pd.DataFrame()
    df1214['Date'] = df0sim['Date']
    df1214['Well Name'] = df0sim['Well Name']
    df1214['2012-2014 Obs. GWL (m)'] = df0obs['Groundwater level (m)']
    df1214['2012-2014 Sim. GWL (m)'] = df0sim['Groundwater level (m)']

    # Create a new df for 2012-2020 data
    df1220 = pd.DataFrame()
    df1220['Date'] = df1obs['Date']
    df1220['Well Name'] = df1obs['Well Name']
    df1220['2012-2020 Obs. GWL (m)'] = df1obs['Groundwater level (m)']
    df1220['2012-2020 Sim. GWL (m)'] = df1sim['Groundwater level (m)']
    return df1214, df1220, df2obs


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


def plot_line(df1214, df1220, df2obs, wname, xmin, ymin, xmax, ymax, obs_type):
    print(f'\nRunning plot_line, well {wname} ...\n')
    cutoff_date = datetime(2014, 7, 31)
    df1214 = df1214[df1214['2012-2014 Obs. GWL (m)'] != -9999]
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(
        8, 5), sharex=True, sharey=True)
    plt.grid(color='#e6e6e6', linestyle='-',
             linewidth=0.5, axis='both', alpha=0.1)
    df2 = df1220[df1220['Well Name'] == wname]
    print(f'df2 shape = {df2.shape}')

    #df2obs_filter = df2obs[df2obs['Well Name'] == wname]
    #print(f'df2obs_filter shape = {df2obs_filter.shape}')
    if df2.shape[0] > 0:

        # SP separation line
        ax.plot([cutoff_date, cutoff_date], [ymin, ymax], '--r', alpha=0.7)

        # Add river stage
        ifile_river_stage = f'../../final_deliverables/Boundary_Conditions/genRIV_version4/RIV_stage_vs_time_2012-2020.csv'
        df_riv = pd.read_csv(ifile_river_stage)
        df_riv['date'] = pd.to_datetime(df_riv['date'])

        # Plot sp ave data
        df_riv.plot(ax=ax, x='date', y='average_stage',
                    style=['-'], alpha=0.6, linewidth=1., label='River Stage (m)')

        '''
        # resample to monthly ave
        df_riv_m = df_riv.resample('m', on='date').mean()
        df_riv_m.rename(
            columns={'average_stage': 'Monthly Ave. B-gage Stage'}, inplace=True)
        df_riv_m = df_riv_m.reset_index()
        df_riv_m.plot(ax=ax, x='date', y='Monthly Ave. B-gage Stage',
                      style=['--x'], markersize=3, alpha=0.5, linewidth=1.)
        '''
        # [Solid line 1] 2012 - 2014 simulated heads
        df2.Date = pd.to_datetime(df2.Date)
        df2.plot(ax=ax, x='Date', y='2012-2020 Sim. GWL (m)',
                 alpha=0.9)
        print(f'df 2012-2020: \n \n {df2.head()} \n')

        # Calculate RMSE 2012-2014 (get rid of -9999 rows)
        df3 = df2[df2['2012-2020 Obs. GWL (m)'] != -9999]
        hobs = df3[df3['Date'] <= cutoff_date]['2012-2020 Obs. GWL (m)']
        hsim = df3[df3['Date'] <= cutoff_date]['2012-2020 Sim. GWL (m)']
        # print(hobs.shape)
        # print(hsim.shape)
        if hobs.shape[0] > 0:
            rmse1214 = round(np.sqrt(mean_squared_error(hobs, hsim)), 2)
        else:
            rmse1214 = 'NaN'

        # Calculate RMSE 2012-2020

        hobs_all = df3['2012-2020 Obs. GWL (m)']
        hsim_all = df3['2012-2020 Sim. GWL (m)']
        if hobs_all.shape[0] > 0:
            rmse1220 = round(
                np.sqrt(mean_squared_error(hobs_all, hsim_all)), 2)
        else:
            rmse1220 = 'NaN'

        #

        # [Solid line 2 ] Plot old 2012 - 2014 sim results
        #df1 = df1214[df1214['Well Name'] == wname]
        #df1.Date = pd.to_datetime(df1.Date)
        #print(f'df1214: \n \n {df1} \n')
        # df1.plot(ax=ax, x='Date', y='2012-2014 Sim. GWL (m)',
        #         style='--', alpha=0.9)

        # Plot obs data -------------------------------------------------------
        # df2.plot(ax=ax, x='Date', y='2012-2020 Obs. GWL (m)',
        #         style=['o'], markersize=3, alpha=0.35)

        # [Scatterd plot o] 2012 - 2020 observations
        #df2obs_filter.Date = pd.to_datetime(df2obs_filter.Date)
        df2.plot(ax=ax, x='Date', y='2012-2020 Obs. GWL (m)',
                 style=['o'], markersize=3, alpha=0.5)
        print(f'df2: \n \n {df2} \n')

        ax.set_ylim([ymin, ymax])
        ax.set_xlim([xmin, xmax])
        ax.set_title(
            f'{wname}, RMSE1214={rmse1214} m, RMSE1220={rmse1220} m')
        ax.set_ylabel('Water level (m)')
        ax.set_xlabel('Calendar Year')
        ax.grid()

        # save fig
        ofile = f'output/Sim_GWL_{obs_type}_{wname}_with_riv_stage.png'
        fig.savefig(ofile, dpi=300, transparent=False, bbox_inches='tight')
        print(f'{wname}, RMSEs = {rmse1214}, {rmse1220}')
        print(f'Save {ofile}\n')
    else:
        rmse1214, rmse1220 = ['NaN', 'NaN']
    return rmse1214, rmse1220


if __name__ == "__main__":
    for obs_type in ['AWLN']:  # 'AWLN' vs. 'manual'
        if obs_type == 'AWLN':
            xmin, ymin, xmax, ymax = [118, 118, 128, 128]
        elif obs_type == 'manual':
            xmin, ymin, xmax, ymax = [118, 118, 124, 124]

        # [00] Reading data -------------------------------------------------------
        df1214, df1220, df2obs = read_data(obs_type)
        # Column names
        opt_obs_sim_scatter_plot = False
        opt_valid_sim = True  # Compare Sim. 2012-2014 vs 2012-2020

        #

        cols2plt = [
            '2012-2014 Sim. GWL (m)', '2012-2020 Sim. GWL (m)']

        if opt_valid_sim:
            xmin = cutoff_date = datetime(2012, 1, 1)
            xmax = cutoff_date = datetime(2020, 9, 30)
            list_wells = df1220['Well Name'].unique()
            df_fit = pd.DataFrame(
                columns=['Well Name', 'RMSE1214 (m)', 'RMSE1220 (m)'])
            df_fit['Well Name'] = list_wells
            for wname in list_wells:
                # for wname in ['199-B3-46']:
                #print(f'WName = {wname}\n')
                rmse1214, rmse1220 = plot_line(
                    df1214, df1220, df2obs, wname, xmin, ymin, xmax, ymax, obs_type)

                df_fit['RMSE1214 (m)'][df_fit['Well Name'] == wname] = rmse1214
                df_fit['RMSE1220 (m)'][df_fit['Well Name'] == wname] = rmse1220
            # save fitting
            df_fit.to_csv(f'output/rmse_{obs_type}.csv')

        if opt_obs_sim_scatter_plot:
            xp = '2012-2014 Obs. GWL (m)'  # col to plot
            yp = '2012-2014 Sim. GWL (m)'  # col to plot
            ofile = f'output/check_scatter_obs_sim_{obs_type}.png'

            # get cols to plot
            if obs_type == 'AWLN':
                col2plt = ['199-B2-14', '199-B3-47', '199-B3-51', '199-B4-7',
                           '199-B4-14',  '199-B4-18', '199-B5-6',  # '199-B4-16'
                           '199-B5-8', '199-B8-6']  # '182B-mon'
                df2plot = pd.DataFrame()
                for i in col2plt:
                    df2plot = pd.concat(
                        [df2plot, df1214[df1214['Well Name'] == i]], axis=0)
            else:
                df2plot = df1214.copy()
                df2plot = df2plot[df2plot['2012-2014 Obs. GWL (m)'] != -9999]
                df2plot = df2plot[df2plot.Date <= datetime(2014, 7, 31)]
            plot_scatter(xp, yp, df2plot, ofile, xmin,
                         ymin, xmax, ymax, obs_type)
