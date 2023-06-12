# Google/Pegasus-XSum Summarization Model

## Description

This project use the [Google Pegasus-XSum](https://huggingface.co/google/pegasus-xsum) (Text Summarization) model and turns it into an gRPC service through [SimpleAI](https://github.com/lhenault/simpleAI).

## Pre-requisites

* Poetry
* System install of ffmpeg
* GPU Currently Required!

## Setup

### Poetry

``` shell
poetry install
```

Overloads include:

``` shell
--with jupyter
--with cuda
```

### Build an image

``` shell
docker build . -t pegasus-xsum:0.1

or

podman build . -t pegasus-xsum:0.1
```

* Start Service

``` shell
docker run -it --rm -p 50051:50051 --gpus all pegasus-xsum:0.1

or 

podman run -it --rm -p 50051:50051 --gpus all pegasus-xsum:0.1
```
