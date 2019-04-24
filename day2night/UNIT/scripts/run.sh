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
read -p "Choose number of free GPU for training: [0,1,2...]" gpu
echo "------------------------------------------------------"
echo " Starting training... "
echo "------------------------------------------------------"
echo " Use default config: configs/unit_day2night_512.yaml"
echo " Trainier: UNIT"
echo "------------------------------------------------------"
sleep 2
python train.py --device $gpu --config configs/unit_day2night_512.yaml --trainer UNIT
echo " Completed! "