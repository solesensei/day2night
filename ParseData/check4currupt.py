# Script checking and moving currupted images to special directory
import os, sys
from shutil import move
from PIL import Image

datapath = '/content/drive/datasets/nexet/nexet_2017_1/' # path to dataset directory
curr_dir = '/content/drive/datasets/nexet/currupted'

if not os.path.exists(curr_dir):
    os.mkdir(curr_dir)

with open('log.txt', 'a') as log:
    print('-------- check currupted ----------', file=log)
    curr_count = {}
    for root, _, files in os.walk(datapath):
        print(f'Checking {root} : ', file=log, end='')
        print(f'Checking {root} : ', end='')
        curr_count[root] = 0
        for file in files:
            try:
                src = os.path.join(datapath, file)
                img = Image.open(src) 
                img.verify()
            except (IOError, SyntaxError) as e:
                curr_count[root] += 1
                move(src, curr_dir)
                print(f'currupted move: {src} → {curr_dir}', file=log)
        print(curr_count[root], 'errors', file=log)
        print(curr_count[root], 'errors')
    num_errors = sum(v for v in curr_count.values())
    print(f'Number of currupted files: {num_errors}', file=log)
print('Completed!')