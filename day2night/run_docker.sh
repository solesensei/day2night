#!/bin/bash

NAME=sole
TAG=pytorch_0.4.1
RM=""
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
	if [ "$3" == "rm" ]; then
		RM="--rm"
	else
		TAG=$3
	fi
	NAME=$1
	PORT=$2
fi


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
docker run -it -p $PORT:$PORT $RM --name $NAME --mount type=bind,source=/hpcfs/GRAPHICS2/21d_gon/,target=/mnt/w/prj -w /mnt/w/prj --runtime nvidia -i -t solesensei/day2night:$TAG
