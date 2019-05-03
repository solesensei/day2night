import os
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ------------- Parametrs -------------
img_root = "/mnt/w/prj/data/bdd100k/"
csv_new = "./data/bdd100k_train.csv"
csv_old = "./data/bdd100k_real.csv"
col_names = ['image_filename', 'lighting', 'pixels_light']
# -------------------------------------

hist_values = []


def detect_time(img):
    global hist_values
    frame = cv2.imread(img)
    n = np.sum(np.sum(frame)) / (frame.shape[0] * frame.shape[1] * frame.shape[2])
    hist_values.append(round(n))

    if n > 68.0:
        return 'Day', round(n)
    if 60 < n <= 68:
        return 'Twilight', round(n)
    return 'Night', round(n)


def compare_with_previous(csv):
    old = pd.read_csv(csv, sep=',', encoding='utf8', skipinitialspace=True)
    new = pd.read_csv(csv_new, sep=',', encoding='utf8', usecols=col_names, skipinitialspace=True)
    old = old.drop_duplicates(subset=['image_filename'])
    new = new.drop_duplicates(subset=['image_filename'])
    print('length are equal' if len(old) == len(new) else f'length are not equal ({len(old)},{len(new)})')
    print('------------')
    with open('./data/diffs.csv', 'a') as diff:
        merged = pd.merge(old, new, suffixes=('_was', '_now'), on=['image_filename'], how='inner')
        merged['status'] = np.where((merged['lighting_was'] == merged['lighting_now']), True, False)
        merged = merged[merged.status == False]
        merged = merged[['image_filename', 'lighting_was', 'lighting_now', 'pixels_light']]
        merged.pixels_light = merged.pixels_light.round()
        print(f'{len(merged)} mismatches detected! Writing to diffs.csv')
        merged.to_csv(diff, index=False, sep=',', encoding='utf8')
    print('Compared!')


def main():

    df = pd.DataFrame(columns=col_names, index=['image_filename'])

    if not os.path.exists(img_root):
        raise BaseException(f'No data {img_root} path found')

    for root, _, images in os.walk(img_root):
        print(f'{root} processing...')
        i = 0
        for img in images:
            if i % 100 == 0:
                print(f'{i * 100 // len(images)}% processed', end='\r')
            if img.endswith(('.jpg', '.png', '.jpeg')):
                i += 1
                if img in df.index:
                    continue
                path_to_img = os.path.join(root, img)
                time, light = detect_time(path_to_img)
                df = df.append({"image_filename": img, "lighting": time, "pixels_light": light}, ignore_index=True)
        print(f'Append {i} lines to {csv_new}...', end='\r')
        df.to_csv(csv_new, index=False, sep=',', encoding='utf8')
        df.iloc[0:0]
        print(f'{root} processed!')

    if hist_values:
        print('Building histograms...')
        plt.hist(hist_values, bins=180)
        plt.savefig("histogram180")
        plt.hist(hist_values, bins=60)
        plt.savefig("histogram60")
        plt.hist(hist_values, bins=20)
        plt.savefig("histogram20")

    print(f'Saving data to {csv_new}')
    df.to_csv(csv_new, index=False, sep=',', encoding='utf8')

    if csv_old:
        print(f'Comparing with {csv_old}')
        compare_with_previous(csv_old)

    print('Completed')


if __name__ == "__main__":
    main()
