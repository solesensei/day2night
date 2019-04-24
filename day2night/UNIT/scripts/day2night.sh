#!/bin/bash

set -e

echo "-------------------------------------------------------"
echo "Downloading project..."
echo "-------------------------------------------------------"
wget --no-check-certificate -r "https://docs.google.com/uc?export=download&id=1mrj0vDzuFufpmxSW5SMIAn9XekegX4Hh" -O code.zip
unzip code.zip
rm code.zip

NAME=unit
TAG=pytorch_0.4.1
RM=""
PORT=8080
echo "-------------------------------------------------------"
echo "Pulling docker image: solesensei/day2night:$TAG"
echo "-------------------------------------------------------"
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
docker run -it -p $PORT:$PORT $RM --name $NAME --mount type=bind,source=./,target=/mnt/w/prj -w /mnt/w/prj --runtime nvidia -i -t solesensei/day2night:$TAG
