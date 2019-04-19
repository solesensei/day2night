"""
Copyright (C) 2018 NVIDIA Corporation.  All rights reserved.
Licensed under the CC BY-NC-SA 4.0 license (https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode).
"""
# System import
import os
import sys
import argparse
import shutil

def usage():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, default='configs/unit_day2night.yaml', help='Path to the config file.')
    parser.add_argument('--output_path', type=str, default='.', help="outputs path")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument('--trainer', type=str, default='UNIT', help="MUNIT|UNIT")
    parser.add_argument('--device', metavar='GPU', nargs='+', help='GPU List', default=["0"])
    return parser.parse_args()

opts = usage()

# Choose GPU device to run
os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID" 
os.environ["CUDA_VISIBLE_DEVICES"]=",".join(str(x) for x in opts.device)

import torch
import torch.backends.cudnn as cudnn
from torch.autograd import Variable
from utils import get_all_data_loaders, prepare_sub_folder, write_html, write_loss, get_config, write_2images, Timer
from trainer import MUNIT_Trainer, UNIT_Trainer
try:
    from itertools import izip as zip
except ImportError: # will be 3.x series
    pass
import tensorboardX
from subprocess import call

# Print System Info 
print('CUDA Devices')
call(["nvidia-smi", "--format=csv", "--query-gpu=index,name,driver_version,memory.total,memory.used,memory.free"])
print(f'Available devices {torch.cuda.device_count()}: {", ".join(str(x) for x in opts.device)}')
print('Active CUDA Device: GPU', torch.cuda.current_device())

cudnn.benchmark = True

# Load experiment setting
config = get_config(opts.config)
max_iter = config['max_iter']
display_size = config['display_size']
config['vgg_model_path'] = opts.output_path
config['resnet_model_path'] = opts.output_path

# Setup model and data loader
if opts.trainer == 'MUNIT':
    trainer = MUNIT_Trainer(config)
elif opts.trainer == 'UNIT':
    trainer = UNIT_Trainer(config)
else:
    sys.exit("Only support MUNIT|UNIT")
trainer.cuda()
train_loader_a, train_loader_b, test_loader_a, test_loader_b = get_all_data_loaders(config)
train_display_images_a = torch.stack([train_loader_a.dataset[i] for i in range(display_size)]).cuda()
train_display_images_b = torch.stack([train_loader_b.dataset[i] for i in range(display_size)]).cuda()
test_display_images_a = torch.stack([test_loader_a.dataset[i] for i in range(display_size)]).cuda()
test_display_images_b = torch.stack([test_loader_b.dataset[i] for i in range(display_size)]).cuda()

# Setup logger and output folders
model_name = os.path.splitext(os.path.basename(opts.config))[0]
train_writer = tensorboardX.SummaryWriter(os.path.join(opts.output_path + "/logs", model_name))
output_directory = os.path.join(opts.output_path + "/outputs", model_name)
checkpoint_directory, image_directory = prepare_sub_folder(output_directory)
shutil.copy(opts.config, os.path.join(output_directory, 'config.yaml')) # copy config file to output folder

# Start training
iterations = trainer.resume(checkpoint_directory, hyperparameters=config) if opts.resume else 0
while True:
    for it, (images_a, images_b) in enumerate(zip(train_loader_a, train_loader_b)):
        trainer.update_learning_rate()
        images_a, images_b = images_a.cuda().detach(), images_b.cuda().detach()

        with Timer("Elapsed time in update: %f"):
            # Main training code
            trainer.dis_update(images_a, images_b, config)
            trainer.gen_update(images_a, images_b, config)
            torch.cuda.synchronize()

        # Dump training stats in log file
        if (iterations + 1) % config['log_iter'] == 0:
            print("Iteration: %08d/%08d" % (iterations + 1, max_iter), end=' ')
            print("Learning rate:", trainer.dis_scheduler.get_lr()[0])
            write_loss(iterations, trainer, train_writer)

        # Write images
        if (iterations + 1) % config['image_save_iter'] == 0:
            print(f'Saving images to {image_directory}')
            with torch.no_grad():
                test_image_outputs = trainer.sample(test_display_images_a, test_display_images_b)
                train_image_outputs = trainer.sample(train_display_images_a, train_display_images_b)
            write_2images(test_image_outputs, display_size, image_directory, 'test_%08d' % (iterations + 1))
            write_2images(train_image_outputs, display_size, image_directory, 'train_%08d' % (iterations + 1))
            # HTML
            write_html(output_directory + "/index.html", iterations + 1, config['image_save_iter'], 'images')

        if (iterations + 1) % config['image_display_iter'] == 0:
            with torch.no_grad():
                image_outputs = trainer.sample(train_display_images_a, train_display_images_b)
            write_2images(image_outputs, display_size, image_directory, 'train_current')

        # Save network weights
        if (iterations + 1) % config['snapshot_save_iter'] == 0:
            print(f'Saving pre-trained checkpoint to {checkpoint_directory}')
            trainer.save(checkpoint_directory, iterations, config['snapshot_smart_override'])

        iterations += 1
        if iterations >= max_iter:
            sys.exit('Finish training')
