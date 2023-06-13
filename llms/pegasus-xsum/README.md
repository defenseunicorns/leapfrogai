# Google/Pegasus-XSum Summarization Model

## Description

This project use the [Google Pegasus-XSum](https://huggingface.co/google/pegasus-xsum) (Text Summarization) model and turns it into an gRPC service through [SimpleAI](https://github.com/lhenault/simpleAI).

## Pre-requisites

* Poetry
* System install of ffmpeg

## Setup

### Local with Poetry

``` shell
# Set the location of the Poetry Virtual Environment to the project folder
poetry config virtualenvs.in-project true

# Install dependencies into a Poetry Virtual Environment
poetry install # CPU execution

<or>

poetry install --with cuda # GPU execution

```

``` shell
# Run locally in a Poetry Virtual Environment
poetry shell # opens the Poetry Virtual Environment

python model_test.py # Runs the model with
```

### Build an image (uses Cuda)

``` shell
# Build an image with Docker or Podman
docker build . -t pegasus-xsum:0.1

<or>

podman build . -t pegasus-xsum:0.1
```

``` shell
# Start Service (Requires Cuda)
docker run -it --rm -p 50051:50051 --gpus all pegasus-xsum:0.1

<or>

podman run -it --rm -p 50051:50051 --gpus all pegasus-xsum:0.1
```
