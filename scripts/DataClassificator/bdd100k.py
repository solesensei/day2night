import json
import os
import pandas as pd

# ----------------------------------------------------------------
col_names = ['image_filename', 'lighting', 'pixels_light']
labels_path = 'bdd100k/labels/bdd100k_labels_images_train.json'
data_path = 'bdd100k/images/100k/train/'
csv_file = 'bdd100k_real.csv'
# ----------------------------------------------------------------

def get_labels_bdd(path):
    with open(path) as data_file:
        labels = json.load(data_file)
    # if not isinstance(labels, Iterable):
        # labels = [labels]
    return labels

def parse_labels_bdd(labels):
    df = pd.DataFrame(columns=col_names)
    
    if 'attributes' in labels:
         attr = labels['attributes']

    for name in labels:
        print(name)
        break
    return df
    # df = df.append({"image_filename": img, "lighting": time, "pixels_light": light}, ignore_index=True)
        # print(f'Append {i} lines to {csv_new}...', end='\r')

labels = get_labels_bdd(data_path)
df = parse_labels_bdd(labels)

df.to_csv(csv_file, index=False, sep=',', encoding='utf8')
# df.iloc[0:0]
print(f'{root} processed!')
