![LeapfrogAI Logo](https://github.com/defenseunicorns/leapfrogai/raw/main/docs/imgs/leapfrogai.png)

[![](https://dcbadge.vercel.app/api/server/s2Ja5cmZRQ)](https://discord.gg/s2Ja5cmZRQ)

## Table of Contents
- [Table of Contents](#table-of-contents)
- [Overview](#overview)
- [Why Host Your Own LLM?](#why-host-your-own-llm)
- [Components](#components)
  - [Getting Started](#getting-started)
  - [API](#api)
  - [Backends](#backends)
  - [Image Hardening](#image-hardening)
  - [SDK](#sdk)
  - [User Interface](#user-interface)
- [Community](#community)

## Overview

LeapfrogAI is a self-hosted AI platform designed to be deployed in air-gapped environments. This project aims to bring sophisticated AI solutions to air-gapped resource-constrained environments, by enabling the hosting all requisite components of an AI stack.

Our services include vector databases, model backends, API, and UI. These capabilities can be easily accessed and integrated with your existing infrastructure, ensuring the power of AI can be harnessed irrespective of your environment's limitations.

## Why Host Your Own LLM?

Large Language Models (LLMs) are a powerful resource for AI-driven decision making, content generation, and more. How can LeapfrogAI bring AI to your mission?

- **Data Independence**: Sending sensitive information to a third-party service may not be suitable or permissible for all types of data or organizations. By hosting your own LLM, you retain full control over your data.

- **Scalability**: Pay-as-you-go AI services can become expensive, especially when large volumes of data are involved and require constant connectivity. Running your own LLM can often be a more cost-effective solution for missions of all sizes.

- **Mission Integration**: By hosting your own LLM, you have the ability to customize the model's parameters, training data, and more, tailoring the AI to your specific needs.

## Components

### Getting Started

> GitHub Repo:
>
> - [Tadpole](https://github.com/defenseunicorns/tadpole)

Tadpole is a simple way to get LeapfrogAI up and running locally. While not intended for production, it helps the user to understand the various components of LeapfrogAI and how they interact.

### API

> GitHub Repo:
>
> - [leapfrog-api](https://github.com/defenseunicorns/leapfrogai-api)

LeapfrogAI provides an API that closely matches that of OpenAI's. This feature allows tools that have been built with OpenAI/ChatGPT to function seamlessly with a LeapfrogAI backend.

### Backends

> GitHub Repos:
> | Repo | AMD64 Support | ARM64 Support | Cuda Support | Docker Ready | K8s Ready | Zarf Ready |
> | --- | --- | --- | --- | --- | --- | --- |
> | [llama-cpp-python](https://github.com/defenseunicorns/leapfrogai-backend-llama-cpp-python) | ✅ | 🚧 | 🚧 | ✅ | ✅ | ✅ |
> | [whisper](https://github.com/defenseunicorns/leapfrogai-backend-whisper) | ✅ | 🚧 | ✅ | ✅ | ✅ | ✅ |
> | [ctransformers](https://github.com/defenseunicorns/leapfrogai-backend-ctransformers) | ✅ | 🚧 | 🚧 | ✅ | ✅ | ✅ |
> | [text-embeddings](https://github.com/defenseunicorns/leapfrogai-backend-text-embeddings) | ✅ | 🚧 | ✅ | ✅ | ✅ | ✅ |
> | [vllm](https://github.com/defenseunicorns/leapfrogai-backend-vllm) | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ |

LeapfrogAI provides several backends for a variety of use cases.

### Image Hardening

> GitHub Repo:
>
> - [leapfrogai-images](https://github.com/defenseunicorns/leapfrogai-images)

LeapfrogAI leverages Chainguard's [apko](https://github.com/chainguard-dev/apko) to harden base python images - pinning Python versions to the latest supported version by the other components of the LeapfrogAI stack.

### SDK

> GitHub Repo: [leapfrogai-sdk](https://github.com/defenseunicorns/leapfrogai-sdk)

The LeapfrogAI SDK provides a standard set of protobuff and python utilities for implementing backends and gRPC.

### User Interface

> GitHub Repo:
>
> - [leapfrog-ui](https://github.com/defenseunicorns/leapfrog-ui)

LeapfrogAI provides some options of UI to get started with common use-cases such as chat, summarization, and transcription.

### Advanced Deployments

> GitHub Repo:
>
> - [leapfrogai-deployment](https://github.com/defenseunicorns/leapfrogai-deployment)

These instructions will assist advanced users in standing up the latest production version of LeapfrogAI on Kubernetes.

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
