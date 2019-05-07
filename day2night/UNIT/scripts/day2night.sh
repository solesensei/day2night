#!/bin/bash

set -e

echo "-------------------------------------------------------"
echo "Downloading project..."
echo "-------------------------------------------------------"
sleep 1
wget --no-check-certificate -r "https://docs.google.com/uc?export=download&id=1mrj0vDzuFufpmxSW5SMIAn9XekegX4Hh" -O code.zip
unzip -o code.zip
rm code.zip

NAME=unit
TAG=pytorch_0.4.1_cuda9
RM=""
PORT=8080
sleep 1
echo "-------------------------------------------------------"
echo "Pulling docker image: solesensei/day2night:$TAG"
echo "-------------------------------------------------------"
sleep 1
docker pull solesensei/day2night:$TAG

echo "-------------------------------------------------------"
echo "Creating docker container: $NAME"
echo "Port binding: $PORT <- $PORT"
echo "Docker image: solesensei/day2night:$TAG"
if [ "$RM" == "--rm" ]; then
	echo "Docker temporary: True"
else
	echo "Docker temporary: False"
fi
echo "-------------------------------------------------------"
echo "To Train use: bash ./scripts/train.sh"
echo "To Test use: bash ./scripts/test.sh (change parametrs in script)"
sleep 3
docker run -it -p $PORT:$PORT $RM --name $NAME --mount type=bind,source=$PWD,target=/mnt/w/prj -w /mnt/w/prj/UNIT --runtime nvidia -i -t solesensei/day2night:$TAG
echo "Script complete"
