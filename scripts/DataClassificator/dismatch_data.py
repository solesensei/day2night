import os, sys
import pandas as pd
from shutil import copy, move

csv = './diffs.csv'
datadir = '../../data/nexet/'

df = pd.read_csv(csv, sep=',', encoding='utf8', skipinitialspace=True)

if not os.path.isdir('dismatch'):
    os.mkdir('dismatch')
if not os.path.isdir('dismatch/day'):
    os.mkdir('dismatch/day')
if not os.path.isdir('dismatch/night'):
    os.mkdir('dismatch/night')
if not os.path.isdir('dismatch/twilight'):
    os.mkdir('dismatch/twilight')

for r,d,f in os.walk(datadir):
    for file in f:
        if df.image_filename.str.contains(file).any():
            row = df.loc[df.image_filename == file]
            dst = f'dismatch/{str(row.lighting_was).lower()}/{row.lighting_now}_{row.pixels_light}.jpg'
            src = os.path.join(r, file) 
            # move(src, dst)
            print(f'{src} -> {dst}')

    