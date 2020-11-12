import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from datetime import datetime, date, time

cols = ['Well Name', 'Date', 'Time', 'Groundwater level (m)']
ifile = 'c:/Users/hpham/OneDrive - INTERA Inc/projects/020_100BC/Michelle/Calibration_model/T02_observation_data/mod2obs/Bore_Sample_File_in_model_manual_v4.csv'
df = pd.read_csv(ifile, delimiter=',',
                 skipinitialspace=True, names=cols)

df['Date'] = pd.to_datetime(df['Date'])
cutoff_date = datetime(2020, 9, 25)
df = df[df.Date < cutoff_date]

list_wnames = df['Well Name'].unique()

# get time stress
if_ts = f'c:/Users/hpham/OneDrive - INTERA Inc/projects/020_100BC/hpham/100BC_Calibration_model/slave_2012_2020/sp_date_2012-2020.csv'
df_ts = pd.read_csv(if_ts, delimiter=',',
                    skipinitialspace=True, names=['SP', 'Date'])
#

df2 = pd.DataFrame()
for wn in list_wnames:
    df_tmp = pd.DataFrame()
    df_tmp['SP'] = df_ts['SP']
    df_tmp['Date'] = df_ts['Date']

    df_tmp['Well Name'] = wn
    #df_tmp['Groundwater level(m)'] = -9999
    df2 = pd.concat([df2, df_tmp], axis=0)

df2['Date'] = pd.to_datetime(df2['Date'])
# merge two df by date
df_merge = df2.merge(df,  how='left', on=['Date', 'Well Name'])
df_merge['Time'] = '0:00:00'

df_final = df_merge[['Well Name', 'Date', 'Time', 'Groundwater level (m)']]
ofile = 'c:/Users/hpham/OneDrive - INTERA Inc/projects/020_100BC/hpham/100BC_Calibration_model/slave_2012_2020/Bore_Sample_File_in_model_manual.csv'
#df_final.to_csv(ofile, index=False)
#print(f'Saved {ofile}/n')
print('Remember to replace empty cell = -9999/n')
print('Remember to delete column names/n')
print('Remember to re-format Date column before running mod2obs/n')

# =============================================================================
# For 2012-2014 ===============================================================
# =============================================================================
cols = ['Well Name', 'Date', 'Time', 'Groundwater level (m)']
ifile = '../../100BC_GWFTM/100BC_Calibration_model/PEST_version_7b_modified_2012-2014/slave/Bore_Sample_File_in_model_manual.csv'
df = pd.read_csv(ifile, delimiter=',',
                 skipinitialspace=True, names=cols)
df['Date'] = pd.to_datetime(df['Date'])

list_wnames = df['Well Name'].unique()

# get time stress
if_ts = f'../100BC_Calibration_model/slave_2012_2014/sp_date.csv'
df_ts = pd.read_csv(if_ts, delimiter=',',
                    skipinitialspace=True, names=['SP', 'Date'])
#

df2 = pd.DataFrame()
for wn in list_wnames:
    df_tmp = pd.DataFrame()
    df_tmp['SP'] = df_ts['SP']
    df_tmp['Date'] = df_ts['Date']

    df_tmp['Well Name'] = wn
    #df_tmp['Groundwater level(m)'] = -9999
    df2 = pd.concat([df2, df_tmp], axis=0)

df2['Date'] = pd.to_datetime(df2['Date'])
# merge two df by date
df_merge = df2.merge(df,  how='left', on=['Date', 'Well Name'])
df_merge['Time'] = '0:00:00'

df_final = df_merge[['Well Name', 'Date', 'Time', 'Groundwater level (m)']]
ofile1214 = 'c:/Users/hpham/OneDrive - INTERA Inc/projects/020_100BC/hpham/100BC_Calibration_model/slave_2012_2014/Bore_Sample_File_in_model_manual.csv'
#df_final.to_csv(ofile1214, index=False)

#print(f'Saved {ofile}/n')
print('Remember to replace empty cell = -9999/n')
print('Remember to delete column names/n')
print('Remember to re-format Date column before running mod2obs/n')
