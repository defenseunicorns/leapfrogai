# Whsiper API server

## Pre-requisites

* [Rye](https://github.com/mitsuhiko/rye)
* System install of ffmpeg
* For GPU usage, latest CUDA drivers

## Getting Started

```shell
rye sync
rye run python main.py
```

## Docker Build

```shell
docker build -t leapfrogai-whisper .
docker run --gpus all --ipc=host --ulimit memlock=-1 --ulimit stack=67108864 -p 0.0.0.0:8000:8000 -p 0.0.0.0:50051:50051 -d <image-id>
```

## TODO

* Tests
* Error handling for ffmpeg