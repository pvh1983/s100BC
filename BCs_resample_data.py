
import pandas as pd
import os
import numpy as np

cwd = os.getcwd()
#cwd = "C:\Users\MPedrazas\INTERA Inc\Hai Pham - 020_100BC\mpedrazas\scripts_100BC

# Read
input_dir = os.path.join(os.path.dirname(cwd),"Update.Predictive.Model","2006-2020_pred170","usgs_data")
ifile = "gage_height_PRD_year2020.csv" #this is the 15-minute interval data downloaded from the usgs website
#usgs website: https://waterdata.usgs.gov/nwis/uv?site_no=12472800

df = pd.read_csv(os.path.join(input_dir, ifile))
df['datetime'] = pd.to_datetime(df['datetime'])
df_daily = df.resample('d', on='datetime').mean()  # resample to daily
df_daily.to_csv(os.path.join(input_dir,'gage_height_PRD_year2020_daily.csv'))
df_hourly = df.resample('h', on='datetime').mean()  # resample to daily
df_hourly.to_csv(os.path.join(input_dir,'gage_height_PRD_year2020_hourly.csv'))

# Now calculate B gauge from regression eqn:
df_hourly.rename(columns = {'151852_00065':'PRD stage (ft)'}, inplace=True)
df_hourly['PRD elevation (ft)'] = (df_hourly['PRD stage (ft)'] + 390 + 3.49)/3.2808
df_hourly['bgage_WLelev_corr(m)'] = (df_hourly['PRD elevation (ft)'] * 0.84742) + 15.107
df_hourly['bgage_WLelev_corr(m)'] = df_hourly['bgage_WLelev_corr(m)'].map('{:,.4f}'.format) #two decimal places
df_hourly.to_csv(os.path.join(input_dir,'bgage_stage_regression_year2020_hourly_calcs.csv'))
df_hourly = df_hourly[['bgage_WLelev_corr(m)']] #drop other cols
df_hourly.reset_index(level=0, inplace=True) #make index datetime a column
df_hourly.to_csv(os.path.join(input_dir,'bgage_stage_regression_2020_final.csv'), index=False)

### merge 2004 to 2020 (incomplete year) bgage stage regression with year 2020 dataset.
input_dir2 = os.path.join(os.path.dirname(cwd),"Update.Predictive.Model","2006-2020_pred170")
df_2004_2020 = pd.read_csv(os.path.join(input_dir2, 'bgage_stage_regression_2004_2020.csv'))
df_2004_2020['datetime'] = pd.to_datetime(df_2004_2020['datetime'])
df_2004_2019 = df_2004_2020.loc[df_2004_2020['datetime'] < pd.to_datetime('2020-01-01 00:00:00')]

df_2004_2020_complete = pd.concat([df_2004_2019, df_hourly])
df_2004_2020_complete = df_2004_2020_complete.loc[df_2004_2020_complete['datetime'] < pd.to_datetime('2021-01-01 00:00:00')] #cutoff is end of 2020
df_2004_2020_complete = df_2004_2020_complete.loc[df_2004_2020_complete['bgage_WLelev_corr(m)'] != 'nan'] #get rid of any nans
df_2004_2020_complete['bgage_WLelev_corr(m)'] = df_2004_2020_complete['bgage_WLelev_corr(m)'].astype(float)
df_2004_2020_complete['bgage_WLelev_corr(m)'] = df_2004_2020_complete['bgage_WLelev_corr(m)'].map('{:,.4f}'.format) #four decimal places
df_2004_2020_complete.to_csv(os.path.join(input_dir2,'bgage_stage_regression_2004_2020_complete.csv'), index=False)
df_2004_2020_complete.to_csv(os.path.join(input_dir,'bgage_stage_regression_2004_2020_complete.csv'), index=False)

### Note, to get it in the right format, open it in excel and make sure the custom format is mm/dd/yy hh:mm AM/PM
### Last step is to load it in genRIV_2006_2020_predictive.pl