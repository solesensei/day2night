echo "------------------------------------------------------"
echo "UNIT | day2night | starting..."
echo "------------------------------------------------------"
set -e
sleep 1
cd /mnt/w/prj/UNIT
echo "------------------------------------------------------"
echo " Show all GPUs"
echo "------------------------------------------------------"
nvidia-smi --format=csv --query-gpu=index,name,driver_version,memory.total,memory.used,memory.free
echo "------------------------------------------------------"
read -p "Choose number of free GPU for training: [0,1,2...] " gpu
read -p "Use VGG pre-trained model? [y/n] " vgg
if [ "$vgg" == "y" ]; then
    vgg="YES"
    config="configs/unit_day2night_512_vgg.yaml"
else
    vgg="NO"
    config="configs/unit_day2night_512.yaml"
fi
read -p "Config: $config correct? [y/n] (You can choose manualy if not) " c
if [ "$c" == "n" ]; then
    read -p "Set path to config: " config
fi

read -p "Input folder: $PWD/inputs [y/n] " indir
if [ "$indir" == "y" ]; then
    indir="$PWD/inputs"
else
    read -p "Set path to input folder: " indir
fi

checkpoint="$PWD/checkpoints/gen_00420000.pt"
read -p "Checkpoint: $checkpoint [y/n] " c
if [ "$c" == "n" ]; then
    read -p "Set path to checkpoint: " checkpoint
fi

read -p "Output folder: $PWD/outputs [y/n] " outdir
if [ "$outdir" == "y" ]; then
    outdir="$PWD/outputs"
else
    read -p "Set path to output folder: " outdir
fi
read -p "Domains: Day -> Night [y/n] " c
if [ "$outdir" == "y" ]; then
    A="Day"
    B="Night"
    d2n=1
else
    B="Day"
    A="Night"
    d2n=2
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
python test_batch.py --device $gpu --config $config --input_folder $indir --output_folder $outdir --checkpoint $checkpoint --a2b $d2n --trainer UNIT
echo " Completed! "