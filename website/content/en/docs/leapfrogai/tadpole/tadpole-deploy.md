---
title: Sandbox Deployment
type: docs
---

## Overview

The Tadpole sandbox deployment is the lightweight method to initiate your LeapfrogAI experience and is exclusively designed for **local testing and development purposes only**. Tadpole facilitates a non-Kubernetes deployment that executes a `docker compose` build of the LeapfrogAI API, language backend, and user interface. To ensure a smooth start, there are a collection of straightforward basic recipes. Executing any of these recipes initiates the automated processes within Tadpole, encompassing the build, configuration, and initiation of the necessary components. The culmination of this process results in a locally hosted "Chat with an LLM" demonstration.

### Prerequisites

- Have [Docker](https://docs.docker.com/get-docker/) installed.
- Have [Continue.dev](https://continue.dev/) installed.
  
### System Requirements

- `chat` and `code` recipes require a minimum of 16GB RAM.
- `chat-gpu` recipe requires a minimum of 8GB VRAM and a CUDA capable NVIDIA GPU with drivers setup in order to function correctly with Docker.

{{% alert-note %}}
To set up your CUDA capable NVIDIA GPU, please see the following instructions:

- Prepare your machine for [NVIDIA Driver installation.](https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html#pre-installation-actions)
- Install the proper [NVIDIA Drivers.](https://docs.nvidia.com/datacenter/tesla/tesla-installation-notes/index.html#pre-install)
- Find the correct [CUDA for your environment.](https://developer.nvidia.com/cuda-downloads)
- [Install CUDA](https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html#pre-installation-actions) properly.
- Prepare Docker for [GPU accessibility.](https://docs.docker.com/config/containers/resource_constraints/#gpu)
- Obtain the [NVIDIA device plugin](https://github.com/NVIDIA/k8s-device-plugin) for Kubernetes.
{{% /alert-note %}}

### Operating Systems

- macOS: Only CPU recipes are compatible at this time.
- Windows: CPU recipes are compatible. GPU recipes require that the [Windows Subsystem for Linux](https://learn.microsoft.com/en-us/windows/wsl/install) is installed.
- Linux: CPU and GPU recipes are compatible.  

## Getting Started

### Clone

Clone into the [Tadpole GitHub repository](https://github.com/defenseunicorns/tadpole).

{{% alert-note %}}
Cloning into this repository requires that users have an SSH key associated with your GitHub account. Please follow the [GitHub SSH documentation](https://docs.github.com/en/authentication/connecting-to-github-with-ssh) to obtain this key.
{{% /alert-note %}}

### Chat

To spin up the Tadpole chatbot to your local environment:

```git
make chat
```

The Leapfrog-UI will be running at `http://localhost:3000/`.

### Code

{{% alert-note %}}
This recipe is intended for use with a code extension such as [Continue.dev](https://continue.dev/) and has been tested with the v0.7.53 prerelease.
{{% /alert-note %}}

To build and run the code backend:

```git
make code
```

Navigate to `$HOME/.continue/config.json` and modify your [Continue.dev](https://continue.dev/) configuration:

```git
{
  "models":
  [{
    "title": "leapfrogai",
    "provider": "openai",
    "model": "leapfrogai",
    "apiKey": "freeTheModels",
    "apiBase": "http://localhost:8080/openai"
  }],
  "modelRoles": 
  {
      "default": "leapfrogai"
  }
}
```

### Chat-GPU

{{% alert-note %}}
This requires a CUDA capable NVIDIA GPU with drivers setup.
{{% /alert-note %}}

To activate GPU resources and increase response time for your chatbot:

```git
make chat-gpu
```

The Leapfrog-UI will be running at `http://localhost:3000/`.

### Cleanup

When you are finished, run this cleanup command to remove Tadpole from your system:

```git
make clean
```

For any additional information, or to report an issue, please see the [Tadpole GitHub repository.](https://github.com/defenseunicorns/tadpole/tree/main)
