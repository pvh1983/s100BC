import pandas as pd


list_sce = ['m1214', 'm1220']
List_ifiles = {'m1214', 'input/100BC_GWM_calib7b.pst',
               'm1220', 'input/100BC_GWM_calib_2012_2020.pst'}
pst_obs_cols = ['Well Name', 'Val', 'Weight', 'Group']
dlines = {'m1214': [155, 1047], 'm1220': [155, 4827]}

# Block for head_AWLN
for sce in list_sce:
    ifile = List_ifiles[sce]
    df_org = pd.read_csv(ifile, skiprows=dlines[sce][0], sep=' ',
                         nrows=dlines[sce][1]-dlines[sce][0], skipinitialspace=True,
                         names=pst_obs_cols)
    list_tmp = [df_org['Well Name'].iloc[i].split(
        '_')[0] for i in range(df_org.shape[0])]
    df = pd.DataFrame(columns=['Well Name'])
    df['Well Name'] = list_tmp
    wname = df['Well Name'].unique()
