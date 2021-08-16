import pandas as pd
import numpy as np

bas = r"C:\Users\MPedrazas\OneDrive - INTERA Inc\020_100BC\mpedrazas\100BC_GWM\model_files\flow\100BC_5m_GeoV2_Evaluated_V3.bas"
btn = r"C:\Users\MPedrazas\OneDrive - INTERA Inc\020_100BC\mpedrazas\100BC_GWM\model_files\tran\100BC_2012_2020_tran_v2.btn"

# df_bas = pd.read_csv(bas, sep = "\s+", skiprows = 5, nrows=32584)
# df_btn = pd.read_csv(btn, sep = "\s+", skiprows = 93854, nrows=32584)

data, vals = [],[]
with open(bas,'r') as f:
    for num, line in enumerate(f,1):
        linesplit=line.split()
        if '1(25I3)' in linesplit:
            print('ignoring line: ', num)
        else:
            if ((num > 5) and (num < 32589)):
                vals.append(linesplit)
print('*'*25)
data.append(vals)
df_data = pd.DataFrame(data[0])
df_data = df_data.fillna(-1)
df_bas = df_data.astype(int)

data2, vals2 = [],[]
with open(btn,'r') as f:
    for num, line in enumerate(f,1):
        linesplit=line.split()
        if '1(25I3)' in linesplit:
            print('ignoring line: ', num)
        else:
            if ((num > 93854) and (num < 126438)):
                vals2.append(linesplit)
data2.append(vals2)
df_data2 = pd.DataFrame(data2[0])
df_data2 = df_data2.fillna(-1)
df_btn = df_data2.astype(int)

btn_arr = df_btn.to_numpy().flatten()
bas_arr = df_btn.to_numpy().flatten()

compare = bas_arr == btn_arr
equal_arr = compare.all()
print(equal_arr)






# lst = []
# for i in range(df_bas.shape[0]):
#     for j in range(df_bas.shape[1]):
#         lst.append(df_bas.iloc[i,j])




