#!/bin/bash
# ----------------------- parameters -----------------------
checkdir="checkpoints/vgg"
checkpoint="${checkdir}/gen_01000000.pt"
config="configs/unit_day2night_vgg.yaml"
indir="/mnt/w/prj/GraduateWork/scripts/Any2Gif/img/day_orig"
outdir="${checkdir}/out"
# ----------------------------------------------------------
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
read -p "Choose number of free GPU for training: [0,1,2...] " gpu
read -p "Domains: Day -> Night [y/n] " c
if [ "$c" == "y" ]; then
    A="Day"
    B="Night"
    d2n=1
else
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
echo "------------------------------------------------------"
read -p "It's okay ? [y/n] " ok
if [ "$ok" == "n" ]; then
    echo "Aborted."
    exit 0
fi
echo "Launch testing script..."
sleep 2

python test_batch.py --device $gpu --config $config --input_folder $indir --output_folder $outdir --checkpoint $checkpoint --a2b $d2n --trainer UNIT --recon
echo " Completed! "
