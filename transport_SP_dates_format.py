# -*- coding: utf-8 -*-
"""
Created on Sat Dec 26 08:46:11 2020

@author: MPedrazas
"""
import pandas as pd;
import os;
import platform;
import numpy as np;
import matplotlib.pyplot as plt
from datetime import datetime, date, time


#NICE PLOTTING FONT
plt.rcParams["font.sans-serif"] = "Arial"
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42
plt.rcParams['font.size'] = 8
#plt.style.use('seaborn-white')

print('pandas version: {}'.format(pd.__version__))              # 0.23.4
print('python version: {}'.format(platform.python_version()))   # 3.6.8
outputdir = os.path.dirname(os.getcwd())

#%% %% ########### convert stress_periods.csv to correct format for transport model ucn concentrations to shp file task
outputdir = os.path.dirname(os.getcwd())
sp = pd.read_csv('input/stress_periods_2014.csv', delimiter=',')
sp['end'] = pd.to_datetime(sp['end'],format='%y%m%d')
sp['start'] = pd.to_datetime(sp['start'],format='%y%m%d') #format='%d/%m/%YY')
# sp['start'] = sp['start'].dt.date
# sp['end'] = sp['end'].dt.date
sp['start'] = sp['start'].dt.strftime('%m/%d/%Y')
sp['end'] = sp['end'].dt.strftime('%m/%d/%Y')
sp[['sp','start', 'end']].to_csv('output/stress_periods_2014_transport.csv', index=False) #csv file for transport model ucn concentrations to shp files
