# LeapfrogAI UI

A Svelte UI that provides an easy-to-use frontend for interacting with all components of the LeapfrogAI tech stack.

## Usage

### Pre-Requisites

See the LeapfrogAI documentation website for [system requirements](https://docs.leapfrog.ai/docs/local-deploy-guide/requirements/) and [dependencies](https://docs.leapfrog.ai/docs/local-deploy-guide/dependencies/).

#### Dependent Components

- [UDS Kubernetes cluster bootstrapped with UDS Core Slim Dev](../k3d-gpu/README.md) for local KeyCloak authentication, Istio Service Mesh, and MetalLB advertisement
- [LeapfrogAI API](../api/README.md) for OpenAI API-like AI model backend interaction
- [Supabase](../supabase/README.md) for a vector database to store resulting embeddings in, and user management and authentication
- [Text Embeddings](../text-embeddings/README.md) for RAG
- [LLaMA C++ Python](../llama-cpp-python/README.md) or [vLLM](../vllm/README.md) for completions and chat completions

### Deployment

To build and deploy the UI Zarf package into an existing [UDS Kubernetes cluster](../k3d-gpu/README.md):

> [!IMPORTANT]
> Execute the following commands from the root of the LeapfrogAI repository

```bash
make build-ui LOCAL_VERSION=dev
uds zarf package deploy packages/ui/zarf-package-leapfrogai-ui-*-dev.tar.zst --confirm
```

### Local Development

See the [source code documentation](../../src/leapfrogai_ui/README.md) for running the UI from the source code for local Node environment development.
