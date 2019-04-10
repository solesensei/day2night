#!/bin/bash
echo "Start training..."
echo "datasets:"
ls ../datasets/nexet/
echo "Launching..."
python train.py --config configs/unit_day2night.yaml --trainer UNIT
echo "Ended" > log.txt
echo "Ended"
