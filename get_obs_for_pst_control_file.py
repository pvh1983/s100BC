import os
import pandas as pd


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
    return df


def Delta_targets(cutoff_sp):
    # Define some input files/parameters
    ifile = '../../final_deliverables/preprocess/head_2020/deltas.csv'
    ofile_ins = 'output/pst_ins/Deltas_AWLN.ins'
    # Delete the old file if existing
    if os.path.isfile(ofile_ins):
        os.remove(ofile_ins)
        print(f'Removed {ofile_ins}\n')

    list_delta_targets = ['Delta_4-14', 'Delta_5-8', 'Delta_8-6']

    # read and process data
    df = pd.read_csv(ifile)
    df_pst_final = pd.DataFrame()
    for delta_target in list_delta_targets:
        df2 = pd.DataFrame()
        df2['Well Name'] = df.agg(
            lambda x: f"dta_{x['well']}_{x['sp']}", axis=1)
        df2['Val'] = df['delta']
        df2['Weight'] = 0
        df2['Group'] = delta_target

        # Assign weight
        df2['Weight'][df['sp'] <= cutoff_sp] = 2

        # write to file
        # df2.to_csv('../pst/obs4pst.csv', index=False, sep='\t')
        # print(f'Nobs = {df2.shape[0]}\n')
        df_pst_final = pd.concat([df_pst_final, df2], axis=0)

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
    return df_pst_final


def func_dirn_targets():
    """
    Get pst block and ins files for dirn targets
    """
    # Get weigth from 2014-2014 pst control file
    pst_obs_cols = ['Well Name', 'Val', 'Weight', 'Group']
    df_pst1224 = pd.read_csv(ipst_2012_2014, skiprows=2047, sep=' ',
                             nrows=cutoff_sp, skipinitialspace=True,
                             names=pst_obs_cols)
    #
    list_dirn_targets = ['dirn_SRC', 'dirn2_SRC', 'dirn4_SRC', 'dirn_CRV']
    dic_dirn_targets = {'dirn_SRC': [45, 0.03], 'dirn2_SRC': [45, 0],
                        'dirn4_SRC': [85, 0.05], 'dirn_CRV': [45, 0]}

    dic_ofile = {'dirn_SRC': 'dirn_src_100C7_1', 'dirn2_SRC': 'dirn_src_100C7_2',
                 'dirn4_SRC': 'dirn_src_100C7_4', 'dirn_CRV': 'dirn_CRV'}

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
    print(f'xxx{var}')


if __name__ == "__main__":
    # Define some init pars
    cutoff_sp = 113
    nsp = 384
    # List of targets
    list_targets = ['Head_AWLN', 'Head_MAN', 'Delta_4-14',
                    'Delta_5-8', 'Delta_8-6', 'magn_AWLN', 'dirn_AWLN',
                    'Head_182B', '100C7_Vel', 'plm_vel', 'plm_dir',
                    'dirn_SRC', 'dirn2_SRC', 'dirn3_SRC', 'dirn4_SRC', 'dirn_CRV']
    ipst_2012_2014 = 'input/100BC_GWM_calib7b.pst'

    # Get diff targets
    # [1] AWLN target 1

    df_AWLN = AWLN(cutoff_sp)

    # [2] Head_MAN
    var = 'test'
    df_Head_MAN = Head_MAN(var)

    # [3] Delta_4-14, 'Delta_5-8', 'Delta_8-6',
    Delta_targets(cutoff_sp)

    # [12] dirn_* targets
    df_dirn = func_dirn_targets()

    # [] Read some groups that don't need to change 100C7_Vel, llm_vel, plm_dir
    # velocity1               5.11                  3          100C7_Vel
    # velocity2               3.68                  3          100C7_Vel
    #   plmvel               1.00                  9            plm_vel
    #   plmdir              45.00               0.21            plm_dir
