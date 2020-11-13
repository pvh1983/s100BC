import os
import pandas as pd
import fileinput
from shutil import copyfile


def AWLN(cutoff_sp):
    ifile = f'../../final_deliverables/preprocess/head_2020/targets.csv'
    ofile_ins = 'output/pst_ins/Head_AWLN.ins'

    # read and process data
    df = pd.read_csv(ifile)
    df2 = pd.DataFrame()
    df2['Well Name'] = df.agg(lambda x: f"{x['well']}_{x['sp']}", axis=1)
    df2['Val'] = df['target']
    df2['Weight'] = 0
    df2['Group'] = 'Head_AWLN'

    # Assign weight
    df2['Weight'][df['sp'] <= cutoff_sp] = 2

    # write to file
    # df2.to_csv('../pst/obs4pst.csv', index=False, sep='\t')
    print(f'Nobs = {df2.shape[0]}\n')

    # write to ins file
    df_ins = pd.DataFrame(columns=['pif', '#'])
    df_ins['#'] = df2['Well Name']
    df_ins['pif'] = 'l1'
    df_ins['#'] = df_ins.agg(
        lambda x: f"[{x['#']}]40:48", axis=1)
    # Write instruction file
    df_ins.to_csv(ofile_ins, index=False, sep='\t')
    return df2


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


def func_dirn_targets(ipst_2012_2014, pst_obs_cols, nsp):
    """
    Get pst block and ins files for dirn targets
    """
    # Get weigth from 2014-2014 pst control file

    df_pst1224 = pd.read_csv(ipst_2012_2014, skiprows=2047, sep=' ',
                             nrows=cutoff_sp, skipinitialspace=True,
                             names=pst_obs_cols)
    #
    list_dirn_targets = ['dirn_SRC', 'dirn2_SRC', 'dirn4_SRC', 'dirn_CRV']
    dic_dirn_targets = {'dirn_SRC': [45, 0.03], 'dirn2_SRC': [45, 0],
                        'dirn4_SRC': [85, 0.05], 'dirn_CRV': [45, 0]}

    dic_ofile = {'dirn_SRC': 'dirn_src_100C7_1', 'dirn2_SRC': 'dirn_src_100C7_1_2',
                 'dirn4_SRC': 'dirn_src_100C7_1_4', 'dirn_CRV': 'curve_plume_dirn'}

    list_dirn_name = ['sdirn', 'sdirn2_', 'sdirn4_', 'cdirn']

    df_dirn = pd.DataFrame(columns=pst_obs_cols)
    for i, dirn_target in enumerate(list_dirn_targets):
        df_dirn_tmp = pd.DataFrame(columns=pst_obs_cols)
        df_dirn_tmp['Well Name'] = [
            f'{list_dirn_name[i]}{sp+1}' for sp in range(nsp)]
        df_dirn_tmp['Val'] = dic_dirn_targets[dirn_target][0]
        df_dirn_tmp['Group'] = dirn_target
        df_dirn_tmp['Weight'] = dic_dirn_targets[dirn_target][1]
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
        df_ins = pd.DataFrame(columns=['c1', 'c2', 'c3'])
        df_ins['c3'] = df_dirn_tmp['Well Name']
        df_ins['c3'] = df_ins.agg(
            lambda x: f"# !{x['c3']}!", axis=1)
        df_ins['c1'] = '#'
        df_ins['c2'] = '# #'
        df_ins.to_csv(ofile_ins, mode='a', header=False, index=False, sep=',')
        print(f'Saved {ofile_ins}\n')

    return df_dirn


def Head_MAN(var):
    ifile = f'../../final_deliverables/Head_MAN/Bore_Sample_File_in_model_manual.csv'
    ofile_ins = 'output/pst_ins/Head_MAN.ins'

    # read and process data
    df = pd.read_csv(ifile, names=["well", "date", "time", "head"])
    df['num'] = list(range(1, len(df)+1))

    df2 = pd.DataFrame()
    df2['Well Name'] = df.agg(lambda x: f"MAN{x['num']}", axis=1)
    df2['Val'] = df['head']
    df2['Weight'] = 0
    df2['Group'] = 'Head_MAN'

    # Assign weight
    df2['Weight'][df['num'] <= cutoff_man_obs] = 1

    # write to file
    df2.to_csv('output/pst_ins/head_MAN4pst.csv', index=False, sep='\t')
    print(f'Nobs = {df2.shape[0]}\n')

    # write to ins file
    df_ins = pd.DataFrame(columns=['pif', '#'])
    df_ins['#'] = df2['Well Name']
    df_ins['pif'] = 'l1'
    df_ins['#'] = df_ins.agg(
        lambda x: f"[{x['#']}]40:48", axis=1)
    df_ins2 = df_ins.astype(str).apply(lambda x: '   '.join(x), axis=1)
    df_ins2.rename(' '.join(df_ins.columns)).to_csv(
        ofile_ins, header=True, index=False)
    # Write instruction file
    # df_ins.to_csv(ofile_ins, index=False, sep='\t')
    return df2


def magn_AWLN(cutoff_magn_AWLN):  # MP script
    # Define some input files/parameters
    ifile = f'../../final_deliverables/preprocess/Truex_well_network_2020/TruexWells_all_data_2012-2020_magdir.csv'
    ofile_ins = 'output/pst_ins/magn_AWLN.ins'
    # Delete the old file if existing
    # if os.path.isfile(ofile_ins):
    #     os.remove(ofile_ins)
    #     print(f'Removed {ofile_ins}\n')

    # read and process data
    df = pd.read_csv(ifile)
    df['num'] = list(range(1, len(df)+1))

    df2 = pd.DataFrame()
    df2['Well Name'] = df.agg(
        lambda x: f"magn{x['num']}", axis=1)
    df2['Val'] = df['magnitude']
    df2['Weight'] = 0
    df2['Group'] = 'magn_AWLN'

    # Assign weight
    df2['Weight'][df['num'] <= cutoff_magn_AWLN] = 10000

    # write to file
    df2.to_csv('output/pst_ins/magn_AWLN4pst.csv', index=False, sep='\t')
    print(f'Nobs = {df2.shape[0]}\n')

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


def dirn_AWLN(cutoff_magn_AWLN):  # MP script
    # Define some input files/parameters
    ifile = f'../../final_deliverables/preprocess/Truex_well_network_2020/TruexWells_all_data_2012-2020_magdir.csv'
    ofile_ins = 'output/pst_ins/dirn_AWLN.ins'
    # Delete the old file if existing
    if os.path.isfile(ofile_ins):
        os.remove(ofile_ins)
        print(f'Removed {ofile_ins}\n')

    # read and process data
    df = pd.read_csv(ifile)
    df['num'] = list(range(1, len(df)+1))

    df2 = pd.DataFrame()
    df2['Well Name'] = df.agg(
        lambda x: f"dirn{x['num']}", axis=1)
    df2['Val'] = df['direction']
    df2['Weight'] = 0
    df2['Group'] = 'dirn_AWLN'

    # Assign weight
    df2['Weight'][df['num'] <= cutoff_magn_AWLN] = 0.06

    # write to file
    df2.to_csv('output/pst_ins/dirn_AWLN4pst.csv', index=False, sep='\t')
    print(f'Nobs = {df2.shape[0]}\n')

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


def dirn3_SRC(cutoff_magn_AWLN):  # MP's script
    # Define some input files/parameters
    ifile = f'../../final_deliverables/sdirn/Bore_Sample_File_in_model_100C7_1_dirn3.csv'
    ofile_ins = 'output/pst_ins/dirn_src_100C7_1_3.ins'
    # Delete the old file if existing
    if os.path.isfile(ofile_ins):
        os.remove(ofile_ins)
        print(f'Removed {ofile_ins}\n')

    # read and process data
    df = pd.read_csv(ifile)
    df['num'] = list(range(1, len(df)+1))

    df2 = pd.DataFrame()
    df2['Well Name'] = df.agg(
        lambda x: f"sdirn3_{x['num']}", axis=1)
    df2['Val'] = 75.000
    df2['Weight'] = 0
    df2['Group'] = 'dirn3_SRC'

    # Assign weight
    df2['Weight'][df['num'] <= cutoff_magn_AWLN] = 0.04

    df2 = df2.iloc[0:102]  # cut values at 102 until you hear back from Helal.
    # write to file
    #df3.to_csv('output/pst_ins/dirn3_src4pst.csv', index=False, sep='\t')
    #print(f'Nobs = {df2.shape[0]}\n')

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

    # cut values at 102 until you hear back from Helal.
    df_ins2 = df_ins.iloc[0:102]
    # Write instruction file
    df_ins2.to_csv(ofile_ins, mode='a', header=False, index=False, sep=',')
    return df2


if __name__ == "__main__":
    # cd c:\Users\hpham\OneDrive - INTERA Inc\projects\020_100BC\hpham\scripts\
    # Define some init pars
    cutoff_sp = 113
    nsp = 384
    pst_obs_cols = ['Well Name', 'Val', 'Weight', 'Group']
    # List of targets
    list_targets = ['Head_AWLN', 'Head_MAN', 'Delta_4-14',
                    'Delta_5-8', 'Delta_8-6', 'magn_AWLN', 'dirn_AWLN',
                    'Head_182B', '100C7_Vel', 'plm_vel', 'plm_dir',
                    'dirn_SRC', 'dirn2_SRC', 'dirn3_SRC', 'dirn4_SRC', 'dirn_CRV']
    ipst_2012_2014 = 'input/100BC_GWM_calib7b.pst'
    df_pst_final = pd.DataFrame(columns=pst_obs_cols)
    # Get diff targets

    # [1] AWLN target 1
    df_AWLN = AWLN(cutoff_sp)

    # MP [2] Head_MAN
    cutoff_man_obs = 241  # length of extended model: 1172
    df_Head_MAN = Head_MAN(cutoff_man_obs)

    # MP [4] magn_AWLN and dirns_AWLN
    cutoff_magn_AWLN = 102  # length of extended model: 285
    df_magn_AWLN = magn_AWLN(cutoff_magn_AWLN)
    df_dirn_AWLN = dirn_AWLN(cutoff_magn_AWLN)

    # MP [5]
    # using cutoff_magn_AWLN for truex network number of overlapping SPs.
    # actual length of dirn3: 436, extended model: 1306
    df_dirn3_SRC = dirn3_SRC(cutoff_magn_AWLN)

    # [3] Delta_4-14, 'Delta_5-8', 'Delta_8-6',
    df_delta = Delta_targets(cutoff_sp)

    # [12] dirn_* targets
    df_dirn = func_dirn_targets(ipst_2012_2014, pst_obs_cols, nsp)

    # [] Read some groups that don't need to change 100C7_Vel, llm_vel, plm_dir
    # velocity1               5.11                  3          100C7_Vel
    # velocity2               3.68                  3          100C7_Vel
    #   plmvel               1.00                  9            plm_vel
    #   plmdir              45.00               0.21            plm_dir
    df_no_changes_group = pd.read_csv(ipst_2012_2014, skiprows=1930, sep=' ',
                                      nrows=4, skipinitialspace=True,
                                      names=pst_obs_cols)
    # Combine all groups
    df_pst_final = pd.concat(  # df_Head_MAN,
        [df_AWLN,  df_Head_MAN, df_delta, df_magn_AWLN, df_dirn_AWLN,
         df_no_changes_group, df_dirn, df_dirn3_SRC], axis=0)

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
