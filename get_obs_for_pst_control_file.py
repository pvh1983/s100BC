import os
import pandas as pd
import fileinput
from shutil import copyfile

def Head_AWLN():
    ifile = f'../../../../../final_deliverables/preprocess/head_2020/targets.csv'
    ofile_ins = 'output/pst_ins/Head_AWLN.ins'

    # read and process data
    df = pd.read_csv(ifile)

    df2 = pd.DataFrame()
    df2['Well Name'] = df.agg(lambda x: f"{x['well']}_{x['sp']}", axis=1)
    df2['Val'] = df['target']
    df2['Weight'] = 0
    df2['Group'] = 'Head_AWLN'

    # Assign weight:
    # Get weight from old pst file
    df_pst1224 = pd.read_csv(ipst_2012_2014, skiprows=155, sep=' ',
                             nrows=892, skipinitialspace=True,
                             names=pst_obs_cols)  # 1005 if we include well 182-mon
    # must fix index for 199-B4-18_1:
    fix_idx = df_pst1224[df_pst1224['Weight'] > 120].index
    for i in range(0, len(df_pst1224.columns)-1):
        df_pst1224.iloc[fix_idx[0], i] = df_pst1224.iloc[fix_idx[0], i+1]
    df_pst1224.iloc[fix_idx[0], 3] = 'Head_AWLN'

    # Merge two df based on Well Name
    df_merge = pd.merge(df2, df_pst1224, how='left', on=[
                        'Well Name'], indicator=True)
    df_pst_final = df2.copy()
    df_pst_final['Weight'] = df_merge['Weight_y']
    df_pst_final['Weight'][df_pst_final['Weight'].isnull()] = 0

    # Find out which weights from pest file were not assigned properly. Issue with consistent well_name.
    df_merge2 = pd.merge(df2, df_pst1224, how='right',
                         on=['Well Name'], indicator=True)
    diff = df_merge2[df_merge2['_merge'] == 'right_only']  # well, sp
    # values of 0 for non-existent 199-b4-16 in old data, can ignore
    diff = diff[diff.Weight_y != 0]
    diff.reset_index(inplace=True, drop=True)

    # For trouble wells, assign weights correctly to new pest file:
    wells = ['199-B4-7', '199-B4-14', '199-B4-18',
             '199-B5-6', '199-B5-8', '199-B8-6']
    for well in wells:
        idx1 = diff[diff['Well Name'].str.contains(well)].index.values
        # print(len(idx1))
        idx2 = df_pst_final[df_pst_final['Well Name'].str.contains(
            well)].index.values
        # find idx of last row with a weight of 1, if it exists:
        if len(df_pst_final[(df_pst_final['Weight'] == 1) & (df_pst_final['Well Name'].str.contains(well))]) != 0:
            idx3 = df_pst_final[(df_pst_final['Weight'] == 1) & (
                df_pst_final['Well Name'].str.contains(well))].index.values[-1]

        # Assign weights to the first number of values in new data from old data
        if len(df_pst_final[(df_pst_final['Weight'] == 1) & (df_pst_final['Well Name'].str.contains(well))]) != 0:
            df_pst_final.Weight.iloc[idx3+1:idx3 +
                                     len(idx1)+1] = diff.Weight_y.iloc[idx1].tolist()
        else:
            df_pst_final.Weight.iloc[idx2[0:len(
                idx1)]] = diff.Weight_y.iloc[idx1].tolist()

    # write to file
    df_pst_final.to_csv('output/pst_ins/obs4pst.csv', index=False, sep='\t')
    print(f'Nobs = {df_pst_final.shape[0]}\n')

    # write to ins file
    df_ins = pd.DataFrame(columns=['pif', '#'])
    df_ins['#'] = df_pst_final['Well Name']
    df_ins['pif'] = 'l1'
    df_ins['#'] = df_ins.agg(
        lambda x: f"[{x['#']}]40:48", axis=1)
    # Write instruction file
    df_ins.to_csv(ofile_ins, index=False, sep='\t')
    return df_pst_final

def Delta_targets(cutoff_sp):
    # Define some input files/parameters
    ifile = '../../final_deliverables/preprocess/head_2020/deltas.csv'
    ofile_ins = 'output/pst_ins/Deltas_AWLN.ins'
    # Delete the old file if existing
    if os.path.isfile(ofile_ins):
        os.remove(ofile_ins)
        print(f'Removed {ofile_ins}\n')

    list_delta_targets = ['Delta_4-14', 'Delta_5-8', 'Delta_8-6']
    well_name = ['199-B4-14', '199-B5-8', '199-B8-6']

    # write first row of the ins file
    fid = open(ofile_ins, 'w')
    fid.write('pif #\n')
    fid.close()

    # read and process data
    df = pd.read_csv(ifile)
    df_delta = pd.DataFrame()
    for k, delta_target in enumerate(list_delta_targets):
        df2 = pd.DataFrame()
        df_filter = df[df['well'] == well_name[k]]
        df2['Well Name'] = df_filter.agg(
            lambda x: f"dta_{x['well']}_{x['sp']}", axis=1)
        df2['Val'] = df['delta']
        df2['Weight'] = 0
        df2['Group'] = delta_target

        # Assign weight
        df2['Weight'][df['sp'] <= cutoff_sp] = 2

        # write to file
        # df2.to_csv('../pst/obs4pst.csv', index=False, sep='\t')
        # print(f'Nobs = {df2.shape[0]}\n')
        df_delta = pd.concat([df_delta, df2], axis=0)

        # write ins df to the ins file
        df_ins = pd.DataFrame(columns=['c1', 'c2', 'c3'])
        df_ins['c3'] = df2['Well Name']
        df_ins['c3'] = df_ins.agg(
            lambda x: f"# !{x['c3']}!", axis=1)
        df_ins['c1'] = '#'
        df_ins['c2'] = '# #'
        # Write instruction file
        df_ins.to_csv(ofile_ins, mode='a', header=False, index=False, sep=',')
    return df_delta

def Head_MAN():
    ifile = f'../../final_deliverables/Head_MAN/Bore_Sample_File_in_model_manual.csv'
    ifile2 = f'../../final_deliverables/Head_MAN/Bore_Sample_File_in_model_manual_2014.csv'
    ofile_ins = 'output/pst_ins/Head_MAN.ins'

    # read and process new and old data
    df = pd.read_csv(ifile, names=["well", "date", "time", "head"])
    df['num'] = list(range(1, len(df)+1))
    df_old = pd.read_csv(ifile2, names=["well", "date", "time", "head"])

    # merge dfs to create a column to differentiate new vs old observation points:
    df2 = df.merge(df_old, how='left', left_index=False,
                   indicator=True, on=['well', 'date', 'time', 'head'])
    drop = df2[df2.duplicated() == True]  # drop a duplicated value
    df2.drop(drop.index[:], inplace=True)
    df2.reset_index(inplace=True, drop=True)

    df3 = pd.DataFrame()
    df3['Well Name'] = df2.agg(lambda x: f"MAN{x['num']}", axis=1)
    df3['Val'] = 0
    df3['Weight'] = 0
    df3['Group'] = 'Head_MAN'

    # Find indices in merged dataframe that belong to old head data
    tmp = df2[df2['_merge'] == 'both']
    vals = df2.iloc[tmp.index[:]]['head'].values.tolist()

    # Assign weight and value
    df3['Weight'][df2['_merge'] == 'both'] = 1
    df3['Weight'][(df2['well'] == '199-B4-14') & (df2['date'] ==
                                                  '4/8/2013')] = 0.01  # special case - low head
    df3['Val'][df2['_merge'] == 'both'] = vals
    df3['Val'] = df3['Val'].round(3)

    # write to file
    # df3.to_csv('output/pst_main/head_MAN4pst.csv', index=False, sep='\t')
    # print(f'Nobs = {df3.shape[0]}\n')

    # write to ins file
    df_ins = pd.DataFrame(columns=['pif', '#'])
    df_ins['#'] = df3['Well Name']
    df_ins['pif'] = 'l1'
    df_ins['#'] = df_ins.agg(
        lambda x: f"[{x['#']}]40:48", axis=1)
    df_ins2 = df_ins.astype(str).apply(lambda x: '   '.join(x), axis=1)
    df_ins2.rename(' '.join(df_ins.columns)).to_csv(
        ofile_ins, header=True, index=False)
    return df3

def magn_AWLN(cutoff_truex):
    # Define some input files/parameters
    ifile = f'../../../../../final_deliverables/preprocess/Truex_well_network_2020/TruexWells_all_data_2012-2020_magdir.csv'
    ofile_ins = 'output/pst_ins/magn_AWLN.ins'
    # Delete the old file if existing
    if os.path.isfile(ofile_ins):
        os.remove(ofile_ins)
        print(f'Removed {ofile_ins}\n')

    # read and process data
    df = pd.read_csv(ifile)
    df['num'] = list(range(1, len(df)+1))

    df2 = pd.DataFrame()
    df2['Well Name'] = df.agg(
        lambda x: f"magn{x['num']}", axis=1)
    df2['Val'] = df['magnitude'].round(10)
    df2['Weight'] = 0
    df2['Group'] = 'magn_AWLN'

    # Assign weight
    df2['Weight'][df['num'] <= cutoff_truex] = 10000

    # write to file
    #df2.to_csv('output/pst_main/magn_AWLN4pst.csv', index=False, sep='\t')
    #print(f'Nobs = {df2.shape[0]}\n')

    # write ins df to the ins file
    # write first row of the ins file
    fid = open(ofile_ins, 'w')
    fid.write('pif #\n')
    fid.close()
    df_ins = pd.DataFrame(columns=['c1', 'c2', 'c3'])
    df_ins['c3'] = df2['Well Name']
    df_ins['c3'] = df_ins.agg(
        lambda x: f"# !{x['c3']}!", axis=1)
    df_ins['c1'] = '#'
    df_ins['c2'] = '# #'
    # Write instruction file
    df_ins.to_csv(ofile_ins, mode='a', header=False, index=False, sep=',')
    return df2

def dirn_AWLN(cutoff_truex, ipst_2012_2014):
    # Define some input files/parameters
    ifile = f'../../../../../final_deliverables/preprocess/Truex_well_network_2020/TruexWells_all_data_2012-2020_magdir.csv'
    ofile_ins = 'output/pst_ins/dirn_AWLN.ins'
    # Delete the old file if existing
    if os.path.isfile(ofile_ins):
        os.remove(ofile_ins)
        print(f'Removed {ofile_ins}\n')

    # read in weight column from pest file:
    df_pst1224 = pd.read_csv(ipst_2012_2014, skiprows=1828, sep=' ',
                             nrows=cutoff_truex, skipinitialspace=True,
                             names=pst_obs_cols)
    # read and process data
    df = pd.read_csv(ifile)
    df['num'] = list(range(1, len(df)+1))

    df2 = pd.DataFrame()
    df2['Well Name'] = df.agg(
        lambda x: f"dirn{x['num']}", axis=1)
    df2['Val'] = df['direction'].round(5)
    df2['Weight'] = 0
    df2['Group'] = 'dirn_AWLN'

    # Assign weight from pst file:
    df2['Weight'].iloc[0:cutoff_truex] = df_pst1224['Weight'].round(2)

    # make df2['Val'] = 20 for dirn 40-42, 45-49, 77-82
    df2['Val'].iloc[df2[df2['Weight'] == 0.03].index] = 20.00000

    # write to file
    # df2.to_csv('output/pst_main/dirn_AWLN4pst.csv', index=False, sep='\t')
    # print(f'Nobs = {df2.shape[0]}\n')

    # write ins df to the ins file
    # write first row of the ins file
    fid = open(ofile_ins, 'w')
    fid.write('pif #\n')
    fid.close()
    df_ins = pd.DataFrame(columns=['c1', 'c2', 'c3', 'c4'])
    df_ins['c4'] = df2['Well Name']
    df_ins['c4'] = df_ins.agg(
        lambda x: f"# !{x['c4']}!", axis=1)
    df_ins['c1'] = '#'
    df_ins['c2'] = '# #'
    df_ins['c3'] = '# #'
    # Write instruction file
    df_ins.to_csv(ofile_ins, mode='a', header=False, index=False, sep=',')
    return df2

def dirn3_SRC(cutoff_truex):
    # Define some input files/parameters
    ifile = f'../../final_deliverables/sdirn/Bore_Sample_File_in_model_100C7_1_dirn3.csv'
    ifile2 = f'../../final_deliverables/sdirn/Bore_Sample_File_in_model_100C7_1_dirn3_2014.csv'
    ofile_ins = 'output/pst_ins/dirn_src_100C7_1_3.ins'
    # Delete the old file if existing
    if os.path.isfile(ofile_ins):
        os.remove(ofile_ins)
        print(f'Removed {ofile_ins}\n')

    # read and process data
    df = pd.read_csv(ifile, names=["well", "date", "time", "head"])
    df['num'] = list(range(1, len(df)+1))
    df_old = pd.read_csv(ifile2, names=["well", "date", "time", "head"])

    # merge dfs to create a column to differentiate new vs old observation points:
    df2 = df.merge(df_old, how='left', left_index=False,
                   indicator=True, on=['well', 'date', 'time', 'head'])
    drop = df2[df2.duplicated() == True]  # drop a duplicated value
    df2.drop(drop.index[:], inplace=True)
    df2.reset_index(inplace=True, drop=True)

    df3 = pd.DataFrame()
    df3['Well Name'] = df2.agg(
        lambda x: f"sdirn3_{x['num']}", axis=1)
    df3['Val'] = 75.00000
    df3['Weight'] = 0
    df3['Group'] = 'dirn3_SRC'

    # Assign weight to 2012-2014 data only.
    # df3['Weight'][df2['_merge'] == 'both'] = 0.04
    df3['Weight'][df['num'] <= cutoff_truex] = 0.04

    n_dirn3 = 175  # extended model overlapping SPs from truex network
    # cut values to n_dirn3 --  need to confirm with Helal.
    df4 = df3.iloc[0:n_dirn3]
    # write to file
    #df4.to_csv('output/pst_main/dirn3_src4pst.csv', index=False, sep='\t')
    #print(f'Nobs = {df4.shape[0]}\n')

    # write ins df to the ins file
    # write first row of the ins file
    fid = open(ofile_ins, 'w')
    fid.write('pif #\n')
    fid.close()
    df_ins = pd.DataFrame(columns=['c1', 'c2', 'c3', 'c4'])
    df_ins['c4'] = df4['Well Name']
    df_ins['c4'] = df_ins.agg(
        lambda x: f"# !{x['c4']}!", axis=1)
    df_ins['c1'] = '#'
    df_ins['c2'] = '# #'
    df_ins['c3'] = '# #'

    # cut values to n_dirn3 --  need to confirm with Helal.
    df_ins2 = df_ins.iloc[0:n_dirn3]
    # Write instruction file
    df_ins2.to_csv(ofile_ins, mode='a', header=False, index=False, sep=',')
    return df4

def func_dirn_targets(ipst_2012_2014, pst_obs_cols, nsp):
    """
    Get pst block and ins files for dirn targets
    """
    # Get weight from 2014-2014 pst control file
    df_pst1224 = pd.read_csv(ipst_2012_2014, skiprows=2047, sep=' ',
                             nrows=cutoff_sp, skipinitialspace=True,
                             names=pst_obs_cols)
    #
    list_dirn_targets = ['dirn_SRC', 'dirn2_SRC', 'dirn4_SRC', 'dirn_CRV']
    dic_dirn_targets = {'dirn_SRC': [45, 0.03], 'dirn2_SRC': [45, 0],
                        'dirn4_SRC': [85, 0.05], 'dirn_CRV': [45, 0]}

    dic_ofile = {'dirn_SRC': 'dirn_src_100C7_1', 'dirn2_SRC': 'dirn_src_100C7_1_2',
                 'dirn4_SRC': 'dirn_src_100C7_1_4', 'dirn_CRV': 'curve_plume_dirn'}

    dic_ifile = {'dirn_SRC': '100C7_1_dirn', 'dirn2_SRC': '100C7_1_dirn2',
                 'dirn4_SRC': '100C7_1_dirn4', 'dirn_CRV': 'curve_plume'}

    list_dirn_name = ['sdirn', 'sdirn2_', 'sdirn4_', 'cdirn']

    df_dirn = pd.DataFrame(columns=pst_obs_cols)
    for i, dirn_target in enumerate(list_dirn_targets):
        ifile = f'../../../../../final_deliverables/sdirn/Bore_Sample_File_in_model_{dic_ifile[dirn_target]}.csv'
        ifile2 = f'../../../../../final_deliverables/sdirn/Bore_Sample_File_in_model_{dic_ifile[dirn_target]}_2014.csv'

        df = pd.read_csv(ifile, names=["well", "date", "time", "head"])
        df_old = pd.read_csv(ifile2, names=["well", "date", "time", "head"])
        df2 = df.merge(df_old, how='left', left_index=False,
                       indicator=True, on=['well', 'date', 'time', 'head'])

        df_dirn_tmp = pd.DataFrame(columns=pst_obs_cols)
        df_dirn_tmp['Well Name'] = [
            f'{list_dirn_name[i]}{sp+1}' for sp in range(nsp)]
        df_dirn_tmp['Val'] = dic_dirn_targets[dirn_target][0]
        df_dirn_tmp['Group'] = dirn_target
        df_dirn_tmp['Weight'] = 0
        # Assign weight to 2012-2014 data only:
        df_dirn_tmp['Weight'][df2['_merge'] ==
                              'both'] = dic_dirn_targets[dirn_target][1]
        if dirn_target == 'dirn2_SRC':  # a special case
            df_dirn_tmp['Weight'].iloc[0:cutoff_sp] = df_pst1224['Weight']
        # Combine dfs
        df_dirn = pd.concat([df_dirn, df_dirn_tmp], axis=0)
        df_dirn.to_csv('output/pst_ins/df_dirn.csv')

        # write ins df to the ins file
        # write first row of the ins file
        ofile_ins = f'output/pst_ins/{dic_ofile[dirn_target]}.ins'
        fid = open(ofile_ins, 'w')
        fid.write('pif #\n')
        fid.close()
        df_ins = pd.DataFrame(columns=['c1', 'c2', 'c3', 'c4'])
        df_ins['c4'] = df_dirn_tmp['Well Name']
        df_ins['c4'] = df_ins.agg(
            lambda x: f"# !{x['c4']}!", axis=1)
        df_ins['c1'] = '#'
        df_ins['c2'] = '# #'
        df_ins['c3'] = '# #'
        df_ins.to_csv(ofile_ins, mode='a', header=False, index=False, sep=',')
        print(f'Saved {ofile_ins}\n')

    return df_dirn

if __name__ == "__main__":
    # cwd c:\Users\hpham\OneDrive - INTERA Inc\projects\020_100BC\hpham\scripts\

    # Define some initial parameters:
    cutoff_sp = 113
    nsp = 384
    # List of targets
    list_targets = ['Head_AWLN', 'Head_MAN', 'Delta_4-14',
                    'Delta_5-8', 'Delta_8-6', 'magn_AWLN', 'dirn_AWLN',
                    'Head_182B', '100C7_Vel', 'plm_vel', 'plm_dir',
                    'dirn_SRC', 'dirn2_SRC', 'dirn3_SRC', 'dirn4_SRC', 'dirn_CRV']
    ipst_2012_2014 = '../input/100BC_GWM_calib7b.pst'
    pst_obs_cols = ['Well Name', 'Val', 'Weight', 'Group']

    # [1] Head_AWLN
    df_AWLN = Head_AWLN()

    # [2] Head_MAN
    # cutoff_man_obs = 241  # length of extended model: 1172
    df_Head_MAN = Head_MAN()

    # [3] magn_AWLN and dirns_AWLN
    cutoff_truex = 102  # length of extended model: 285
    df_magn_AWLN = magn_AWLN(cutoff_truex)
    df_dirn_AWLN = dirn_AWLN(cutoff_truex, ipst_2012_2014)

    # [4] dirn* 
    df_dirn = func_dirn_targets(ipst_2012_2014, pst_obs_cols, nsp)
    
    # [5] dirn3
    # using cutoff_truex for overlapping SPs - source_dirn3.csv
    df_dirn3_SRC = dirn3_SRC(cutoff_truex)

    # [6] Delta_4-14, 'Delta_5-8', 'Delta_8-6',
    df_delta = Delta_targets(cutoff_sp)

    # [7] Read some groups that don't need to change 100C7_Vel, llm_vel, plm_dir
    # velocity1               5.11                  3          100C7_Vel
    # velocity2               3.68                  3          100C7_Vel
    #   plmvel               1.00                  9            plm_vel
    #   plmdir              45.00               0.21            plm_dir
    
    df_no_changes_group = pd.read_csv(ipst_2012_2014, skiprows=1930, sep=' ',
                                      nrows=4, skipinitialspace=True,
                                      names=pst_obs_cols)
    # Combine all groups
    df_dirn1 = df_dirn[df_dirn['Group'] == 'dirn_SRC']
    df_dirn2 = df_dirn[df_dirn['Group'] == 'dirn2_SRC']
    df_dirn4 = df_dirn[df_dirn['Group'] == 'dirn4_SRC']
    df_CRV = df_dirn[df_dirn['Group'] == 'dirn_CRV']

    df_pst_final = pd.DataFrame(columns=pst_obs_cols)
    df_pst_final = pd.concat(
        [df_AWLN,  df_Head_MAN, df_delta, df_magn_AWLN, df_dirn_AWLN,
         df_no_changes_group, df_dirn1, df_dirn2, df_dirn3_SRC, df_dirn4, df_CRV], axis=0)

    # Save to file
    df_pst_final.to_csv('input/100BC_GWM_calib7b_par2.pst', header=False,
                        index=False, sep='\t')

    # Get pst file content before obs group
    copyfile('input/100BC_GWM_calib7b_par1_org.pst',
             'input/100BC_GWM_calib7b_par1.pst')

    filename = 'input/100BC_GWM_calib7b_par1.pst'
    n_new_obs = df_pst_final.shape[0]
    text_to_search = '2333'
    replacement_text = str(n_new_obs)
    with fileinput.FileInput(filename, inplace=True, backup='.bak') as file:
        for line in file:
            print(line.replace(text_to_search, replacement_text), end='')

    # Combine three files
    read_files = [f'input/100BC_GWM_calib7b_par{i+1}.pst' for i in range(3)]
    with open("input/100BC_GWM_calib_2012_2020.pst", "wb") as outfile:
        for f in read_files:
            with open(f, "rb") as infile:
                outfile.write(infile.read())
