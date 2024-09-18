---
title: Quick Start
type: docs
weight: 3
---

# LeapfrogAI UDS Deployment

The fastest and easiest way to get started with a deployment of LeapfrogAI is by using [UDS](https://github.com/defenseunicorns/uds-core). These quick start instructions show how to deploy LeapfrogAI in either a CPU or GPU-enabled environment.

## Pre-Requisites

See the [Dependencies](https://docs.leapfrog.ai/docs/local-deploy-guide/dependencies/) and [Requirements](https://docs.leapfrog.ai/docs/local-deploy-guide/requirements/) pages for more details.

## Default Models

LeapfrogAI deploys with certain default models. The following models were selected to balance portability and performance for a base deployment:

| Backend            | CPU/GPU Support   | Default Model                                                                  |
| ------------------ | ----------------- | ------------------------------------------------------------------------------ |
| llama-cpp-python   | CPU               | [SynthIA-7B-v2.0-GGUF](https://huggingface.co/TheBloke/SynthIA-7B-v2.0-GGUF)   |
| vllm               | GPU               | [Synthia-7B-v2.0-GPTQ](https://huggingface.co/TheBloke/SynthIA-7B-v2.0-GPTQ)   |
| text-embeddings    | CPU/GPU           | [Instructor-XL](https://huggingface.co/hkunlp/instructor-xl)                   |
| whisper            | CPU/GPU           | [OpenAI whisper-base](https://huggingface.co/openai/whisper-base)              |

If a user's system specifications exceed the [minimum requirements](https://docs.leapfrog.ai/docs/local-deploy-guide/requirements/), advanced users are able to swap out the default model choices with larger or fine-tuned models.

Examples of other models to put into vLLM or LLaMA C++ Python that are not sponsored nor owned by Defense Unicorns include:

- [defenseunicorns/Hermes-2-Pro-Mistral-7B-4bit-32g](https://huggingface.co/defenseunicorns/Hermes-2-Pro-Mistral-7B-4bit-32g)
- [hugging-quants/Meta-Llama-3.1-70B-Instruct-AWQ-INT4](https://huggingface.co/hugging-quants/Meta-Llama-3.1-70B-Instruct-AWQ-INT4)
- [justinthelaw/Phi-3-mini-128k-instruct-4bit-128g](https://huggingface.co/justinthelaw/Phi-3-mini-128k-instruct-4bit-128g)
- [NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO-GGUF](https://huggingface.co/NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO-GGUF)

The default configuration when deploying with GPU support assumes a single GPU. `vllm` is assigned the GPU resource. GPU workloads **_WILL NOT_** run if GPU resources are unavailable to the pod(s). You must provide sufficient NVIDIA GPU scheduling or else the pod(s) will go into a crash loop. See the [Dependencies](https://docs.leapfrog.ai/docs/local-deploy-guide/dependencies/) and [Requirements](https://docs.leapfrog.ai/docs/local-deploy-guide/requirements/) pages for more details.

## Building the UDS Bundle

If you already have a pre-built UDS bundle, please skip to [Deploying the UDS Bundle](#deploying-the-uds-bundle)

1. Start by cloning the [LeapfrogAI Repository](https://github.com/defenseunicorns/leapfrogai):

    ``` bash
    git clone https://github.com/defenseunicorns/leapfrogai.git
    ```

2. From within the cloned repository create the LeapfrogAI bundle using **ONE** of the following:

    ```bash
    # For CPU-only
    cd bundles/latest/cpu/
    uds create .

    # For compatible AMD64, NVIDIA CUDA-capable GPU machines
    cd bundles/latest/gpu/
    uds create .
    ```

## Deploying the UDS bundle

1. Deploy a UDS Kubernetes cluster with **ONE** of the following:

    ```bash
    make create-uds-cpu-cluster     # if you have CPUs only
    # OR
    make create-uds-gpu-cluster     # if you have GPUs (macOS not supported)
    ```

2. Deploy the bundle you created in the [previous steps](#building-the-uds-bundle):

    ```bash
    # make sure you are in the directory with the UDS bundle archive
    uds deploy uds-bundle-leapfrogai*.tar.zst
    ```

## Checking Deployment

Once the cluster and LFAI have deployed, the cluster and pods can be inspected using uds:

```bash
uds zarf tools monitor
```

These URLs will only be accessible *after* the UDS Kubernetes cluster and LeapfrogAI have been deployed:

| Tool                  | URL                                   |
| --------------------- | ------------------------------------- |
| LeapfrogAI UI         | <https://ai.uds.dev>                  |
| LeapfrogAI API        | <https://leapfrogai-api.uds.dev/docs> |
| Supabase Console      | <https://supabase-kong.uds.dev>       |
| KeyCloak User Page    | <https://sso.uds.dev>                 |
| KeyCloak Admin Panel  | <https://keycloak.admin.uds.dev>      |

## Clean-up

To clean-up or perform a fresh install, run the following commands in the context in which you had previously installed UDS Core and LeapfrogAI:

```bash
k3d cluster delete uds  # kills a running uds cluster
uds zarf tools clear-cache # clears the Zarf tool cache
rm -rf ~/.uds-cache && rm -rf /tmp/zarf-* # clears the UDS and Zarf temporary files
docker system prune -a -f # removes all hanging containers and images
docker volume prune -f # removes all hanging container volumes
```

## References

- [UDS Core](https://github.com/defenseunicorns/uds-core)
- [UDS CLI](https://github.com/defenseunicorns/uds-cli)

## Further Tinkering

For more LeapfrogAI customization options and developer-level documentation, please visit the [LeapfrogAI GitHub](https://github.com/defenseunicorns/leapfrogai) project for more details.
