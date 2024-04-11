![LeapfrogAI Logo](https://github.com/defenseunicorns/leapfrogai/raw/main/docs/imgs/leapfrogai.png)

[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/defenseunicorns/leapfrogai/badge)](https://api.securityscorecards.dev/projects/github.com/defenseunicorns/leapfrogai)

## Table of Contents
- [Table of Contents](#table-of-contents)
- [Overview](#overview)
- [Why Host Your Own LLM?](#why-host-your-own-llm)
- [Structure](#structure)
- [Getting Started](#getting-started)
- [Components](#components)
  - [API](#api)
  - [Backends](#backends)
  - [Image Hardening](#image-hardening)
  - [SDK](#sdk)
  - [User Interface](#user-interface)
- [Usage](#usage)
  - [UDS (Latest)](#uds-latest)
  - [UDS (Dev)](#uds-dev)
  - [Local Dev](#local-dev)
- [Community](#community)

## Overview

LeapfrogAI is a self-hosted AI platform designed to be deployed in air-gapped environments. This project aims to bring sophisticated AI solutions to air-gapped resource-constrained environments, by enabling the hosting all requisite components of an AI stack.

Our services include vector databases, model backends, API, and UI. These capabilities can be easily accessed and integrated with your existing infrastructure, ensuring the power of AI can be harnessed irrespective of your environment's limitations.

## Why Host Your Own LLM?

Large Language Models (LLMs) are a powerful resource for AI-driven decision making, content generation, and more. How can LeapfrogAI bring AI to your mission?

- **Data Independence**: Sending sensitive information to a third-party service may not be suitable or permissible for all types of data or organizations. By hosting your own LLM, you retain full control over your data.

- **Scalability**: Pay-as-you-go AI services can become expensive, especially when large volumes of data are involved and require constant connectivity. Running your own LLM can often be a more cost-effective solution for missions of all sizes.

- **Mission Integration**: By hosting your own LLM, you have the ability to customize the model's parameters, training data, and more, tailoring the AI to your specific needs.

## Structure

The LeapfrogAI repository follows a monorepo structure based around an [API](#api) with each of the [components](#components) included in a dedicated `packages` directory. Each of these package directories contains the source code for each component as well as the deployment infrastructure. The UDS bundles that handle the development and latest deployments of LeapfrogAI are in the `uds-bundles` directory. The structure looks as follows:

```
leapfrogai/
├── src/
│   └── leapfrogai_api/
│       ├── main.py
│       └── ...
├── packages/
│   ├── api/
│   ├── llama-cpp-python/
│   ├── text-embeddings/
│   ├── vllm/
│   └── whisper/
├── uds-bundles/
│   ├── dev/
│   └── latest/
├── Makefile
├── pyproject.toml
├── README.md
└── ...
```

## Getting Started

The preferred method for running LeapfrogAI is a local [Kubernetes](https://kubernetes.io/) deployment using [UDS](https://github.com/defenseunicorns/uds-core). Refer to the [Quick Start](https://docs.leapfrog.ai/docs/local-deploy-guide/quick_start/) section of the LeapfrogAI documentation site for instructions on this type of deployment.

## Components

### API

LeapfrogAI provides an API that closely matches that of OpenAI's. This feature allows tools that have been built with OpenAI/ChatGPT to function seamlessly with a LeapfrogAI backend.

### Backends

> Available Backends:
> | Backend | AMD64 Support | ARM64 Support | Cuda Support | Docker Ready | K8s Ready | Zarf Ready |
> | --- | --- | --- | --- | --- | --- | --- |
> | [llama-cpp-python](packages/llama-cpp-python/) | ✅ | 🚧 | ✅ | ✅ | ✅ | ✅ |
> | [whisper](packages/whisper/) | ✅ | 🚧 | ✅ | ✅ | ✅ | ✅ |
> | [text-embeddings](packages/text-embeddings/) | ✅ | 🚧 | ✅ | ✅ | ✅ | ✅ |
> | [vllm](packages/vllm/) | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ |
> | [rag](https://github.com/defenseunicorns/leapfrogai-backend-rag) (repo integration soon) | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |

LeapfrogAI provides several backends for a variety of use cases.

### Image Hardening

> GitHub Repo:
>
> - [leapfrogai-images](https://github.com/defenseunicorns/leapfrogai-images)

LeapfrogAI leverages Chainguard's [apko](https://github.com/chainguard-dev/apko) to harden base python images - pinning Python versions to the latest supported version by the other components of the LeapfrogAI stack.

### SDK

The LeapfrogAI SDK provides a standard set of protobuff and python utilities for implementing backends and gRPC.

### User Interface

> GitHub Repo:
>
> - [leapfrog-ui](https://github.com/defenseunicorns/leapfrog-ui)

LeapfrogAI provides some options of UI to get started with common use-cases such as chat, summarization, and transcription.

## Usage

### UDS (Latest)

LeapfrogAI can be deployed and run locally via UDS and Kubernetes, built out using [Zarf](https://zarf.dev) packages. This pulls the most recent package images and is the most stable way of running a local LeapfrogAI deployment. These instructions can be found on the [LeapfrogAI Docs](https://docs.leapfrog.ai/docs/) site.

### UDS (Dev)

If you want to make some changes to LeapfrogAI before deploying via UDS (for example in a dev environment), you can follow these instructions:

Make sure your system has the [required dependencies](https://docs.leapfrog.ai/docs/local-deploy-guide/quick_start/#prerequisites).

For ease, it's best to create a virtual environment:
```
python -m venv .venv
source .venv/bin/activate
```

Each component is built into its own Zarf package. This can be done easily using the provided `Make` targets:
```
make build-api
make build-vllm                 # if you have GPUs
make build-llama-cpp-python     # if you have CPU only
make build-text-embeddings
make build-whisper
```
**OR**

You can build all of the packages you need at once with the following make targets:

```
make build-cpu    # api, llama-cpp-python, text-embeddings, whisper
make build-gpu    # api, vllm, text-embeddings, whisper
make build-all    # all of the backends
```

Once the packages are created, you can deploy either a CPU or GPU-enabled deployment via one of the UDS bundles:

#### CPU
```
cd uds-bundles/dev/cpu
uds create .
uds deploy k3d-core-slim-dev:0.18.0
uds deploy uds-bundle-leapfrogai*.tar.zst
```

#### GPU
```
cd uds-bundles/dev/gpu
uds create .
uds deploy k3d-core-slim-dev:0.18.0 --set K3D_EXTRA_ARGS="--gpus=all --image=ghcr.io/justinthelaw/k3d-gpu-support:v1.27.4-k3s1-cuda"     # be sure to check if a newer version exists
uds deploy uds-bundle-leapfrogai-*.tar.zst --confirm
```

### Local Dev

The following instructions are for running each of the LFAI components for local development. This is useful when testing changes to a specific component, but will not assist in a full deployment of LeapfrogAI. Please refer to the above sections for deployment instructions.

It is highly recommended to make a virtual environment to keep the development environment clean:

```
python -m venv .venv
source .venv/bin/activate
```

#### API

To run the LeapfrogAI API locally (starting from the root directory of the repository):

```
python -m pip install ".[dev]"
cd src
uvicorn leapfrogai_api.main:app --port 3000 --reload
```

#### Backend: llama-cpp-python

To run the llama-cpp-python backend locally (starting from the root directory of the repository):

```
python -m pip install ".[llama-cpp-python,dev]"
cd packages/llama-cpp-python
python scripts/model_download.py
mv .model/*.gguf .model/model.gguf
python -m leapfrogai_api.types.cli --app-dir=. main:Model
```

#### Backend: text-embeddings
To run the text-embeddings backend locally (starting from the root directory of the repository):

```
python -m pip install ".[text-embeddings,dev]"
cd packages/text-embeddings
python scripts/model_download.py
python -u main.py
```

#### Backend: vllm
To run the vllm backend locally (starting from the root directory of the repository):

```
python -m pip install ".[vllm,dev]"
cd packages/vllm
python scripts/model_download.py
export QUANTIZATION=awq
python -m leapfrogai_api.types.cli --app-dir=. main:Model
```

#### Backend: whisper
To run the vllm backend locally (starting from the root directory of the repository):

```
python -m pip install ".[whisper,dev]"
cd packages/whisper
ct2-transformers-converter --model openai/whisper-base --output_dir .model --copy_files tokenizer.json --quantization float32
python -u main.py
```

## Community

LeapfrogAI is supported by a community of users and contributors, including:

- [Defense Unicorns](https://defenseunicorns.com)
- [Beast Code](https://beast-code.com)
- [Chainguard](https://www.chainguard.dev/)
- [Exovera](https://exovera.com/)
- [Hypergiant](https://www.hypergiant.com/)
- [Pulze](https://www.pulze.ai)
- [SOSi](https://www.sosi.com/)
- [United States Navy](https://www.navy.mil/)
- [United States Air Force](https://www.airforce.com)
- [United States Space Force](https://www.spaceforce.mil)

[![Defense Unicorns logo](/docs/imgs/user-logos/defense-unicorns.png)](https://defenseunicorns.com)[![Beast Code logo](/docs/imgs/user-logos/beast-code.png)](https://beast-code.com)[![Hypergiant logo](/docs/imgs/user-logos/hypergiant.png)](https://hypergiant.com)[![Pulze logo](/docs/imgs/user-logos/pulze.png)](https://pulze.ai)

*Want to add your organization or logo to this list? [Open a PR!](https://github.com/defenseunicorns/leapfrogai/edit/main/README.md)*
