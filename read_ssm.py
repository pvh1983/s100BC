# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 16:39:10 2021

@author: MPedrazas
"""

import flopy
import os
import numpy as np
import pandas as pd

#recharge:
rch_path = os.path.join(os.path.dirname(os.getcwd()),'Transport_Model','T6_SSM_Package','100BC_5m_GeoV2_Evaluated_V3.rch')

#nosourcedecay: 53 arrays, rate = 100
ssm_path = os.path.join(os.path.dirname(os.getcwd()),'Transport_Model','T6_SSM_Package','nosourcedecay.ssm')

#calib144: 54 arrays, rate = 100, then 1000
ssm_path2 = os.path.join(os.path.dirname(os.getcwd()),'Transport_Model','T6_SSM_Package','calib144.ssm')

#columnb: 126 arrays, rate = 100
ssm_path3 = os.path.join(os.path.dirname(os.getcwd()),'Transport_Model','T6_SSM_Package','columnb.ssm')

#columnb: 126 arrays, rate = 100
ssm_path4 = os.path.join(os.path.dirname(os.getcwd()),'Transport_Model','T6_SSM_Package','columna.ssm')

#constantsourcenoscale: 1 array, rate = 100
ssm_path5 = os.path.join(os.path.dirname(os.getcwd()),'Transport_Model','T6_SSM_Package','constantsourcenoscale.ssm')

ssm_file=ssm_path2
#%% Read in actual model grid values

data, vals = [],[]
with open(ssm_file,'r') as f:
    for num, line in enumerate(f,1):
        # if num >= first_line and num <= last_line:
        linesplit=line.split()
        if (len(linesplit) >= 8):
            vals.append(linesplit)    
data.append(vals)

#%% Read in concn headers
data2, headers = [], []
with open(ssm_file,'r') as f:
    for num, line in enumerate(f,1):
        # if num ==4:
        linesplit=line.split()
        # print(linesplit)
        if (len(linesplit) >= 3) and (len(linesplit) <= 4):
            headers.append(linesplit)

data2.append(headers)

#Flatten out list by converting into dataframe:
df_data2= pd.DataFrame(data2[0])
#%% Read in what seems to be SP repetitions
first_line = 4
data3, reps = [], []
with open(ssm_file,'r') as f:
    for num, line in enumerate(f,1):
        if num > first_line:
            linesplit=line.split()
            if (len(linesplit) == 1):
                reps.append(linesplit)

data3.append(reps)

# flatten out list by converting into dataframe:
df_data3= pd.DataFrame(data3[0]).astype(float)
#get rid of 1s which are related to ccn headers
df_data3_no1s = df_data3.loc[df_data3[0] != 1] 

#%%  Get individual arrays and store them in list ssm_array
ssm_array=[]
# nrows = 362
ncols = 368

for n in range(0,len(data)):
    a=data[n]
    arr=[]
    if len(a)!=0:
        for i in range(0,len(a)):
            for j in range(0,len(a[i])):
                temp=a[i][j]
                arr.append(temp)
        sf1=np.array(arr)
        sf1=sf1.astype(np.float)
        sf1.shape
        nrows = int(len(sf1)/ncols)
        sf1=np.reshape(sf1,[nrows,ncols])
        ssm_array.append(sf1)
        
#%% Plot model grid arrays concentration values
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

fig = plt.figure()
final_grid = []
for k in range(0,len(ssm_array[0]),362):
    print(k)
    grid = ssm_array[0][k:k+362]
    im = plt.imshow(grid, cmap = 'viridis') #, vmin=0, vmax = 31000000.0)
    plt.colorbar(im, orientation = 'vertical')
    plt.grid(which='both')
    plt.show()
    final_grid.append(grid)
    
    
#%% get statistics for every array
stats = []
for i in range(0,len(final_grid)):
    print(i)
    mean_lst = final_grid[i].mean()
    max_lst = final_grid[i].max()
    min_lst = final_grid[i].min()
    sum_lst = final_grid[i].sum()
    stats.append((mean_lst,max_lst,min_lst, sum_lst))

stats_df = pd.DataFrame(stats, columns=['Mean', 'Max','Min','Sum'])
stats_df.to_csv(os.path.join(os.getcwd(),'output','statistics-ssm-file.csv'), index=False)

test = pd.DataFrame(final_grid[0])

#%% Plot concentration headers
fig = plt.figure()
x = range(0,len(df_data2[0]),1)
plt.scatter(x,df_data2[0], s=10)
plt.ylabel('Mass loading rate')
plt.xlabel('Time')

#%%