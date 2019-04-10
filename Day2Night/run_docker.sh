#!/bin/bash

NAME=sole
TAG=pytorch_0.4.1
PORT=1434

if [ $# -eq 1 ]; then
	if [ "$1" == "-h" ] || [ "$1" == "--help" ]; then
		echo "Usage: rundocker [-h] [NAME] [PORT] [TAG]"
		exit 0
	fi
	NAME=$1
elif [ $# -eq 2 ]; then
	NAME=$1
	PORT=$2
elif [ $# -eq 3 ]; then
	NAME=$1
	PORT=$2
	TAG=$3
fi


echo "-------------------------------------------------------"
echo "Creating docker container: $NAME"
echo "Port binding: $PORT <- $PORT"
echo "Docker image: solesensei/day2night:$TAG"
echo "-------------------------------------------------------"
docker run -it -p $PORT:$PORT --name $NAME --mount type=bind,source=/hpcfs/GRAPHICS2/21d_gon/,target=/mnt/w/prj -w /mnt/w/prj --runtime nvidia -i -t solesensei/day2night:$TAG
