# Script checking and moving corrupted images to special directory
import os
from shutil import move
from PIL import Image

datapath = '/mnt/w/prj/data/nexet/nexet_2017_1'  # path to dataset directory
corr_dir = '/mnt/w/prj/data/nexet/corrupted'

if not os.path.exists(corr_dir):
    print(f'Creating {os.path.abspath(corr_dir)} directory')
    os.mkdir(os.path.abspath(corr_dir))

with open('log.txt', 'a') as log:
    print('-------- check corrupted ----------', file=log)
    corr_count = {}
    for root, _, files in os.walk(datapath):
        print(f'Checking {root} : ', file=log, end='')
        print(f'Checking {root} : ')
        corr_count[root] = 0
        for i, file in enumerate(files):
            if i % 100 == 0:
                print(f'{i} processed {corr_count[root]} corrupted', end='\r')
            try:
                src = os.path.join(root, file)
                img = Image.open(src)
                img.verify()
            except (IOError, SyntaxError) as e:
                corr_count[root] += 1
                move(src, corr_dir)
                print(f'corrupted move: {src} → {corr_dir}', file=log)
        print(corr_count[root], 'errors', file=log)
        print()
    num_errors = sum(v for v in corr_count.values())
    print(f'Number of corrupted files: {num_errors}', file=log)
    print(f'Number of corrupted files: {num_errors}')
print('Completed!')
