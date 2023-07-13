# Getting Started

## Description

This is a quick guide to get LeapFrogAI running locally.

## Requirements

* Go >= 1.20
* Python >= 3.10
* Cuda >= 11.8
* NVidia GPU w/ 16GB VRAM (24GB recommended)

## Instructions

### API Server

LeapFrogAI's API server is written in go. To launch the API Server:

``` shell
go run ./api/main.go
```

### mpt-7b-chat

1. Navigate to `./models/llms/mpt-7b-chat`.
2. Create a venv and activate it:

``` shell
python3 -m venv venv

source ./venv/bin/activate
```

3. Pull the model (this will take some time):

``` shell
python get_model.py
```

4. Launch the model server:

``` shell
python model.py
```

The URL for this server will default to http://localhost:8080/openai.

^ If you need a client, check this out: https://github.com/defenseunicorns/chatbot-ui
