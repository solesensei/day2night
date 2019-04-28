docker pull taesungp/pytorch-cyclegan-and-pix2pix
# nvidia-docker run -it -p 8097:8097 --mount type=bind,source=/mnt/w/prj/data,target=/mnt/w/prj/data cyclegan
docker run -it -p 8097:8097 --name cycgan --mount type=bind,source=/mnt/w/prj/data,target=/mnt/w/prj/data --runtime nvidia -i -t cyclegan:latest
