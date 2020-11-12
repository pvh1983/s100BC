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

df2 = df[df.Date < cutoff_date]

ofile = 'c:/Users/hpham/OneDrive - INTERA Inc/projects/020_100BC/hpham/100BC_Calibration_model/slave_2012_2020/Bore_Sample_File_in_model_manual.csv'
print(f'Saved {ofile}\n')

df2.to_csv(ofile, index=False)

print('Remember to delete column names\n')
print('Remember to re-format Date column before running mod2obs\n')
