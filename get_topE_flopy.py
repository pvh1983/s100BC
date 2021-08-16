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
outDir=os.path.join(cwd,'intermediate','topE_OUTPUT')
if not os.path.exists(outDir):
    os.makedirs(outDir)

# Flopy Basics
exe = 'mf2k-chprc07dpl'
ws = r'C:\Users\mpedrazas\OneDrive - INTERA Inc\020_100BC\mpedrazas\100BC_GWM\model_files\flow'

#load model
m = flopy.modflow.Modflow.load('100BC_2012_2020.nam', verbose = True, model_ws = ws, exe_name = exe, check=False)
# get dis object
dis = m.get_package("dis")
#WARNING. This command is to create a new DIS package: dis = flopy.modflow.ModflowDis(m)

print(m.dis.nlay)
a = m.dis.top.array[0]
m.dis.top.plot()

# ax = m.dis.top.plot()
# m.dis.top.plot(axes=ax, contour=True, pcolor=False);

m.dis.top.export(os.path.join(outDir,"topE.shp"))
gdf_topE = gpd.read_file(os.path.join(outDir, "topE.shp"))

#%%
#use model grid shapefile geometry
gridShp = os.path.join(cwd,'input','grid_100BC_GWM.shp') #model grid shapefile
gdf = gpd.read_file(gridShp)   

#export shapefile
gdf2 = gpd.GeoDataFrame(gdf_topE, crs='EPSG:4326', geometry=gdf.geometry) 
gdf2.to_file(driver = 'ESRI Shapefile', filename = os.path.join(outDir,'topE_w_geom.shp')) 
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