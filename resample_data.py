
import pandas as pd

# Read
ifile = '../usgs_data/gage_height_PRD.csv'
# c:/Users\hpham\OneDrive - INTERA Inc\projects\020_100BC\hpham\Boundary_Conditions\genRIV_version4\USGS_data\

df = pd.read_csv(ifile)
df['datetime'] = pd.to_datetime(df['datetime'])
df_daily = df.resample('d', on='datetime').mean()  # resample to daily
df_daily.to_csv('output/PRD_gage_height_daily.csv')

df_hourly = df.resample('h', on='datetime').mean()  # resample to daily
df_hourly.to_csv('output/PRD_gage_height_hourly.csv')
