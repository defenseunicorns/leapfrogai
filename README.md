![LeapfrogAI](https://github.com/defenseunicorns/leapfrogai/raw/main/docs/imgs/leapfrogai.png)

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
  - [SDK](#sdk)
  - [User Interface](#user-interface)
  - [Repeater](#repeater)
- [Usage](#usage)
  - [Flavors](#flavors)
  - [UDS](#uds)
    - [UDS Latest](#uds-latest)
    - [UDS Dev](#uds-dev)
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

```shell
leapfrogai/
├── src/
│   ├── leapfrogai_api/   # source code for the API
│   ├── leapfrogai_sdk/   # source code for the SDK
│   └── leapfrogai_ui/    # source code for the UI
├── packages/
│   ├── api/              # deployment infrastructure for the API
│   ├── llama-cpp-python/ # source code & deployment infrastructure for the llama-cpp-python backend
│   ├── repeater/         # source code & deployment infrastructure for the repeater model backend  
│   ├── supabase/         # deployment infrastructure for the Supabase backend and postgres database
│   ├── text-embeddings/  # source code & deployment infrastructure for the text-embeddings backend
│   ├── ui/               # deployment infrastructure for the UI
│   ├── vllm/             # source code & deployment infrastructure for the vllm backend
│   └── whisper/          # source code & deployment infrastructure for the whisper backend
├── uds-bundles/
│   ├── dev/              # uds bundles for local uds dev deployments
│   └── latest/           # uds bundles for the most current uds deployments
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

LeapfrogAI provides several backends for a variety of use cases.

> Available Backends:
> | Backend | AMD64 Support | ARM64 Support | Cuda Support | Docker Ready | K8s Ready | Zarf Ready |
> | --- | --- | --- | --- | --- | --- | --- |
> | [llama-cpp-python](packages/llama-cpp-python/) | ✅ | 🚧 | ✅ | ✅ | ✅ | ✅ |
> | [whisper](packages/whisper/) | ✅ | 🚧 | ✅ | ✅ | ✅ | ✅ |
> | [text-embeddings](packages/text-embeddings/) | ✅ | 🚧 | ✅ | ✅ | ✅ | ✅ |
> | [vllm](packages/vllm/) | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ |

### SDK

The LeapfrogAI [SDK](src/leapfrogai_sdk/) provides a standard set of protobuff and python utilities for implementing backends and gRPC.

### User Interface

LeapfrogAI provides a [User Interface](src/leapfrogai_ui/) with support for common use-cases such as chat, summarization, and transcription.

### Repeater

The [repeater](packages/repeater/) "model" is a basic "backend" that parrots all inputs it receives back to the user. It is built out the same way all the actual backends are and it primarily used for testing the API.

## Usage

### Flavors

Each component has different images and values that refer to a specific image registry and/or hardening source. These images are packaged using [Zarf Flavors](https://docs.zarf.dev/ref/examples/package-flavors/):

1. `upstream`: uses upstream vendor images from open source container registries and repositories
2. (WIP) `registry1`: uses [IronBank hardened images](https://repo1.dso.mil/dsop) from the Repo1 harbor registry
3. (WIP) `unicorn`: uses [Chainguard hardened images](https://www.chainguard.dev/chainguard-images) from the Chainguard registry

### UDS

LeapfrogAI can be deployed and run locally via UDS and Kubernetes, built out using [Zarf](https://zarf.dev) packages. See the [Quick Start](https://docs.leapfrog.ai/docs/local-deploy-guide/quick_start/#prerequisites) for a list of prerequisite packages that must be installed first.

Prior to deploying any LeapfrogAI packages, a UDS Kubernetes cluster must be deployed using the most recent k3d bundle:

```sh
make create-uds-cpu-cluster
```

#### UDS Latest

This type of deployment pulls the most recent package images and is the most stable way of running a local LeapfrogAI deployment. These instructions can be found on the [LeapfrogAI Docs](https://docs.leapfrog.ai/docs/) site.

#### UDS Dev

If you want to make some changes to LeapfrogAI before deploying via UDS (for example in a dev environment), follow the [UDS Dev Instructions](/uds-bundles/dev/README.md).

### Local Dev

Each of the LFAI components can also be run individually outside of a Kubernetes environment via local development. This is useful when testing changes to a specific component, but will not assist in a full deployment of LeapfrogAI. Please refer to the above sections for deployment instructions.

Please refer to the linked READMEs for each individual packages local development instructions:

- [API](/src/leapfrogai_api/README.md)
- [llama-cpp-python](/packages/llama-cpp-python/README.md)
- [repeater](/packages/repeater/README.md)
- [supabase](/packages/supabase/README.md)
- [text-embeddings](/packages/text-embeddings/README.md)
- [ui](/src/leapfrogai_ui/README.md)
- [vllm](/packages/vllm/README.md)
- [whisper](/packages/whisper/README.md)

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
