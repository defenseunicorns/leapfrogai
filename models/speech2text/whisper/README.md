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
```

## Usage

Open `http://localhost:8000/docs` for a Swagger interface.

## TODO

* Tests
* Error handling for ffmpeg