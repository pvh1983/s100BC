import os
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error

def rmse(predictions, targets):
    return np.sqrt(((predictions - targets) ** 2).mean())

res_2014 = '../../hpham/100BC_Calibration_model/PEST_version_7b_modified_2012-2014/master/100BC_GWM_calib7b.res'
res_2020 = '../../hpham/100BC_Calibration_model/PEST_version_7b_modified_2012-2014/test7_chkobjfunc_newweigh/100BC_GWM_calib_2012_2020.res'
res_cols = ['Name', 'Group', 'Measured', 'Modelled','Residual','Weight', 'Weight*Measured','Weight*Modelled', 'Weight*Residual' , 'Measurement_sd', 'Natural_weight']
df_2014 = pd.read_csv(res_2014 , skiprows =1 , names = res_cols)
df_2020 = pd.read_csv(res_2020 , skiprows =1 , names = res_cols)

dfs = [df_2014,df_2020]
for i, df in enumerate(dfs):
    df[res_cols] = df.Name.str.split(expand=True) 
    # df.columns = df.columns.str.replace('   ', '')
    df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

df, mean_lst, rmse_lst, final_lst = [],[],[],[]

for group in (df_2014['Group'].unique()[:-6]): #['dirn_crv']
    #get rid of head_182b:
    if group == 'head_182b':
        continue
    else:
        print(group)
        df = df_2014[df_2014['Group'] == group] 
        df = np.where(df == 'na',0, df)
        df = pd.DataFrame(df, columns=res_cols)
        df.iloc[:,2:] = df.iloc[:,2:].astype(float)

        mean_obs = df['Measured'].astype(float).mean()
        mean_sim = df['Modelled'].astype(float).mean()
        rmse_val = rmse(np.array(df['Modelled']), np.array(df['Measured']))
        mse_val = mean_squared_error(np.array(df['Measured']), df['Modelled'])
        
        final_lst.append((group, mean_obs, mean_sim, rmse_val, mse_val))

stats_2014 = pd.DataFrame(final_lst)#.transpose()
stats_2014 = stats_2014.rename(columns = {0:'Group', 1:'Mean_Obs',2:'Mean_Sim',3:'RMSE',4:'MSE'})
stats_2014.to_csv('output/stats',index=False)