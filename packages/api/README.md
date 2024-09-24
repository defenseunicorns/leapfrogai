# LeapfrogAI Python API

A Python API that exposes AI backends, via FastAPI and gRPC, in the [OpenAI API specification](https://platform.openai.com/docs/api-reference).

## Usage

### Pre-Requisites

See the LeapfrogAI documentation website for [system requirements](https://docs.leapfrog.ai/docs/local-deploy-guide/requirements/) and [dependencies](https://docs.leapfrog.ai/docs/local-deploy-guide/dependencies/).

#### Dependent Components

- [UDS Kubernetes cluster bootstrapped with UDS Core Slim Dev](../k3d-gpu/README.md) for local KeyCloak authentication, Istio Service Mesh, and MetalLB advertisement
- [Supabase](../supabase/README.md) for a vector database to store resulting embeddings in, and user management and authentication
- [Text Embeddings](../text-embeddings/README.md) for RAG
- [LLaMA C++ Python](../llama-cpp-python/README.md) or [vLLM](../vllm/README.md) for completions and chat completions

### Deployment

To build and deploy the API Zarf package into an existing [UDS Kubernetes cluster](../k3d-gpu/README.md):

> [!IMPORTANT]
> Execute the following commands from the root of the LeapfrogAI repository

```bash
make build-api LOCAL_VERSION=dev FLAVOR=upstream
uds zarf package deploy packages/api/zarf-package-leapfrogai-api-*-dev.tar.zst --confirm
```

For other package flavors, use the following example:

```bash
make build-api FLAVOR=registry1
uds zarf package deploy packages/api/zarf-package-leapfrogai-api-*-dev.tar.zst --confirm
```

### Local Development

See the [source code documentation](../../src/leapfrogai_api/README.md) for running the API from the source code for local Python environment development.
