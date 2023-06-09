# Google/Pegasus-XSum Summarization Model

## Description

This project use the [Google Pegasus-XSum](https://huggingface.co/google/pegasus-xsum) (Text Summarization) model and turns it into an gRPC service through [SimpleAI](https://github.com/lhenault/simpleAI).

## Pre-requisites

* [Rye](https://github.com/mitsuhiko/rye)
* System install of ffmpeg
* GPU Currently Required!

## Setup

* Ensure [Rye](https://github.com/mitsuhiko/rye) is setup.
* Generate your environment and requirements files:

```shell
rye sync
```

* Build a docker image:

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

* Run Simple AI Service:

``` shell
simple_ai serve [--host 127.0.0.1] [--port 8080]
```
