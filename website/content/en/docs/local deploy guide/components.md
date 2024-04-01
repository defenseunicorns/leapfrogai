---
title: Components 
type: docs
weight: 3
---

## Components

### LeapfrogAI API

LeapfrogAI offers an API closely aligned with OpenAI's, facilitating seamless compatibility for tools developed with OpenAI/ChatGPT to operate seamlessly with a LeapfrogAI backend. The LeapfrogAI API is a Python API that exposes LLM backends, via FastAPI and gRPC, in the OpenAI API specification.

### Backend

LeapfrogAI offers several backends for a variety of use cases:

| Backend                                                                                    | Support                         |
| ------------------------------------------------------------------------------------------ | ------------------------------- |
| [llama-cpp-python](https://github.com/defenseunicorns/leapfrogai/tree/main/packages/llama-cpp-python) | AMD64, Docker, Kubernetes, Zarf |
| [whisper](https://github.com/defenseunicorns/leapfrogai/tree/main/packages/whisper)                   | AMD64, Docker, Kubernetes, Zarf |
| [text-embeddings](https://github.com/defenseunicorns/leapfrogai/tree/main/packages/text-embeddings)   | AMD64, Docker, Kubernetes, Zarf |
| [VLLM](https://github.com/defenseunicorns/leapfrogai/tree/main/packages/vllm)                         | AMD64, Docker, Kubernetes, Zarf |
| [RAG](https://github.com/defenseunicorns/leapfrogai-backend-rag)                           | AMD64, Docker, Kubernetes, Zarf |

### Image Hardening

LeapfrogAI utilizes Chainguard's [apko](https://github.com/chainguard-dev/apko) to fortify base Python images by adhering to a version-pinning approach, ensuring compatibility with the latest supported version by other components within the LeapfrogAI stack. Please see the [leapfrogai-images](https://github.com/defenseunicorns/leapfrogai-images) GitHub repository for additional information.

### Software Development Kit

The LeapfrogAI SDK offers a standardized collection of Protobuf and Python utilities designed to facilitate the implementation of backends and gRPC. Please see the [leapfrogai-sdk](https://github.com/defenseunicorns/leapfrogai-sdk) GitHub repository for additional information.

### User Interface

LeapfrogAI offers user-friendly interfaces tailored for common use-cases, including chat, summarization, and transcription, providing accessible options for users to initiate these tasks. Please see the [leapfrogai-ui](https://github.com/defenseunicorns/leapfrogai-ui) GitHub repository for additional information.
