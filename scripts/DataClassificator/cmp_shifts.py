import os

datapath = '/home/sole/gml/nexet/'
# -----------------------------

if not os.path.exists(datapath):
    raise FileExistsError(f'{datapath} not found')

stack = []
for root,dirs,files in os.walk(datapath):
    print(root)
    if len(files) == 0:
        continue
    dfs = set()
    for f in files:
        path = os.path.join(root, f)
        name = os.path.splitext(os.path.basename(f))[0]
        print('name:', name)
        with open(path, 'r') as txt:
            for line in txt:
                dfs.add(line.strip())
    stack.append(dfs)

for s in stack:
    print(s.head())
    print(s.columns)


df1 = stack[0]
df2 = stack[1]


if (df1.columns != df2.columns).any():
    raise ValueError("Two dataframe columns must match")

if df1.equals(df2):
    df = None
else:
    df = pd.concat([df2, df1, df1]).drop_duplicates(keep=False)
    # df = pd.concat([df1, df2, df2]).drop_duplicates(keep=False)

print(df.head())
    # df1 = v[0]#.reset_index(drop=True)
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