# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 15:43:38 2021

@author: MPedrazas
"""
import geopandas as gpd
import numpy as np
import pandas as pd
import os
import glob
import shutil
import os
import sys
import numpy as np
import matplotlib as mpl
import flopy.modflow as fpm
import flopy.utils as fpu
import flopy

# directories
cwd=os.getcwd()
outDir=os.path.join(cwd,'intermediate','RCH_OUTPUT')
if not os.path.exists(outDir):
    os.makedirs(outDir)

# Flopy Basics
exe = 'mf2k-chprc07dpl'
ws = r'C:\Users\mpedrazas\OneDrive - INTERA Inc\020_100BC\mpedrazas\100BC_GWM\model_files\flow'

#load model and get rch object
m = flopy.modflow.Modflow.load('100BC_2012_2020.nam', verbose = True, model_ws = ws, exe_name = exe, check=False)
rch = m.get_package("rch")
df_rch = m.rch.rech.array[0][0] #get first array

vals = []
for i in range(0,362):
    for j in range(0,368):
#            print(i,j)
        val = df_rch[i,j]
        vals.append(val)
dfval = pd.DataFrame(vals, dtype = float, columns = ['rech']) # + str(myint-1))

## plot rch -you call rech values using rch.rech.
#rch changes in 2011,2021 and 2051 #SP of interest - zero-based index (flopy)
# m.rch.rech.plot(kper=0, masked_values=[0.], colorbar=True); #kper = 'all''

## recharge array is constant from 2012-2020
# for i in range(0,385):
#     print(i)
#     a= m.rch.rech.get_kper_entry(i)[1]
#     b = m.rch.rech.get_kper_entry(i+1)[1]
#     if a[75:]== b[75:]:
#         print('True')

## export rch as shapefile
#transient - how to pick times correctly?
# m.rch.rech.as_shapefile(os.path.join(outDir,'rch1.shp'))
# m.rch.export(os.path.join(outDir,"rch2.shp"))
# gdf_rch = gpd.read_file(os.path.join(outDir, "rch.shp"))

#%% Use model grid shapefile geometry
gridShp = os.path.join(cwd,'input','grid_100BC_GWM.shp') #model grid shapefile
gdf = gpd.read_file(gridShp)   
dfval['row'] = gdf['row']
dfval['column'] = gdf['column']
# #export shapefile
gdf2 = gpd.GeoDataFrame(dfval, crs='EPSG:4326', geometry=gdf.geometry) 
gdf2.to_csv(os.path.join(outDir,'rch_w_geom.csv'), index=False)
gdf2.to_file(driver = 'ESRI Shapefile', filename = os.path.join(outDir,'rch_w_geom.shp')) 
#%%
# copy in template *.shx, *.shp, and *.prj from template file which contains R,C and X,Y coords (same size)
tplname='grid_100BC_GWM' 
for file in glob.iglob(os.path.join(outDir, '*.dbf')):
    name=os.path.splitext(file)[0]
    print(file)
    print(name)
    for ext in ['.prj','.shx','.shp']:
        shutil.copyfile(os.path.join(cwd,'input',tplname + ext), os.path.join(outDir,name + ext))
        print(name + ext)