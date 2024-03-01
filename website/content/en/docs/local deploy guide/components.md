---
title: Components 
type: docs
weight: 2
---

## Components

### Sandbox Deployment

[Tadpole](https://github.com/defenseunicorns/tadpole) serves as a straightforward method to set up LeapfrogAI for local use. Although **not suitable for production environments**, it aids users in understanding the different components of LeapfrogAI and their interactions.

### Advanced LeapfrogAI Deployment

The LeapfrogAI deployment guide is designed to guide advanced users through the process of deploying the latest production version of LeapfrogAI locally on Kubernetes.

### LeapfrogAI API

LeapfrogAI offers an [API](https://github.com/defenseunicorns/leapfrogai-api) closely aligned with OpenAI's, facilitating seamless compatibility for tools developed with OpenAI/ChatGPT to operate seamlessly with a LeapfrogAI backend. The LeapfrogAI API is a Python API that exposes LLM backends, via FastAPI and gRPC, in the OpenAI API specification.

### Backend

LeapfrogAI offers several backends for a variety of use cases:

| Backend                                                                                    | Support                         |
| ------------------------------------------------------------------------------------------ | ------------------------------- |
| [llama-cpp-python](https://github.com/defenseunicorns/leapfrogai-backend-llama-cpp-python) | AMD64, Docker, Kubernetes, Zarf |
| [whisper](https://github.com/defenseunicorns/leapfrogai-backend-whisper)                   | AMD64, Docker, Kubernetes, Zarf |
| [instructor-xl](https://github.com/defenseunicorns/leapfrogai-backend-instructor-xl)       | AMD64, Docker, Kubernetes       |
| [VLLM](https://github.com/defenseunicorns/leapfrogai-backend-vllm)                         |                                 |

### Image Hardening

LeapfrogAI utilizes Chainguard's [apko](https://github.com/chainguard-dev/apko) to fortify base Python images by adhering to a version-pinning approach, ensuring compatibility with the latest supported version by other components within the LeapfrogAI stack. Please see the [leapfrogai-images](https://github.com/defenseunicorns/leapfrogai-images) GitHub repository for additional information.

### Software Development Kit

The LeapfrogAI SDK offers a standardized collection of Protobuf and Python utilities designed to facilitate the implementation of backends and gRPC. Please see the [leapfrogai-sdk](https://github.com/defenseunicorns/leapfrogai-sdk) GitHub repository for additional information.

### User Interface

LeapfrogAI offers user-friendly interfaces tailored for common use-cases, including chat, summarization, and transcription, providing accessible options for users to initiate these tasks. Please see the [leapfrogai-ui](https://github.com/defenseunicorns/leapfrogai-ui) GitHub repository for additional information.
