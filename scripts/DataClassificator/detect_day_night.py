import os
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ------------- Parametrs -------------
img_root = "/mnt/W/prj/data/nexet/"
# -------------------------------------

hist_values = []
def detect_time(img):
    global hist_values
    frame = cv2.imread(img)
    n = np.sum(np.sum(frame))/(frame.shape[0]*frame.shape[1]*frame.shape[2])
    hist_values.append(round(n))

    if n > 68.0:
        return 'Day'
    elif 60 < n <= 68:
        return 'Twilight'
    else:
        return 'Night'


def main():
    
    df = pd.DataFrame(columns=['pathname', 'time'])
    
    for root, _, images in os.walk(img_root):
        print(f'{root} processing...')
        i = 0 
        for img in images:
            if i % 100 == 0:
                print(f'{i * 100 // len(images)}% processed', end='\r')
            if img.endswith(('.jpg', '.png', '.jpeg')):
                i += 1
                path_to_img = os.path.join(root, img)
                time = detect_time(path_to_img)
                df = df.append({"pathname" : path_to_img, "time" : time}, ignore_index=True)
        print(f'Append {i} lines to csv...', end='\r')
        df.to_csv("file.csv", index=False, sep=',', encoding='utf8')
        df.iloc[0:0]
        print(f'{root} processed!')
    
    print('Building histograms...')
    plt.hist(hist_values, bins=180)
    plt.savefig("histogram180")
    plt.hist(hist_values, bins=60)
    plt.savefig("histogram60")
    plt.hist(hist_values, bins=20)
    plt.savefig("histogram20")
    
    print('Saving data to .csv')
    df.to_csv("file.csv", index=False, sep=',', encoding='utf8')
    
    print('Completed')


if __name__ == "__main__":
    main()
