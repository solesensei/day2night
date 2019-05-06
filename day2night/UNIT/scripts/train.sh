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
echo "------------------------------------------------------"
echo " Starting training... "
echo "------------------------------------------------------"
echo " Trainer: UNIT"
echo " Use default config: $config"
echo " GPU: $gpu"
echo "------------------------------------------------------"
read -p "It's okay ? [y/n] " ok
if [ "$ok" == "n" ]; then
    echo "Aborted."
    exit 0
fi
echo "Launch testing script..."
sleep 2
python train.py --device $gpu --config $config --trainer UNIT
echo " Completed! "