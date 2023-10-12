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
docker build --build-arg IMAGE_TAG=${IMAGE_TAG} -t leapfrogai-whisper .
docker run --gpus all --ipc=host --ulimit memlock=-1 --ulimit stack=67108864 -p 0.0.0.0:50051:50051 -d <image-id>

```

## Usage

Open `http://localhost:8000/docs` for a Swagger interface.

## TODO

* Tests
* Error handling for ffmpeg