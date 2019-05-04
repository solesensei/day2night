import os
from shutil import copy, move
import pandas as pd

csv = './bdd_diffs.csv'
datadir = '/mnt/w/prj/data/bdd100k/images/100k/train/'

df = pd.read_csv(csv, sep=',', encoding='utf8', skipinitialspace=True)

mismatch_dir = os.path.join(datadir, 'mismatch')
mismatch_day = os.path.join(mismatch_dir, 'day')
mismatch_night = os.path.join(mismatch_dir, 'night')
mismatch_twilight = os.path.join(mismatch_dir, 'twilight')

if not os.path.isdir(mismatch_dir):
    os.mkdir(mismatch_dir)
if not os.path.isdir(mismatch_day):
    os.mkdir(mismatch_day)
if not os.path.isdir(mismatch_night):
    os.mkdir(mismatch_night)
if not os.path.isdir(mismatch_twilight):
    os.mkdir(mismatch_twilight)

num_all = len(df)
already_processed = 0
for r, _, f in os.walk(mismatch_dir):
    print(r, len(f))
    already_processed += len(f)
print('Already processed:', already_processed)
with open('log.txt', 'a', encoding="utf-8") as log:
    print(f'---- start log ----', file=log)
    for r, d, f in os.walk(datadir):
        for i, file in enumerate(f):
            if file.endswith('.jpg') and df.image_filename.str.contains(file).any():
                row = df.loc[df.image_filename == file]
                dst = f'{datadir}/mismatch/{str(row.lighting_now.values[0]).lower()}/{file}'
                df = df[~df.image_filename.str.contains(file)]
                print(f'{num_all - len(df)} processed', end='\r')
                if not os.path.exists(dst):
                    lwas = str(row.lighting_was.values[0]).lower()
                    lnow = str(row.lighting_now.values[0]).lower()
                    print(f'{file[:-4]}\t{lwas}->{lnow} [{row.pixels_light.values[0]}]', file=log)
                    src = os.path.join(r, file)
                    move(src, dst)

print(f'{num_all - len(df)} moved! {len(df)} last')
