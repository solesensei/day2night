import os, sys
import pandas as pd
from shutil import copy, move

csv = './diffs.csv'
datadir = '../../../data/nexet/'

df = pd.read_csv(csv, sep=',', encoding='utf8', skipinitialspace=True)

if not os.path.isdir('dismatch'):
    os.mkdir('dismatch')
if not os.path.isdir('dismatch/day'):
    os.mkdir('dismatch/day')
if not os.path.isdir('dismatch/night'):
    os.mkdir('dismatch/night')
if not os.path.isdir('dismatch/twilight'):
    os.mkdir('dismatch/twilight')

num = len(df)
already_processed = 0
for r,_,f in os.walk('dismatch'):
    print(r, len(f))
    already_processed += len(f)
print(already_processed)
print(num - already_processed, 'processed', end='\r')
for r,d,f in os.walk(datadir):
    for i, file in enumerate(f):
        if file.endswith('.jpg') and df.image_filename.str.contains(file).any():
            row = df.loc[df.image_filename == file]
            dst = f'dismatch/{str(row.lighting_was.values[0]).lower()}/{file[:-4]}_{row.lighting_now.values[0]}_{row.pixels_light.values[0]}.jpg'
            df = df[~df.image_filename.str.contains(file)]
            print(f'{num - len(df)} processed', end='\r')
            if not os.path.exists(dst):
                src = os.path.join(r, file)
                copy(src, dst)
            
print(f'{num - len(df)} moved! {len(df)} last')

    
