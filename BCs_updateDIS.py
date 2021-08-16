import os
import shutil
import pandas as pd
import numpy as np
import datetime as dt
import csv

cwd = os.getcwd()
#cwd = "C:\Users\MPedrazas\INTERA Inc\Hai Pham - 020_100BC\mpedrazas\scripts_100BC

# [Step 1] Read in files
input_dir = os.path.join(os.path.dirname(cwd),"Update.Predictive.Model","2006-2020_pred125")

dis_df = pd.read_csv(os.path.join(input_dir, "01_genRIV","sp_date_2006-2020.csv"), names=["SP","date"])
dis_df.date = pd.to_datetime(dis_df.date)
dis_df['SPlen'] = 0
delta,lst = [],[]
for i in range(len(dis_df)-1):
    date1 = dis_df.date.iloc[i]
    date2 = dis_df.date.iloc[i+1]
    delta.append(date2-date1)
delta.append(pd.Timedelta("30 days")) #last SP starts 12/02/2020 ends in 12/31/2020 = 30 days.
dis_df.SPlen = delta

disx4 = pd.concat([dis_df]*4, ignore_index=True) #cycle through monthly SPs 4 times.
yearlydis = dis_df.loc[dis_df.date == pd.to_datetime('9/3/2019')]#SP 165
yearlydis['SPlen'] = pd.Timedelta("365 days")
yearlydisx110 = pd.concat([yearlydis]*110, ignore_index=True)

dis_full = pd.concat([disx4, yearlydisx110], ignore_index=True)
dis_full.SP = dis_full.index+1
dis_full['Month'] = 'Jan-Dec'
dis_full.Month.loc[dis_full.index < 720] = dis_full.date.dt.strftime('%b')

start_year, end_year, end_pred170 = 2021, 2081, 2190
years = list(np.arange(start_year, end_year,1))
yrs_lst = []
for year in years:
    for i in range(12): #monthly SPs, so repeat 12 times
        yrs_lst.append(year)
for year2 in list(np.arange(end_year, end_pred170+1, 1)): #append yearly SPs to end of simulation
    yrs_lst.append(year2)
dis_full['Year'] = yrs_lst

for leapyear in list(np.arange(2084,2190,4)):
    dis_full.SPlen.loc[dis_full.Year == leapyear] = pd.Timedelta("366 days")
dis_full.SPlen.loc[dis_full.Year == 2100] = pd.Timedelta("365 days") #Year 2100 is not a leap year
dis_full.SPlen = dis_full.SPlen.dt.days #convert timedelta into integers

final_df = dis_full.copy()
final_df['ts'] = '1'
final_df.ts.loc[dis_full.index >= 720] = '5'
final_df['n'] = '1.000000'
final_df['TR'] = 'TR'
for i in range(len(final_df)):
    final_df.Year.loc[i] = f'   {final_df.Year.loc[i]}'
    if i < 720:
        final_df.SPlen.loc[i] = f' {final_df.SPlen.loc[i]}.000000'
    else: #i >= 720:
        final_df.SPlen.loc[i] = f' {final_df.SPlen.loc[i]}.00000'
final_df = final_df[['SPlen', 'ts', 'n', 'TR', 'Month', 'Year']]
final_df.to_csv(os.path.join(input_dir,"06_updateDIS","stress_periods_DIS_pred170.txt"),
                sep = ",", index=False, header=False)
final_df_str = final_df.to_string(header=False, index = False)

#[STEP 2] Append new SPs to end of DIS file, remove old SPs
oldfiles = ["100BC_5m_GeoV2_Evaluated_V3_125yrs.dis"]
appendfiles = ["stress_periods_DIS_pred170.txt"]
newfiles = ["100BC_5m_GeoV2_Evaluated_V0_170yrs.dis"]

monthlySP, yearlySP = 720, 110
lines,lines2,stop = [],[],[]
for f1,f2,f3 in zip(oldfiles,appendfiles, newfiles):
    lines, start, end = [], [], []
    with open(os.path.join(os.path.dirname(input_dir),"2006-2015_pred125",f1), 'r') as file1:
        for idx, line in enumerate(file1):
            lines.append((idx, line))
            if line == "  30.000000  1  1.000000  TR      January   2015\n":
                stop.append(idx)
    # file2 = open(os.path.join(input_dir, "06_updateDIS", f2), 'r')  # write new file for updated predictive model
    # for idx, line in enumerate(file1):
    #     lines.append((idx, line))
    with open(os.path.join(input_dir,"06_updateDIS",f3), 'w') as file3:
        for n in list(np.arange(0, stop[0])):
            file3.write(lines[n][1])
        file3.write(final_df_str)

    ### Don't forget to update Line 2 of DIS file with updated total number of SPs.










