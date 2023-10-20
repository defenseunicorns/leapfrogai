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

#### Go
LeapFrogAI's API server is written in go. To launch the API Server:

``` shell
cd ./api
go run main.go
```

#### Docker
* **Build**
  * [Optional] - If the models are being deploying on other machines, edit the `url` value in each model within `/api/models.toml` to the public ip address of the target machine. Otherwise, no modifications are necessary.
  * `docker build -t leapfrogai/go-api:latest .`
* **Run**
  * `docker run --rm --ulimit memlock=-1 --ulimit stack=67108864 --network host -d --name leapfrogai-go-api leapfrogai/go-api:latest`

### mpt-7b-chat

#### Python
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

#### Docker
1. Navigate to `./models/llms/mpt-7b-chat` and follow the README.md instructions found there.
