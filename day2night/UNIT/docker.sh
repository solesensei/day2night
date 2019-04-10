#!/bin/bash
# docker build -t "unit:test" .

docker run --mount type=bind,source=/mnt/w/prj/data,target=/mnt/w/prj/data --mount type=bind,source=/mnt/w/prj/GraduateWork/UNIT/,target=/mnt/w/prj/GraduateWork/UNIT/ --runtime nvidia -i -t unit:test