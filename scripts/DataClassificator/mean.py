import pandas as pd
import numpy as np

csvpath = './data/nexet_builded.csv'

csv = pd.read_csv(csvpath, sep=',', encoding='utf8', skipinitialspace=True)

print(len(csv))
csv_day = csv[csv.lighting == 'Day']
csv_night = csv[csv.lighting == 'Night']
mean_day = np.sum(csv_day.pixels_light) / len(csv_day)
mean_night = np.sum(csv_night.pixels_light) / len(csv_night)
max_day = np.max(csv_day.pixels_light)
min_day = np.min(csv_day.pixels_light)
max_night = np.max(csv_night.pixels_light)
min_night = np.min(csv_night.pixels_light)
mean = np.sum(csv.pixels_light) / len(csv)
print(f'Mean Day light  = {mean_day}    for {len(csv_day)} images')
print(f'Mean Night light= {mean_night}  for {len(csv_night)} images')
print(f'Max light       = {mean}        for {len(csv)} images')
print('----------------')
print(f'Day light range = {min_day}..{max_day}')
print(f'Night light range = {min_night}..{max_night}')
