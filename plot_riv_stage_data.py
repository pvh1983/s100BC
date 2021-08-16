import os
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt

plt.rc('xtick', labelsize=12)
plt.rc('ytick', labelsize=12)

def plot_ts_2rows(files, title, x, y, scatter_plot, colors):
    fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(16, 9), sharex=True, sharey=True)

    for i, file in enumerate(files.values()):
        file[x] = pd.to_datetime(file[x])
        if scatter_plot == True:
            ax[i].scatter(file[x], file[y], s=1,
                       c = colors[i], alpha=0.9, zorder=3)
        else:
            ax[i].plot(file[x], file[y], linewidth=1.5,
                       color=colors[i], alpha=0.9, zorder=3)
        ax[i].set_title(f'{title} {list(files.keys())[i]}', fontsize=14)
        ax[i].set_ylabel('River Stage (m)', fontsize=14)
        ax[i].set_xlabel('Time (years)', fontsize=14)
        # Customize the major grid
        ax[i].grid(which='major', linestyle='-',
                linewidth='0.1', color='red', zorder=2)
        ax[i].minorticks_on()
        # Customize the minor grid
        ax[i].grid(which='minor', linestyle='--',
                linewidth='0.1', color='black', zorder=1)
    plt.show()
    ofile = f'output/Riv_Stage_Comparison/{title}.png'
    fig.savefig(ofile, dpi=300, transparent=False, bbox_inches='tight')
    print(f'Saved {ofile}\n')
    plt.close()
    return None

def plot_ts_1fig(files, title, x, y, scatter_plot, ls, colors):
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(16, 5))

    for i, file in enumerate(files.values()):
        file[x] = pd.to_datetime(file[x])
        if scatter_plot == True:
            if list(files.keys())[i].endswith('2020'):
                ax.scatter(file[x], file[y], s=1, c = colors[i],
                            alpha=0.9, zorder=3, label = list(files.keys())[i])
            else:
                ax.scatter(file[x], file[y], s=1, c = colors[i],
                            alpha=0.9, zorder=4, label = list(files.keys())[i])
        else:
            ax.plot(file[x], file[y], linewidth=1.5, linestyle = ls[i], color = colors[i],
                    alpha=0.9, zorder=3, label = list(files.keys())[i])
    ax.set_title(f'{title}', fontsize=14)
    ax.legend()
    ax.set_ylabel('River Stage (m)', fontsize=14)
    ax.set_xlabel('Time (years)', fontsize=14)
    # Customize the major grid
    ax.grid(which='major', linestyle='-',
            linewidth='0.1', color='red', zorder=2)
    ax.minorticks_on()
    # Customize the minor grid
    ax.grid(which='minor', linestyle='--',
            linewidth='0.1', color='black', zorder=1)

    # plt.show()
    # ofile = f'output/Riv_Stage_Comparison/{title}_v2.png'
    # fig.savefig(ofile, dpi=300, transparent=False, bbox_inches='tight')
    # print(f'Saved {ofile}\n')
    plt.close()

    return None

def plot_ts_2rows_ccbyyear(dictionary, title, x, y, scatter_plot, ls):
    fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(16, 16), sharex=False, sharey=True)

    for i, file in enumerate(files.values()):
        file[x] = pd.to_datetime(file[x])
        grouped = file.groupby(file.date.dt.year)
        for key in grouped.groups.keys():
            grouped.get_group(key).plot(ax=ax[i], x = x, y = y,
                        linewidth=1.5,alpha=0.9, zorder=3, label = key)
        ax[0].set_title(f'{title}', fontsize=14)
        ax[i].set_ylabel('River Stage (m)', fontsize=14)
        ax[1].set_xlabel('Time (years)', fontsize=14)
        ax[0].set_xlabel('') #dum fix
        ax[i].legend(bbox_to_anchor=(1.05, 1))
        # Customize the major grid
        ax[i].grid(which='major', linestyle='-',
                linewidth='0.1', color='red', zorder=2)
        ax[i].minorticks_on()
        # Customize the minor grid
        ax[i].grid(which='minor', linestyle='--',
                linewidth='0.1', color='black', zorder=1)
    plt.show()
    ofile = f'output/Riv_Stage_Comparison/{title}_v3.png'
    fig.savefig(ofile, dpi=300, transparent=False, bbox_inches='tight')
    print(f'Saved {ofile}\n')
    plt.close()
    return None

def plot_ts_1fig_ccbyyear(dictionary, title, x, y, scatter_plot, ls):
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(16, 5))
    for i, file in enumerate(files.values()):

        # if list(files.keys())[i].endswith('2020'):
        file[x] = pd.to_datetime(file[x])
        grouped = file.groupby(file.date.dt.year)
        for key in grouped.groups.keys():
            grouped.get_group(key).plot(ax=ax, x = x, y = y,
                        linewidth=1.5,alpha=0.9, zorder=3, label = key)
            ax.minorticks_on()
            # Customize the minor grid
            ax.grid(which='minor', linestyle='--',
                    linewidth='0.1', color='black', zorder=1)
        ax.set_title(f'{title}', fontsize=14)
        ax.set_ylabel('River Stage (m)', fontsize=14)
        ax.set_xlabel('Time (years)', fontsize=14)
        ax.legend(bbox_to_anchor=(1.05, 1))
        # Customize the major grid
        ax.grid(which='major', linestyle='-',
                linewidth='0.1', color='red', zorder=2)

    plt.show()
    ofile = f'output/Riv_Stage_Comparison/{title}_{list(files.keys())[i]}.png'
    fig.savefig(ofile, dpi=300, transparent=False, bbox_inches='tight')
    print(f'Saved {ofile}\n')
    plt.close()
    return None

def plot_SPs_bymonth_allyears(files, title, x, y, scatter_plot, ls):
    import numpy as np
    # fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(16, 5))

    for i, file in enumerate(files.values()):
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(16, 5))
        file[x] = pd.to_datetime(file[x])
        file['year'] = file[x].dt.year
        file['month'] = file[x].dt.month
        file['day'] = file[x].dt.day
        if list(files.keys())[i].endswith('2015'):
            # file = file.loc[file.year < 2012]
            cmap = plt.get_cmap('gist_rainbow')
            colors = [cmap(k) for k in np.linspace(0, 1, len(file.year.unique()))] #0.4 end
        elif list(files.keys())[i].endswith('2020'):
            cmap = plt.get_cmap('gist_rainbow')
            colors = [cmap(k) for k in np.linspace(0, 1, len(file.year.unique()))] #0.5 start
        print(file.year.unique())
        for j, year in enumerate(file.year.unique()):
            df = file.loc[file.year == year]
            ax.plot(df['month'], df[y], color = colors[j], label = year)

        ax.grid(which='major', linestyle='-',
                linewidth='0.1', color='red', zorder=2)
        ax.minorticks_on()
        # Customize the minor grid
        ax.grid(which='minor', linestyle='--',
                linewidth='0.1', color='black', zorder=1)
        ax.set_title(f'{title}', fontsize=14)
        ax.legend(bbox_to_anchor=(1.05, 1))
        ax.set_ylabel('River Stage (m)', fontsize=14)
        ax.set_xlabel('Time (years)', fontsize=14)

        ###Update x-axis tick labels
        import matplotlib.ticker as plticker
        loc = plticker.MultipleLocator(base=1.0)  # this locator puts ticks at regular intervals
        ax.xaxis.set_major_locator(loc)
        labels = [item.get_text() for item in ax.get_xticklabels()]
        labels = ['0','Jan', 'Feb', 'Mar', 'Apr', 'May','Jun','Jul', 'Aug','Sep','Oct', 'Nov','Dec','13']
        ax.set_xticklabels(labels)

        ### Plot and save
        plt.show()
        ofile = f'output/Riv_Stage_Comparison/yearly_comparison_{list(files.keys())[i]}.png'
        fig.savefig(ofile, dpi=300, transparent=False, bbox_inches='tight')
        print(f'Saved {ofile}\n')
        plt.close()
        return None

def plot_ts_1figv2(files, title, x1, y1,x2, y2, ls, colors, DateRange):
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(16, 5))

    for i, file in enumerate(files.values()):
        if list(files.keys())[i].endswith('2020'):
            print('True 2020')
            file[x2] = pd.to_datetime(file[x2])
            ax.scatter(file[x2], file[y2], s=1, c=colors[i],
                       alpha=0.2, zorder=3, label=list(files.keys())[i])
        elif list(files.keys())[i].endswith('2015'):
            print('True 2015')
            file[x2] = pd.to_datetime(file[x2])
            ax.scatter(file[x2], file[y2], s=1, c=colors[i],
                       alpha=0.2, zorder=4, label=list(files.keys())[i])
        elif list(files.keys())[i].endswith('SP'):
            print('True SP')
            file[x1] = pd.to_datetime(file[x1])
            ax.plot(file[x1], file[y1], linewidth=1.5, linestyle=ls[i], color=colors[i],
                    alpha=1, zorder=6, label=list(files.keys())[i])
    ax.set_title(f'{title}', fontsize=14)
    ax.legend()
    ax.set_ylabel('River Stage (m)', fontsize=14)
    ax.set_xlabel('Time (years)', fontsize=14)
    # Customize the major grid
    ax.grid(which='major', linestyle='-',
            linewidth='0.1', color='red', zorder=2)
    ax.minorticks_on()
    # Customize the minor grid
    ax.grid(which='minor', linestyle='--',
            linewidth='0.1', color='black', zorder=1)

    if DateRange:
        ### used to focus in on a specific datetime range
        xmin, xmax = pd.to_datetime('01/1/2019'), pd.to_datetime('12/31/2019')
        ax.set_xlim([xmin, xmax])

    plt.show()
    ofile = f'output/Update.Predictive.Model/{title}_lowriverstage_2019.png'
    fig.savefig(ofile, dpi=300, transparent=False, bbox_inches='tight')
    print(f'Saved {ofile}\n')
    plt.close()

    return None

if __name__ == "__main__":
    cwd = os.getcwd()
    # inputDir = os.path.join(os.path.dirname(cwd), "Flow_Calibration_model", "T05_riverstage_eval")
    inputDir2 = os.path.join(os.path.dirname(cwd), "Update.Predictive.Model")
    # print(inputDir)

    ### SP-AVERAGED RIVER STAGE DATA ###
    # StgFil_SP = pd.read_csv(os.path.join(inputDir, "RIV_stage_vs_time_2006-2015.csv"))
    # StgFil_SP_2020 = pd.read_csv(os.path.join(inputDir, "RIV_stage_vs_time_2012-2020.csv"))
    # files = {'2006-2015': StgFil_SP, '2012-2020': StgFil_SP_2020}
    # title = "River Stage by SPs"
    # x = 'date'
    # y = 'average_stage'
    # scatter_plot = False
    # ls = ['-','--']
    # colors = ['darkorange', 'cornflowerblue']
    #
    # # ## HOURLY RIVER STAGE DATA ###
    # StgFil = pd.read_csv(os.path.join(inputDir, "bgage_raw_stage_2004-2015_corrected_after01Nov2010_and_reg.csv"))
    # StgFil_2020 = pd.read_csv(os.path.join(inputDir, "bgage_stage_regression_2004_2020.csv"))
    # files = {'2004-2014': StgFil, '2004-2020': StgFil_2020}
    # title = "River Stage (hourly)"
    # x = 'datetime'
    # y = 'bgage_WLelev_corr(m)'
    # scatter_plot = True
    # ls = ['-', '--']
    # colors = ['darkorange', 'cornflowerblue']

    # ### ALL RIVER STAGE DATA ###
    # StgFil_SP = pd.read_csv(os.path.join(inputDir, "RIV_stage_vs_time_2006-2015.csv"))
    # StgFil_SP_2020 = pd.read_csv(os.path.join(inputDir, "RIV_stage_vs_time_2012-2020.csv"))
    # StgFil = pd.read_csv(os.path.join(inputDir, "bgage_raw_stage_2004-2015_corrected_after01Nov2010_and_reg.csv"))
    # StgFil_2020 = pd.read_csv(os.path.join(inputDir, "bgage_stage_regression_2004_2020.csv"))
    #
    # files = {'2006-2015-SP': StgFil_SP, '2012-2020-SP': StgFil_SP_2020, '2004-2015': StgFil, '2004-2020': StgFil_2020}
    # title = "River Stage"
    # x1 = 'date'
    # y1 = 'average_stage'
    # x2 = 'datetime'
    # y2 = 'bgage_WLelev_corr(m)'
    # ls = ['-', '--','-','--']
    # colors = ['black', 'blue', 'lightgreen', 'grey']

    # ### ALL RIVER STAGE DATA ###
    ##Comparing old predictive model with new calibrated model:
    # StgFil_SP = pd.read_csv(os.path.join(inputDir, "RIV_stage_vs_time_2006-2015.csv"))
    # StgFil = pd.read_csv(os.path.join(inputDir, "bgage_raw_stage_2004-2015_corrected_after01Nov2010_and_reg.csv"))
    # StgFil_SP_2020 = pd.read_csv(os.path.join(inputDir, "RIV_stage_vs_time_2012-2020.csv"))
    # StgFil_2020 = pd.read_csv(os.path.join(inputDir, "bgage_stage_regression_2004_2020.csv"))

    ##Comparing old and new predictive models:
    StgFil_SP = pd.read_csv(os.path.join(inputDir2, "2006-2015_pred125", "RIV_stage_vs_time_2006-2015.csv"))
    StgFil = pd.read_csv(os.path.join(inputDir2, "2006-2015_pred125", "bgage_raw_stage_2004-2015_corrected_after01Nov2010_and_reg.csv"))
    StgFil_SP_2020 = pd.read_csv(os.path.join(inputDir2, "2006-2020_pred125", "01_genRIV", "RIV_stage_vs_time_2006-2020.csv"))
    StgFil_2020 = pd.read_csv(os.path.join(inputDir2, "2006-2020_pred125", "01_genRIV", "bgage_stage_regression_2004_2020_complete.csv"))

    # files = {'2006-2015-SP': StgFil_SP, '2006-2020-SP': StgFil_SP_2020, '2004-2015': StgFil, '2004-2020': StgFil_2020}
    files = {'2006-2020-SP': StgFil_SP_2020, '2004-2020': StgFil_2020}
    title = "River Stage"
    x1 = 'date'
    y1 = 'average_stage'
    x2 = 'datetime'
    y2 = 'bgage_WLelev_corr(m)'
    ls = ['-', '-.','-','--']
    colors = ['limegreen', 'mediumblue', 'navajowhite', 'slategrey']
    updateDate = True

    ### FUNCTIONS ###
    ## Hourly OR SP functions:
    # plot_ts_2rows(files, title, x, y, scatter_plot, colors)
    # plot_ts_1fig(files, title, x, y, scatter_plot, ls, colors)
    # plot_ts_2rows_ccbyyear(files, title, x, y, scatter_plot, ls)
    # plot_ts_1fig_ccbyyear(files, title, x, y, scatter_plot, ls)

    ## SP time-step function only:
    # plot_SPs_bymonth_allyears(files, title, x, y, scatter_plot, ls)

    ## Hourly AND SP function:
    plot_ts_1figv2(files, title, x1, y1, x2, y2, ls, colors, DateRange = updateDate)






