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


def read_ref(ifile, nr, nc):  # Return an array
    # Generate an empty arr
    arr = np.empty([nr, nc])
    arr[:, :] = np.nan

    count = 0
    val = []
    i = 0
    with open(ifile) as fp:
        for line in fp:
            line_spit = line.split()
            line_spit_conv = [float(line_spit[k])
                              for k in range(len(line_spit))]
            #print(f'i = {i}, count = {count}, {line.split()[0]}, {len(val)}\n')
            val = val + line_spit_conv
            count += 1
            if len(val) == nc:
                arr[i, :] = val
                val = []
                i += 1
    return arr

if __name__ == "__main__":
    # directories
    cwd=os.getcwd()                               # base directory to inconc*.ref files
    year = '2014_max' #2014_max
    outDir=os.path.join(cwd,'intermediate','IC_shps_rev3_{}_OUTPUT'.format(year))
    if not os.path.exists(outDir):
        os.makedirs(outDir)
    # path2ref = r"C:\Users\MPedrazas\OneDrive - INTERA Inc\020_100BC\mpedrazas\Transport_Model\T09_IC_map\INPUT_Files\rev2013_ref_files_IC_forHelal"
    # path2ref = r"S:\PSC\CHPRC.C003.HANOFF\Rel.106\preprocess\plume_process\CrVI_2014\max_05172021"
    path2ref = r"S:\PSC\CHPRC.C003.HANOFF\Rel.106\preprocess\plume_process\CrVI_{}\max_05172021".format(year[0:4])
    if year == '2014_max':
        refs = [f'100BC_CrVI_IC_{year[0:4]}_1_max.ref',
               f'100BC_CrVI_IC_{year[0:4]}_2_max.ref',
               f'100BC_CrVI_IC_{year[0:4]}_3_max.ref',
               f'100BC_CrVI_IC_{year[0:4]}_4_max.ref',
               f'100BC_CrVI_IC_{year[0:4]}_5_max.ref',
               f'100BC_CrVI_IC_{year[0:4]}_6_max.ref']
    if year == '2013':
        refs = [f'100BC_CrVI_IC_{year[0:4]}_1.ref',
           f'100BC_CrVI_IC_{year[0:4]}_2.ref',
           f'100BC_CrVI_IC_{year[0:4]}_3.ref',
           f'100BC_CrVI_IC_{year[0:4]}_4.ref',
           f'100BC_CrVI_IC_{year[0:4]}_5.ref',
           f'100BC_CrVI_IC_{year[0:4]}_6.ref']
    for myint in range(len(refs)):
        print(myint)
        df = read_ref(os.path.join(path2ref,refs[myint]), 362, 368)
        
        #flatten row x column df
        vals = []
        for i in range(0,362):
            for j in range(0,368):
    #            print(i,j)
                val = df[i,j]
                vals.append(val)
        #use model grid shapefile geometry
        gridShp = os.path.join(cwd,'input','grid_100BC_GWM.shp') #model grid shapefile
        gdf = gpd.read_file(gridShp)   
        dfval = pd.DataFrame(vals, dtype = float, columns = ['lf_data00'+ str(myint)]) # + str(myint-1))
        dfval['row'] = gdf['row']
        dfval['column'] = gdf['column']
        
        #export shapefile
        gdf1 = gpd.GeoDataFrame(dfval, crs='EPSG:4326', geometry=gdf.geometry) 
        gdf1.to_file(driver = 'ESRI Shapefile', filename = os.path.join(outDir,'initial_conc_L' + str(myint)+'.shp')) 
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