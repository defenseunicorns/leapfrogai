FROM nvidia/cuda:12.1.1-runtime-ubuntu22.04

# Update, install
RUN apt update && \
    apt install -y build-essential python3 python3-pip git

# Create user instead of using root
ENV USER='user'
RUN groupadd -r user && useradd -r -g $USER $USER


RUN mkdir -p /home/$USER/app

RUN chown -R $USER /home/$USER
RUN chmod a+rwx -R  /home/$USER
USER $USER


RUN pip install --upgrade pip setuptools wheel


# Define workdir
WORKDIR /home/$USER/app


ENV PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:1024
COPY requirements.txt leapfrogai/requirements.txt
RUN pip3 install -r leapfrogai/requirements.txt
COPY . leapfrogai/