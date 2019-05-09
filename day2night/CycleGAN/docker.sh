docker pull solesensei/day2night:cyclegan
docker run -it -p 8097:8097 --name cycgan --mount type=bind,source=/mnt/w/prj/,target=/mnt/w/prj/ \
                    --mount type=bind,source=/mnt/w/prj/GraduateWork/day2night/CycleGAN/checkpoints,target=/mnt/w/prj/checkpoints \
                    --runtime nvidia -i -t cyclegan:latest
