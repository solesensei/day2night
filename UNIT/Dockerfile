FROM nvidia/cuda:10.1-cudnn7-runtime-ubuntu18.04
# Set anaconda path
ENV ANACONDA /opt/anaconda
ENV PATH $ANACONDA/bin:$PATH
RUN apt-get update && apt-get install -y --no-install-recommends \
         wget \
         libopencv-dev \
         python-opencv \
         build-essential \
         cmake \
         git \
         curl \
         ca-certificates \
         libjpeg-dev \
         libpng-dev \
         axel \
         zip \
         unzip
RUN wget https://repo.anaconda.com/archive/Anaconda3-5.2.0-Linux-x86_64.sh -P /tmp
RUN bash /tmp/Anaconda3-5.0.1-Linux-x86_64.sh -b -p $ANACONDA
RUN rm /tmp/Anaconda3-5.0.1-Linux-x86_64.sh -rf
RUN conda install -y pytorch torchvision cudatoolkit=10.0 -c pytorch
RUN conda install -y pip yaml -c anaconda
RUN pip install tensorboard tensorboardX;
