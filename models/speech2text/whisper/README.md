# Whsiper API server

## Pre-requisites

* [Rye](https://github.com/mitsuhiko/rye)
* docker
    * For GPU support please consult: https://docs.docker.com/config/containers/resource_constraints/#gpu
* System install of ffmpeg
* For GPU usage, latest CUDA drivers

## Getting Started

#### Python

* `rye sync`
* `rye run python main.py`

## Build

#### Docker

* `docker build --user=root -t leapfrogai/whisper:latest .`

## Run
#### Docker
* GPU
    * `docker run --rm --gpus all --ipc=host --ulimit memlock=-1 --ulimit stack=67108864 -p 8000:8000 -p 50052:50051 -d --name whisper leapfrogai/whisper:latest`
        * `--gpus device=<device-num>` to target a specific GPU device ex: `--gpus device=0`
* CPU
    * `docker run --rm --ipc=host --ulimit memlock=-1 --ulimit stack=67108864 -p 8000:8000 -p 50052:50051 -d --name whisper leapfrogai/whisper:latest`

## TODO

* Tests
* Error handling for ffmpeg