import json
import os
import pandas as pd
from tqdm import tqdm

# ----------------------------------------------------------------
col_names = ['image_filename', 'lighting']
labels_path = '/mnt/w/prj/data/bdd100k/labels/bdd100k_labels_images_train.json'
data_path = '/mnt/w/prj/data/bdd100k/images/100k/train/'
csv_file = './data/bdd100k_real.csv'
# ----------------------------------------------------------------

def to_log(*args):
    with open('log.txt', 'a') as log:
        print(*args, file=log)

def get_labels_bdd(path):
    print('Loading labels', end='\r')
    with open(path) as data_file:
        labels = json.load(data_file)
    print('Loaded labels!', end='\r')
    return labels

def parse_labels_bdd(labels):
    df = pd.DataFrame(columns=col_names)

    to_log('-' * 50)
    for pic in tqdm(labels):
        img = pic['name']
        time = pic['attributes']['timeofday']
        if time == 'night':
            time = 'Night'
        elif time == 'daytime':
            time = 'Day'
        elif time == 'dawn/dusk':
            time = 'Twilight'
        else:
            to_log(time, img)
            continue
        df = df.append({"image_filename": img, "lighting": time}, ignore_index=True)
    return df
        # print(f'Append {i} lines to {csv_new}...', end='\r')

labels = get_labels_bdd(labels_path)
df = parse_labels_bdd(labels)
df.to_csv(csv_file, index=False, sep=',', encoding='utf8')
