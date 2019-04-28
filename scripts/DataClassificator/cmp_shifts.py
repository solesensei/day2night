import os
import pandas as pd 
import numpy as np

datapath = '/home/sole/gml/nexet/'
# -----------------------------

if not os.path.exists(datapath):
    raise FileExistsError(f'{datapath} not found')

dfs = []
for root,dirs,files in os.walk(datapath):
    print(root)
    for f in files:
        path = os.path.join(root, f)
        name = os.path.splitext(os.path.basename(f))[0]
        print('name:', name)
        df = pd.read_csv(path, sep=" ")
        df.columns = [name]
        dfs.append(df)

dfs = pd.concat(dfs, axis=1)
print(dfs.head())
print(dfs.columns)
# for k,v in dfs.items():
#     if len(v) != 2:
#         print(f'{k} has {len(v)} files, can\'t compare')
#         continue
#     df1 = v[0]#.reset_index(drop=True)
#     df2 = v[1]#.reset_index(drop=True)
#     # print(df1.head)
#     # print(df1.columns)
#     df = df1.concat(df2)
#     print(len(df))
#     df.reset_index(inplace=True)
#     print(len(df))
#     m = pd.merge(df1, df2, on=['name'], how='inner')
#     print(len(df2))
#     df2 = df2[(df2!=df1)].dropna(how='all')
#     print(len(df2))
#     print(len(mergedStuff))
#     ne_stacked = (df1 != df2).stack()
#     changed = ne_stacked[ne_stacked]
#     difference_locations = np.where(df1 != df2)
#     changed_from = df1.values[difference_locations]
#     changed_to = df2.values[difference_locations]
#     t = pd.DataFrame({'from': changed_from, 'to': changed_to}, index=changed.index)
#     print(t)
#     break