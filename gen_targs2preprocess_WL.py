import pandas as pd
import os

###### prepare {well}_targets.csv for truex well netowrk pre-processing

def prep_file2preprocess(path2mod2obs,path2sp, wells):

    #%% look at sp start and end to make procDate for truex well network pre-processing
    sp = pd.read_csv(path2sp, delimiter=',')
    awln_df = pd.read_csv(path2mod2obs, delimiter=',', names = ["WELL_NAME", "Date", "Time", "Head (m)"])
    awln_df['Date'] = pd.to_datetime(awln_df['Date'])
    sp = sp.iloc[:, 0:3] #get first three cols
    sp['start'] = pd.to_datetime(sp['start'], format='%y%m%d').dt.date
    sp['end'] = pd.to_datetime(sp['end'], format='%y%m%d').dt.date

    deltas = []
    for i in range(0, len(sp)):
        a = sp['start'].iloc[i] + ((sp['end'].iloc[i] - sp['start'].iloc[i])/2)
        deltas.append(a)
    sp_new = sp.assign(procdate=deltas)

    for well in wells:
        print(well)
        df = awln_df[awln_df['WELL_NAME'] == well]
        df.Date = df.Date.dt.date
        truex_targs = df.merge(sp_new, left_on = 'Date', right_on='end', how = 'left')
        print(len(truex_targs))
        truex_targs.drop(columns = ['Date','start','end','sp','Time'], inplace=True)
        truex_targs['date/time'] = truex_targs['procdate']
        truex_targs = truex_targs[['WELL_NAME','procdate','date/time','Head (m)']] #keep certain cols
        truex_targs.rename(columns={'WELL_NAME':'well_name', 'Head (m)':'wlevel'},inplace=True) #rename cols
        truex_targs.to_csv(os.path.join(inputDir, "targets", f'{well}_2012-2020_targets.csv'), index=False) #csv file for pp truex
    return None

if __name__ == "__main__":
    cwd = os.getcwd()
    inputDir = os.path.join(os.path.dirname(cwd), "Update.Predictive.Model", "2006-2020_pred170", "03_evalGrad", "preprocess")
    path2mod2obs = os.path.join(inputDir, 'Bore_Sample_File_in_model_AWLN.csv')
    path2sp = os.path.join(inputDir, 'stress_periods.csv')
    wellDict = {'NorthWells': ['199-B5-1', '199-B3-51', '199-B3-50'],
                'SouthWells': ['199-B4-14', '199-B5-8', '199-B8-6'],
                'CenterWells': ['199-B5-1', '199-B4-16', '199-B3-50']}
    for key in list(wellDict.keys()):
        print(key)
        prep_file2preprocess(path2mod2obs, path2sp, wellDict[key])

    ### Last step: Manually make date/time column in target csv numeric using Excel.