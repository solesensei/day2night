import torch
import os
from torch.utils.serialization import load_lua
from torchvision.models import resnet18
from networks import Vgg16, ResNet
import torch.utils.model_zoo as model_zoo

model_dir = 'models/'

with open('lua.txt', 'w') as luaf:
    vgglua = load_lua(os.path.join(model_dir, 'vgg16.t7'))
    vgg = Vgg16()
    for (src, dst) in zip(vgglua.parameters()[0], vgg.parameters()):
        print(src, file=luaf)
        input()
        dst.data[:] = src

resnet = ResNet()
resnet.load_state_dict(model_zoo.load_url('https://download.pytorch.org/models/resnet18-5c106cde.pth',model_dir))
