FROM nvidia/cuda:9.1-cudnn7-runtime-ubuntu16.04
#FROM nvidia/cuda:10.1-cudnn7-runtime-ubuntu18.04
# Set anaconda path
ENV ANACONDA /opt/anaconda
ENV PATH $ANACONDA/bin:$PATH
ENV TZ=Europe/Moscow
ENV DEBIAN_FRONTEND=noninteractive 
ENV ANACONDA_VER Anaconda3-5.2.0-Linux-x86_64.sh
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update && apt-get install -y --no-install-recommends \
         apt-utils \
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
         unzip \
         vim
RUN wget https://repo.anaconda.com/archive/${ANACONDA_VER} -P /tmp
RUN bash /tmp/${ANACONDA_VER} -b -p $ANACONDA
RUN rm /tmp/${ANACONDA_VER} -rf
RUN conda install -y pytorch=0.4.1 torchvision cuda91 -c pytorch
# RUN conda install -y pytorch torchvision cudatoolkit=10.0 -c pytorch
RUN conda install -y pip yaml -c anaconda
RUN pip install tensorboard tensorboardX tensorflow;
