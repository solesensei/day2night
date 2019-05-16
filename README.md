# Day2Night | Image2Image Translation Research 

**[Diploma](./diploma/source/Day2Night.pdf) | Graduation Work | Bachelor's Degree**

__Lomonosov Moscow State University,__ Faculty of Computer Science, Graphics Lab

## Test with Docker
_This repo is huge_

### Automated
So you can download **bash** [script](day2night/UNIT/scripts/day2night.sh)
```bash
wget https://raw.githubusercontent.com/solesensei/day2night/master/day2night/UNIT/scripts/day2night.sh -O ~/prj/day2night.sh
```
Then just run (_in repository you want to start_)
```bash
cd ~/prj
bash day2night.sh
```

### Manually

#### Get project
Clone repository
```bash
git clone --depth 1 https://github.com/solesensei/day2night.git
```
or just get the code ([if not working](#PT-models))
```
wget --no-check-certificate -r "https://docs.google.com/uc?export=download&id=1mrj0vDzuFufpmxSW5SMIAn9XekegX4Hh" -O code.zip
unzip -o code.zip
```

#### Get image
Pull Docker image
```bash
docker pull solesensei/day2night:pytorch_0.4.1 # CUDA 9 : Ubuntu LTS 18.04
# or
docker pull solesensei/day2night:pytorch_0.4.1_cuda9 # CUDA 9 : Ubuntu LTS 16.04
```
**All tags:**
- `pytorch_0.4.1_cuda9` : CUDA 9, Ubuntu LTS 16.04, Pytorh==0.4.1
- `cyclegan` - CUDA 9, Base,  Pytorh>=1.0.1
- `pytorch_0.4.1` - CUDA 10, Ubuntu LTS 18.04, Pytorh==0.4.1
- `pytorch_latest` - CUDA 10, Ubuntu LTS 18.04, Pytorch>=1.0.1

#### Run container
```bash
cd ~/prj
docker run -it -p 1111:1111 --name day2night --mount type=bind,source=$PWD,target=/mnt/w/prj -w /mnt/w/prj/UNIT --runtime nvidia -i -t solesensei/day2night:pytorch_0.4.1 # your tag here
```

Modify parametrs in [test.sh](./day2night/UNIT/scripts/test.sh)

And run test
```bash
cd ~/prj/UNIT
bash ./scripts/test.sh
```
or train
```bash
bash ./scripts/test.sh
```

### PT-models

- **[Google.Drive](https://drive.google.com/open?id=1Qe_AEZ1qeN8i5Q2cgXqGDmjKdXDRpBhT)**
- **[Minimal Source Code](https://drive.google.com/open?id=1mrj0vDzuFufpmxSW5SMIAn9XekegX4Hh)**

## UNIT vs. CycleGAN

|                              RetinaNet                              |         Day        |         Night        |         All         |
|:-------------------------------------------------------------------:|:-------------------:|:-------------------:|:-------------------:|
| Real Data Images ([NEXET](https://www.getnexar.com/challenge-2/))   |        0.8664       |        0.8406       |        0.8535       |
| [CycleGAN](https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix) |   0.8701 (+0.42%)   | **0.8571 (+1.96%)** | **0.8636 (+1.18%)** |
| [UNIT](https://github.com/mingyuliutw/UNIT)                         | **0.8749 (+0.98%)** |   0.8512 (+1.26%)   |   0.8631 (+1.12%)   |

|                             Faster R-CNN                              |         Day        |         Night        |         All         |
|:---------------------------------------------------------------------:|:-------------------:|:-------------------:|:-------------------:|
| Real Data Images ([NEXET](https://www.getnexar.com/challenge-2/))     |        0.9015       |        0.8822       |        0.8919       |
| [CycleGAN](https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix)   | **0.9087 (+0.79%)** |   0.8881 (+0.66%)   |   0.8984 (+0.72%)   |
| [UNIT](https://github.com/mingyuliutw/UNIT)                           |   0.9066 (+0.56%)   | **0.8929 (+1.21%)** | **0.8998 (+0.88%)** |

![](diploma/source/img/aug_full_en.png)

## VGG16 and Normalization

![](diploma/source/img/vgg_norm_cmp_en.png)

## Results
### UNIT
![](diploma/source/img/results.svg)
