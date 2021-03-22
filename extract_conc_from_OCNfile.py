# -*- coding: utf-8 -*-
"""
Created on Wed Dec 30 10:31:34 2020

@author: MPedrazas

INPUT: STUFF.ocn --> output file from the TOB package of the transport model
OUTPUT: STUFF.txt
"""
import os
import pandas as pd
import fileinput
import csv

def get_conc_from_OCN(ifile, ofile):
    ifile = f'../../mpedrazas/Transport_Model/Transport/model1_clean/STUFF.ocn'
    ofile = f'../../mpedrazas/Transport_Model/Transport/model1_clean/STUFF_MP.txt'
    src = ifile
    dst = ofile
    
    header = ['WELLID','X_GRID','Y_GRID','LAYER', 'ROW', 'COLUMN','SPECIES', 'CALCULATED']
    
    #%% Get important data from line parsing OCN file:
    # fo=open(dst, "w")
    
    sp_idx_lst,num_lst, conc_lst =[],[],[]
    with open(src) as f:
        for num, line in enumerate(f,1): #loop through every line in STUFF.ocn
            linesplit=line.split()
            if('STRESS PERIOD' in line): #record line numbers where SP changes
                sp_idx_lst.append(num)
            if (len(linesplit) >= 8): #store conc data (and respective line numbers) only
                if ('No obs wells active at current transport step' not in line):
                    if('WELLID' not in line):
                        if('dry cell' not in line):
                            conc_lst.append(linesplit)
                            num_lst.append(num)
    
    df = pd.DataFrame(conc_lst, columns= header)
    df['line_num'] = num_lst
    
    sp_idx = sp_idx_lst[::5] #drop repeated SP line numbers for transport steps 2,3,4,5.
    SP = len(sp_idx)
    print("Stress Periods in OCN file:", SP)
    
    #%% Assign SP for conc data based on line numbers:
    
    #find index value for last rows related to last SP
    diff = pd.DataFrame([df.line_num[i + 1] - df.line_num[i] for i in range(len(df.line_num)-1)])
    last_row = df.line_num[(diff.loc[diff[0]>5]).index[-1]] 
    
    #make a dictionary between SP indices and actual SP values
    SPdict = {sp_idx[i]: list(range(1,SP+1))[i] for i in range(SP)} 
    temp = []
    for row in df.iterrows(): #loop through conc data
        for i,val in enumerate(sp_idx): #loop through SP line numbers
            print(row[1].line_num)
            if i == (SP-1) and row[1].line_num > last_row:  #last rows, before: hard coded 12158 as line num
                temp.append(SPdict[sp_idx[i]])
            elif i < (SP-1): #all other rows
                if row[1].line_num >= sp_idx[i] and row[1].line_num < sp_idx[i+1]:
                    temp.append(SPdict[val])
    df['SP'] = temp
    
    #Save conc data as csv
    df.to_csv(dst,index=False)
    print(f'Saved {dst}\n')
    df_check = pd.read_csv(dst)
    return df_check
#%%
if __name__ == "__main__":
    ifile = f'../../mpedrazas/Transport_Model/Transport/model1_clean/STUFF.ocn'
    ofile = f'../../mpedrazas/Transport_Model/Transport/model1_clean/STUFF_MP.txt'
    
    df = get_conc_from_OCN(ifile,ofile)