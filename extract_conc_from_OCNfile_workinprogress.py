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

def Head_AWLN():
    ifile = f'../../mpedrazas/Transport_Model/Transport/model1_clean/STUFF.ocn'
    ofile = f'../../mpedrazas/Transport_Model/Transport/model1_clean/MP.txt'
    
    df = pd.read_csv(ifile)
    src = ifile
    dst = ofile
    
    header = ['WELLID','X_GRID','Y_GRID','LAYER', 'ROW', 'COLUMN','SPECIES', 'CALCULATED']
    
    #%%
    fo=open(dst, "w")
    flag=0
    
    sp_idx_lst,num_lst, conc_lst =[],[],[]
    with open(src) as f:
        for num, line in enumerate(f,1):
            linesplit=line.split()
            if('STRESS PERIOD' in line):
                sp_idx_lst.append(num)
            if (len(linesplit) >= 8):
                if ('No obs wells active at current transport step' not in line):
                    if('WELLID' not in line):
                        if('dry cell' not in line):
                            conc_lst.append(linesplit)
                            num_lst.append(num)
    
    df = pd.DataFrame(conc_lst, columns= header)
    df['line_num'] = num_lst
    
    sp_idx = sp_idx_lst[::5] #drop repeated SP indices for transport steps (5)
    
    #make a dictionary between SP indices and actual SP values
    SPdict = {sp_idx[i]: list(range(1,145))[i] for i in range(len(sp_idx))} 
    
    #%%
    temp = []
    
    for row in df.iterrows():
        for i,val in enumerate(sp_idx): #[:-1]
            if i == 143 and row[1].num >= 12218:
                row[1].sp = sp_idx[i]
                temp.append(SPdict[row[1].sp])
            elif i < 143:
                if row[1].num >= sp_idx[i] and row[1].num < sp_idx[i+1]:
                    row[1].sp = val
                    temp.append(SPdict[row[1].sp])
    df['SP'] = temp
#%%



# for t in temp:
#     df['SP'] = SPdict[t]

#%%%    


# ok.drop_duplicates(inplace=True)
# ok[8] = ok[8].astype('|S') 
# ok2 = ok[ok[8] != b' [No obs wells active at current transport step]\n']
# # for col in cols:
# ok2[0] = ok2[0].str.split('      ').apply(lambda x: float(x[2])) #SP
# ok2[1] = ok2[1].str.split('      ').apply(lambda x: float(x[2])) #TS
# ok2[2] = ok2[2].str.split('      ').apply(lambda x: float(x[1])) #transport step
# ok2[3] = ok2[3].str.split('    ').apply(lambda x: float(x[1])) #times
# header = ok2.iloc[0,6]
# ok2.drop(axis=1, columns=[4,5,6,7], inplace=True)


#%%
# for row in ok.iterrows():
#     print(row[1][8])
#     if (row[1][8] == b' [No obs wells active at current transport step]\n'):
#         ok2 = ok.drop(row[0])



#%%
# with open(src) as f:
#     orig = f.readlines()

# newf = open(dst, "w")

# write = True
# first_time = True

# with open(src) as f, open(dst, "w") as newf:
#     for line in f:
#       if first_time == True:
#           if 'STRESS' in line:
#               first_time = False
#               write = False
#               for i in range(1):
#                   newf.write(
#                   '\n  -------------------- MIDDLE OF THE FILE -------------------')
#               print('\n\n')
#       if 'STRESS' in line: write = True
#       if write: newf.write(line)
# print('Done.')


#%%
# fo=open(dst, "w")
# flag=0
# with open(src) as f:
#     for line in f:
#         linesplit=line.split()
#         print(linesplit)
#         if('STRESS' in line): 
#             flag=1
#             newList=[]
#             print(line)
#         if((flag==1)  & (linesplit[0]!='STRESS')):
#             newList.append(line)        
#         # printing part
#         if(linesplit[0]!='STRESS'):
#             fo.write(line)
#         elif(linesplit[0]=='STRESS'):
#             for item in newList:
#                 fo.write("%s" % item)
# fo.close()

# final_df = pd.read_csv(dst)
