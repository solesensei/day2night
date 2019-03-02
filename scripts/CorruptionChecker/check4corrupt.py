# Script checking and moving corrupted images to special directory
import os, sys
from shutil import move
from PIL import Image

datapath = '/mnt/W/prj/data/nexet/nexet_2017_1/' # path to dataset directory
curr_dir = '/mnt/W/prj/data/nexet/corrupted'

if not os.path.exists(curr_dir):
    os.mkdir(curr_dir)

with open('log.txt', 'a') as log:
    print('-------- check corrupted ----------', file=log)
    curr_count = {}
    for root, _, files in os.walk(datapath):
        print(f'Checking {root} : ', file=log, end='')
        print(f'Checking {root} : ', end='')
        curr_count[root] = 0
        for file in files:
            try:
                src = os.path.join(root, file)
                img = Image.open(src) 
                img.verify()
            except (IOError, SyntaxError) as e:
                curr_count[root] += 1
                move(src, curr_dir)
                print(f'corrupted move: {src} → {curr_dir}', file=log)
        print(curr_count[root], 'errors', file=log)
        print(curr_count[root], 'errors')
    num_errors = sum(v for v in curr_count.values())
    print(f'Number of corrupted files: {num_errors}', file=log)
print('Completed!')