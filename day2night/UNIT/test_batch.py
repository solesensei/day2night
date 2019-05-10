"""
Copyright (C) 2018 NVIDIA Corporation.  All rights reserved.
Licensed under the CC BY-NC-SA 4.0 license (https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode).
"""
from __future__ import print_function
from utils import get_config, get_data_loader_folder, pytorch03_to_pytorch04
from trainer import MUNIT_Trainer, UNIT_Trainer
import argparse
from subprocess import call
from torch.autograd import Variable
from data import ImageFolder
import torchvision.utils as vutils
try:
    from itertools import izip as zip
except ImportError: # will be 3.x series
    pass
from time import time
import sys
import torch
import os

def usage():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, help="path net configuration", required=True)
    parser.add_argument('--input_folder', type=str, help="input image folder", required=True)
    parser.add_argument('--output_folder', type=str, help="output image path", required=True)
    parser.add_argument('--checkpoint', type=str, help="checkpoint of autoencoders", required=True)
    parser.add_argument('--a2b', type=int, help="1 for a2b and others for b2a", default=1)
    parser.add_argument('--recon', action='store_true', help="save reconstructions too")
    parser.add_argument('--number', type=int, default=-1, help="Number of image to process, default: all")
    parser.add_argument('--seed', type=int, default=1, help="random seed")
    parser.add_argument('--num_style',type=int, default=10, help="number of styles to sample")
    parser.add_argument('--synchronized', action='store_true', help="whether use synchronized style code or not")
    parser.add_argument('--output_only', action='store_true', help="whether use synchronized style code or not")
    parser.add_argument('--output_path', type=str, default='.', help="path for logs, checkpoints, and VGG model weight")
    parser.add_argument('--trainer', type=str, default='UNIT', help="MUNIT|UNIT")
    parser.add_argument('--device', metavar='GPU', nargs='+', help='GPU List', default=["0"])
    return parser.parse_args()

opts = usage()

# Choose GPU device to run
os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID" 
os.environ["CUDA_VISIBLE_DEVICES"]=",".join(str(x) for x in opts.device)

torch.manual_seed(opts.seed)
torch.cuda.manual_seed(opts.seed)
if not os.path.exists(opts.output_folder):
    os.makedirs(opts.output_folder)

if not opts.output_only and not os.path.exists(os.path.join(opts.output_folder, 'input')):
    os.makedirs(os.path.join(opts.output_folder, 'input'))

# Print System Info 
print('CUDA Devices')
call(["nvidia-smi", "--format=csv", "--query-gpu=index,name,driver_version,memory.total,memory.used,memory.free"])
print(f'Available devices {torch.cuda.device_count()}: {", ".join(str(x) for x in opts.device)}')
print('Active CUDA Device: GPU', torch.cuda.current_device())

print('Load experiment setting')
config = get_config(opts.config)
input_dim = config['input_dim_a'] if opts.a2b else config['input_dim_b']

print('Setup model and data loader')
if 'new_size' in config:
    new_size = config['new_size']
else:
    if opts.a2b==1:
        new_size = config['new_size_a']
    else:
        new_size = config['new_size_b']
image_names = ImageFolder(opts.input_folder, transform=None, return_paths=True)
data_loader = get_data_loader_folder(opts.input_folder, 1, False, new_size=new_size, crop=False, num_workers=config['num_workers'])

config['vgg_model_path'] = opts.output_path
config['resnet_model_path'] = opts.output_path
if opts.trainer == 'MUNIT':
    style_dim = config['gen']['style_dim']
    trainer = MUNIT_Trainer(config)
elif opts.trainer == 'UNIT':
    trainer = UNIT_Trainer(config)
else:
    sys.exit("Only support MUNIT|UNIT")

try:
    state_dict = torch.load(opts.checkpoint)
    trainer.gen_a.load_state_dict(state_dict['a'])
    trainer.gen_b.load_state_dict(state_dict['b'])
except:
    state_dict = pytorch03_to_pytorch04(torch.load(opts.checkpoint))
    trainer.gen_a.load_state_dict(state_dict['a'])
    trainer.gen_b.load_state_dict(state_dict['b'])

trainer.cuda()
trainer.eval()

encode = trainer.gen_a.encode if opts.a2b else trainer.gen_b.encode # encode function
decode = trainer.gen_b.decode if opts.a2b else trainer.gen_a.decode # decode function
if opts.recon:
    decode_r = trainer.gen_b.decode if not opts.a2b else trainer.gen_a.decode # decode for reconstruction function

with torch.no_grad():
    t_start = time() 
    if opts.trainer == 'MUNIT':

        print('Start testing')
        style_fixed = Variable(torch.randn(opts.num_style, style_dim, 1, 1).cuda(), volatile=True)
        for i, (images, names) in enumerate(zip(data_loader, image_names)):
            print(f"{names[1]} -> {opts.output_folder}")
            images = Variable(images.cuda(), volatile=True)
            code, _ = encode(images)
            style = style_fixed if opts.synchronized else Variable(torch.randn(opts.num_style, style_dim, 1, 1).cuda(), volatile=True)
            for j in range(opts.num_style):
                s = style[j].unsqueeze(0)
                outputs = decode(code, s)
                outputs = (outputs + 1) / 2.
                # path = os.path.join(opts.output_folder, 'input{:03d}_output{:03d}.jpg'.format(i, j))
                basename = os.path.basename(names[1])
                path = os.path.join(opts.output_folder+"_%02d"%j,basename)
                if not os.path.exists(os.path.dirname(path)):
                    os.makedirs(os.path.dirname(path))
                vutils.save_image(outputs.data, path, padding=0, normalize=True)
            if not opts.output_only:
                # also save input images
                vutils.save_image(images.data, os.path.join(opts.output_folder, 'input/', "_%02d"%j,basename), padding=0, normalize=True)
        print('Testing Сomplete!')
    elif opts.trainer == 'UNIT':

        print('Start testing')
        for i, (images, names) in enumerate(zip(data_loader, image_names)):
            if opts.number != -1 and i >= opts.number:
                break
            bar = f"{names[1]}"
            print(f'{bar} --> encoding', ' '*20, end='\r')
            images = Variable(images.cuda(), volatile=True)
            code, _ = encode(images)
            if opts.recon:
                print(f'{bar} --> reconstructing', ' '*20, end='\r')
                reconstructed = decode_r(code)
                reconstructed = (reconstructed + 1) / 2.

            print(f'{bar} --> translating', ' '*20, end='\r')
            outputs = decode(code)
            outputs = (outputs + 1) / 2.

            print(f'{bar} --> saving', ' '*20, end='\r')
            basename = os.path.basename(names[1])
            path = os.path.join(opts.output_folder,basename)
            path_dir = os.path.dirname(path)
            if not os.path.exists(path_dir):
                os.makedirs(path_dir)
            vutils.save_image(outputs.data, path, padding=0, normalize=True)
            if not opts.output_only:
                if not os.path.exists(os.path.join(path_dir, 'input/')):
                    os.makedirs(os.path.join(path_dir, 'input/'))
                vutils.save_image(images.data, os.path.join(path_dir, 'input/', basename), padding=0, normalize=True)
            if opts.recon:
                if not os.path.exists(os.path.join(path_dir, 'recon/')):
                    os.makedirs(os.path.join(path_dir, 'recon/'))
                vutils.save_image(reconstructed.data, os.path.join(opts.output_folder, 'recon/', basename), padding=0, normalize=True)
            print(f'{bar} --> {opts.output_folder}', ' '*20)
                
        print('Testing Complete')
    else:
        pass
    t_fin = time() - t_start
    print(f'Time: {int(t_fin//60)}m {int(t_fin%60)}s | {int(t_fin)}s')
