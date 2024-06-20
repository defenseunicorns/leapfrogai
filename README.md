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
  - [Image Hardening](#image-hardening)
  - [SDK](#sdk)
  - [User Interface](#user-interface)
  - [Repeater](#repeater)
- [Usage](#usage)
  - [UDS (Latest)](#uds-latest)
  - [UDS (Dev)](#uds-dev)
    - [CPU](#cpu)
    - [GPU](#gpu)
  - [Accessing the UI](#accessing-the-ui)
  - [Cleanup](#cleanup)
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
│   ├── leapfrogai_api/     # source code for the API
│   ├── leapfrogai_sdk/     # source code for the SDK
│   └── leapfrogai_ui/      # source code for the UI
├── packages/
│   ├── api/                # deployment infrastructure for the API
│   ├── llama-cpp-python/   # source code & deployment infrastructure for the llama-cpp-python backend
│   ├── repeater/           # source code & deployment infrastructure for the repeater model backend  
│   ├── supabase/           # deployment infrastructure for the supabase database
│   ├── text-embeddings/    # source code & deployment infrastructure for the text-embeddings backend
│   ├── ui/                 # deployment infrastructure for the UI
│   ├── vllm/               # source code & deployment infrastructure for the vllm backend
│   └── whisper/            # source code & deployment infrastructure for the whisper backend
├── uds-bundles/
│   ├── dev/                # uds bundles for local uds dev deployments
│   └── latest/             # uds bundles for the most current uds deployments
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

### Image Hardening

> GitHub Repo:
>
> - [leapfrogai-images](https://github.com/defenseunicorns/leapfrogai-images)

LeapfrogAI leverages Chainguard's [apko](https://github.com/chainguard-dev/apko) to harden base python images - pinning Python versions to the latest supported version by the other components of the LeapfrogAI stack.

### SDK

The LeapfrogAI [SDK](src/leapfrogai_sdk/) provides a standard set of protobuff and python utilities for implementing backends and gRPC.

### User Interface

LeapfrogAI provides a [User Interface](src/leapfrogai_ui/) with support for common use-cases such as chat, summarization, and transcription.

### Repeater

The [repeater](packages/repeater/) "model" is a basic "backend" that parrots all inputs it receives back to the user. It is built out the same way all the actual backends are and it primarily used for testing the API.

## Usage

### UDS (Latest)

LeapfrogAI can be deployed and run locally via UDS and Kubernetes, built out using [Zarf](https://zarf.dev) packages. This pulls the most recent package images and is the most stable way of running a local LeapfrogAI deployment. These instructions can be found on the [LeapfrogAI Docs](https://docs.leapfrog.ai/docs/) site.

### UDS (Dev)

If you want to make some changes to LeapfrogAI before deploying via UDS (for example in a dev environment), you can follow these instructions:

Make sure your system has the [required dependencies](https://docs.leapfrog.ai/docs/local-deploy-guide/quick_start/#prerequisites).

For ease, it's best to create a virtual environment:

```shell
python -m venv .venv
source .venv/bin/activate
```

Each component is built into its own Zarf package. You can build all of the packages you need at once with the following `Make` targets:

```shell
make build-cpu    # api, llama-cpp-python, text-embeddings, whisper, supabase
make build-gpu    # api, vllm, text-embeddings, whisper, supabase
make build-all    # all of the backends
```

**OR**

You can build components individually using the following `Make` targets:

```shell
make build-api
make build-supabase
make build-vllm                 # if you have GPUs
make build-llama-cpp-python     # if you have CPU only
make build-text-embeddings
make build-whisper
```

Once the packages are created, you can deploy either a CPU or GPU-enabled deployment via one of the UDS bundles:

#### CPU

```shell
cd uds-bundles/dev/cpu
uds create .
uds deploy k3d-core-slim-dev:0.22.2
uds deploy uds-bundle-leapfrogai*.tar.zst
```

#### GPU

```shell
cd uds-bundles/dev/gpu
uds create .
uds deploy k3d-core-slim-dev:0.22.2 --set K3D_EXTRA_ARGS="--gpus=all --image=ghcr.io/justinthelaw/k3d-gpu-support:v1.27.4-k3s1-cuda"     # be sure to check if a newer version exists
uds deploy uds-bundle-leapfrogai-*.tar.zst --confirm
```

### Accessing the UI

LeapfrogAI is integrated with the UDS Core KeyCloak service, which provides authentication via SSO. Below are general instructions for accessing the LeapfrogAI UI after a successful UDS deployment of UDS Core and LeapfrogAI.

1. Connect to the KeyCloak admin panel
    - Run the following to get a port-forwarded tunnel:  `uds zarf connect keycloak`
    - Go to the resulting localhost URL and create an admin account

2. Go to ai.uds.dev and press "Login using SSO"

3. Register a new user by pressing "Register Here"

4. Fill-in all of the information
    - The bot detection requires you to scroll and click around in a natural way, so if the Register button is not activated despite correct information, try moving around the page until the bot detection says 100% verified

5. Using an authenticator, follow the MFA steps

6. Go to sso.uds.dev
    - Login using the admin account you created earlier

7. Approve the newly registered user
    - Click on the hamburger menu in the top left to open/close the sidebar
    - Go to the dropdown that likely says "Keycloak" and switch to the "uds" context
    - Click "Users" in the sidebar
    - Click on the newly registered user's username
    - Go to the "Email Verified" switch and toggle it to be "Yes"
    - Scroll to the bottom and press "Save"

8. Go back to ai.uds.dev and login as the registered user to access the UI

### Cleanup

To clean-up or perform a fresh install, run the following commands in the context in which you had previously installed UDS Core and LeapfrogAI:

```bash
k3d cluster delete uds  # kills a running uds cluster
uds zarf tools clear-cache # clears the Zarf tool cache
rm -rf ~/.uds-cache # clears the UDS cache
docker system prune -a -f # removes all hanging containers and images
docker volume prune -f # removes all hanging container volumes
```

### Local Dev

Each of the LFAI components can also be run individually outside a deployment environment via local development. This is useful when testing changes to a specific component, but will not assist in a full deployment of LeapfrogAI. Please refer to the above sections for deployment instructions.

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
