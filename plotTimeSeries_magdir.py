import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib.ticker import AutoMinorLocator

plt.rc('xtick', labelsize=12)
plt.rc('ytick', labelsize=12)

def plot_ts_1figv2(files, title, x2, y2, ls, colors, DateRange, plotTitle):
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(16, 6))
    for i, file in enumerate(files.values()):
        file[x2] = pd.to_datetime(file[x2])
        ax.plot(file[x2], file[y2], linewidth=1.5, linestyle=ls[i], color=colors[i],
                    alpha=1, zorder=2, label=list(files.keys())[i])
        ax.scatter(file[x2], file[y2], s=20, zorder=3, color=colors[i], edgecolor = colors[i+2], linewidth = 0.5)
    if plotTitle:
        ax.set_title(f'{title}: {wellDict[title]}', fontsize=14, fontweight='bold')
    ax.legend()
    if y2 == 'dir':
        ax.set_ylabel('Direction (degrees, north=0)', fontsize=14)
        plt.yticks(np.arange(0, 364, 45))
        ax.set_yticklabels(['0 N', '45 NE', '90 E', '135 SE', '180 S', '225 SW', '270 W', '315 NW', '360 N'])
        # ax.set_ylim([0 - 5, 360 + 5])
        # ax.yaxis.set_minor_locator(AutoMinorLocator(5))
    elif y2 == 'mag':
        ax.set_ylabel('Magnitude (m/m)', fontsize=14)
        ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.1e'))
        ax.axhline(y=0.000125, color='black')
    ax.set_xlabel('Time (years)', fontsize=14)
    # Customize the major grid
    ax.grid(which='major', linestyle='-',
            linewidth='0.1', color='red', zorder=1)
    if DateRange:
        ### used to focus in on a specific datetime range
        xmin, xmax = pd.to_datetime('01/1/2019'), pd.to_datetime('12/31/2019')
        ax.set_xlim([xmin, xmax])

    ### Update x-axis tick labels
    import matplotlib.dates as mdates
    ax.get_xaxis().set_major_locator(mdates.MonthLocator(interval=6)) # Tick labels every 3 months
    ax.get_xaxis().set_major_formatter(mdates.DateFormatter("%b %Y")) #formate date displayed
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right") #rotate dates so they fit nicely
    ax.xaxis.set_minor_locator(mdates.MonthLocator()) #set minor ticks every month


    # Customize the minor grid
    ax.grid(which='minor', linestyle='--',
            linewidth='0.1', color='black', alpha=0.5, zorder=1)

    plt.show()
    if DateRange:
        ofile = f'output/Update.Predictive.Model/{title}_{y2}_evalgrad_focus2019.png'
    else:
        ofile = f'output/Update.Predictive.Model/{title}_{y2}_evalgrad.png'
    fig.savefig(ofile, dpi=300, transparent=False, bbox_inches='tight')
    print(f'Saved {ofile}\n')
    plt.close()

    return None

def plot_crossplot(files, title, x2, y2, ls, colors, DateRange, plotTitle):
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 10))
    ax.scatter(files['Observed'][y2], files['Simulated'][y2], s=50, zorder=3, edgecolor='darkgreen',
            color='#e5f5e0')
    if plotTitle:
        ax.set_title(f'{title}: {wellDict[title]}', fontsize=14, fontweight='bold')
    # ax.legend()
    ax.plot([0, 1], [0, 1], color='gray', linestyle = '--', linewidth=2, transform=ax.transAxes, zorder=1)
    if min(files['Observed'][y2]) >  min(files['Simulated'][y2]):
        plot_min = min(files['Observed'][y2])
    else:
        plot_min = min(files['Simulated'][y2])
    if max(files['Observed'][y2]) >  max(files['Simulated'][y2]):
        plot_max = max(files['Observed'][y2])
    else:
        plot_max = max(files['Simulated'][y2])
    ax.set_ylim([plot_min - plot_min*1.5, plot_max + plot_max*0.1])
    ax.set_xlim([plot_min - plot_min*1.5, plot_max + plot_max*0.1])
    if y2 == 'dir':
        ax.set_ylabel('Simulated Direction (degrees, north=0)', fontsize=14)
        ax.set_xlabel('Observed Direction (degrees, north=0)', fontsize=14)
        plt.yticks(np.arange(0, 364, 45))
        plt.xticks(np.arange(0, 364, 45))
        ax.set_yticklabels(['0 N', '45 NE', '90 E', '135 SE', '180 S', '225 SW', '270 W', '315 NW', '360 N'])
        ax.set_yticklabels(['0 N', '45 NE', '90 E', '135 SE', '180 S', '225 SW', '270 W', '315 NW', '360 N'])
    elif y2 == 'mag':
        ax.set_ylabel('Simulated Magnitude (m/m)', fontsize=14)
        ax.set_xlabel('Observed Magnitude (m/m)', fontsize=14)
        ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.1e'))
        ax.xaxis.set_major_formatter(mtick.FormatStrFormatter('%.1e'))
        # ax.axhline(y=0.000125, color='black')
    # Customize the major grid
    ax.grid(which='major', linestyle='-',
            linewidth='0.1', color='red', zorder=1)
    # Customize the minor grid
    ax.grid(which='minor', linestyle='--',
            linewidth='0.1', color='black', alpha=0.5, zorder=1)
    plt.show()
    ofile = f'output/Update.Predictive.Model/{title}_crossplot_evalgrad.png'
    fig.savefig(ofile, dpi=300, transparent=False, bbox_inches='tight')
    print(f'Saved {ofile}\n')
    plt.close()

    return None

if __name__ == "__main__":
    cwd = os.getcwd()
    inputDir = os.path.join(os.path.dirname(cwd), "Update.Predictive.Model", "2006-2020_pred170", "03_evalGrad")
    print(inputDir)

    wellDict = {'NorthWells': ['199-B5-1', '199-B3-51','199-B3-50'],
                'SouthWells': ['199-B4-14', '199-B5-8','199-B8-6'],
                'CenterWells': ['199-B5-1', '199-B4-16','199-B3-50']}

    for key in list(wellDict.keys()):
        file_Sim = pd.read_csv(os.path.join(inputDir, f"source_{key}.csv"), names=["date", "date2", "mag", "dir"])
        file_Obs = pd.read_csv(os.path.join(inputDir, "preprocess", f"{key}", f"{key}_2012-2020_magdir.csv"),
                               names=["date", "date2", "mag", "dir"], skiprows=1)
        files = {'Simulated': file_Sim, 'Observed': file_Obs}
        title = f"{key}"
        x2 = 'date'
        y2 = 'dir'
        ls = ['-', '-.','-','--']
        colors = ['royalblue', 'peru', 'cornflowerblue','orange', ]
        plot_ts_1figv2(files, title, x2, y2, ls, colors, DateRange = False, plotTitle = False)
        if y2 == 'mag':
            plot_crossplot(files, title, x2, y2, ls, colors, DateRange = False, plotTitle = False)

        # ### get table of groupbymonth, min, med, max:
        # for i, file in enumerate(files.values()):
        #     file[x2] = pd.to_datetime(file[x2])
        #     # file[x2], file[y2],label=list(files.keys())[i])