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

| Backend | AMD64 Support | ARM64 Support | Cuda Support | Docker Ready | K8s Ready | Zarf Ready |
| --- | --- | --- | --- | --- | --- | --- |
| [llama-cpp-python](https://github.com/defenseunicorns/leapfrogai/tree/main/packages/llama-cpp-python) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| [whisper](https://github.com/defenseunicorns/leapfrogai/tree/main/packages/whisper) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| [text-embeddings](https://github.com/defenseunicorns/leapfrogai/tree/main/packages/text-embeddings) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| [vllm](https://github.com/defenseunicorns/leapfrogai/tree/main/packages/vllm) | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ |

### Flavors

Each component has different images and values that refer to a specific image registry and/or hardening source. These images are packaged using [Zarf Flavors](https://docs.zarf.dev/ref/examples/package-flavors/):

1. `upstream`: uses upstream vendor images from open source container registries and repositories
2. 🚧 `registry1`: uses [IronBank hardened images](https://repo1.dso.mil/dsop) from the Repo1 harbor registry
3. 🚧 `unicorn`: uses [Chainguard hardened images](https://www.chainguard.dev/chainguard-images) from the Chainguard registry

### Artifact Support

LeapfrogAI contains built-in embeddings for RAG and transcription / translation solutions that can handle many different file types. Many of these capabilities are accessible via the LeapfrogAI API. The support artifact types are as follows:

#### Transcription / Translation

- All formats supported by `ffmpeg -formats`, e.g., `.mp3`, `.wav`, `.mp4`, etc.

#### Embeddings for RAG

- `.pdf`
- `.txt`
- `.html`
- `.htm`
- `.csv`
- `.md`
- `.doc`
- `.docx`
- `.xlsx`
- `.xls`
- `.pptx`
- `.ppt`

### Software Development Kit

The LeapfrogAI SDK offers a standardized collection of Protobuf and Python utilities designed to facilitate the implementation of backends and gRPC. Please see the [LeapfrogAI SDK](https://github.com/defenseunicorns/leapfrogai/tree/main/src/leapfrogai_sdk) sub-directory for the source code and details.

### User Interface

LeapfrogAI offers user-friendly interfaces tailored for common use-cases, including chat, summarization, and transcription, providing accessible options for users to initiate these tasks. Please see the [LeapfrogAI UI](https://github.com/defenseunicorns/leapfrogai/tree/main/src/leapfrogai_ui)GitHub repository for additional information.