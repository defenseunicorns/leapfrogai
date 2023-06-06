# Whsiper API server

## Pre-requisites

* [Rye](https://github.com/mitsuhiko/rye)
* System install of ffmpeg
* For GPU usage, latest CUDA drivers

## Getting Started

```shell
rye sync
rye run uvicorn main:app --reload

# to enter a Python shell:
rye shell
```

## Usage

Open `http://localhost:8000/docs` for a Swagger interface.

## TODO

* Tests
* Error handling for ffmpeg