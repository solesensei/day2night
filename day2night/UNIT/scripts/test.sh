#!/bin/bash
# ----------------------- parameters -----------------------
checkdir="checkpoints/512_vgg"
checkpoint=f"{checkdir}/gen_00473000.pt"
config="configs/unit_day2night_512_vgg.yaml"
indir="/mnt/w/prj/data/nexet/nexet_2017_1/testA"
outdir=f"{checkdir}/out473"
number=200
# ----------------------------------------------------------
if [ "$#" -gt 0 ]; then
    checkdir="$1"
    checkpoint="$2"
    config="$3"
    # indir="${checkdir}/out"
    indir="$4"
    outdir="$5"
    number="$6"
    gpu="$7"
    a2b="$8"
    flag=0
else
    flag=1
fi

# cd /mnt/w/prj/UNIT
mkdir -p $outdir

echo "------------------------------------------------------"
echo "UNIT | day2night | starting..."
echo "------------------------------------------------------"
set -e
sleep 1
echo "------------------------------------------------------"
echo " Show all GPUs"
echo "------------------------------------------------------"
nvidia-smi --format=csv --query-gpu=index,name,driver_version,memory.total,memory.used,memory.free
echo "------------------------------------------------------"
if [ $flag -eq 1 ]; then
    read -p "Choose number of free GPU for training: [0,1,2...] " gpu
    read -p "Domains: Day -> Night [y/n] " a2b
fi
if [ "$a2b" == "y" ] || [ $a2b -eq 1 ]; then
    A="Day"
    B="Night"
    d2n=1
elif [ "$a2b" == "n" ] || [ $a2b -eq 0 ]; then
    B="Day"
    A="Night"
    d2n=0
fi

echo "------------------------------------------------------"
echo " Starting tests... "
echo "------------------------------------------------------"
echo " Trainer: UNIT"
echo " Use config: $config"
echo " Input folder: $indir"
echo " Output folder: $outdir"
echo " Checkpoint: $checkpoint"
echo " Domains: $A -> $B"
echo " GPU: $gpu"
echo " Number: $number"
echo "------------------------------------------------------"
if [ $flag -eq 1 ]; then
    read -p "It's okay ? [y/n] " ok
fi
if [ "$ok" == "n" ]; then
    echo "Aborted."
    exit 0
fi
echo "Launch testing script..."
sleep 1

python test_batch.py --device $gpu --config $config --input_folder $indir --output_folder $outdir --number $number --checkpoint $checkpoint --a2b $d2n --trainer UNIT --recon
echo " Completed! "
