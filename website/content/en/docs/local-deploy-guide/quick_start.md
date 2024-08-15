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

The following instructions are split into two sections:

1. [LeapfrogAI Latest](#leapfrogai-latest): for hassle-free deployment of the latest stable version of LeapfrogAI
2. [LeapfrogAI Development](#leapfrogai-development): for deployment of a unreleased branch, a fork or `main`

If you already have a pre-built UDS bundle, please skip to [Deploying the UDS Bundle](#deploying-the-uds-bundle)

If you are using MacOS, please skip to [MacOS Specific Instructions](#macos-specifics)

### LeapfrogAI Latest

1. Start by cloning the [LeapfrogAI Repository](https://github.com/defenseunicorns/leapfrogai):

    ``` bash
    git clone https://github.com/defenseunicorns/leapfrogai.git
    ```

2. From within the cloned repository create the LeapfrogAI bundle using **ONE** of the following:

    ```bash
    cd bundles/latest/cpu/
    uds create .
    uds deploy uds-bundle-leapfrogai-*.tar.zst --confirm

    cd bundles/latest/gpu/
    uds create .
    uds deploy uds-bundle-leapfrogai-*.tar.zst --confirm
    ```

3. Move on to [Deploying the UDS Bundle](#deploying-the-uds-bundle)

### LeapfrogAI Development

1. For ease, it's best to create a virtual environment for installing, managing and isolating package creation dependencies:

    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

2. Install all the necessary package creation dependencies:

    ```bash
    python -m pip install "hugging_face[cli,hf_transfer]" "transformers[torch]" ctranslate2
    ```

3. Build all of the packages you need at once with **ONE** of the following `Make` targets:

    ```bash
    LOCAL_VERSION=dev make build-cpu    # ui, api, llama-cpp-python, text-embeddings, whisper, supabase
    # OR
    LOCAL_VERSION=dev make build-gpu    # ui, api, vllm, text-embeddings, whisper, supabase
    # OR
    LOCAL_VERSION=dev make build-all    # all of the components
    ```

    **OR**

    You can build components individually using the following `Make` targets:

    ```bash
    LOCAL_VERSION=dev make build-ui
    LOCAL_VERSION=dev make build-api
    LOCAL_VERSION=dev make build-supabase
    LOCAL_VERSION=dev make build-vllm                 # if you have GPUs (macOS not supported)
    LOCAL_VERSION=dev make build-llama-cpp-python     # if you have CPU only
    LOCAL_VERSION=dev make build-text-embeddings
    LOCAL_VERSION=dev make build-whisper
    ```

## MacOS Specifics

To run the same commands in MacOS, you will need to prepend your command with a couple of env vars like so:

**All Macs:** `REG_PORT=5001`

**Apple Silicon (M1/M2/M3/M4 series) Macs:** `ARCH=arm64`

To demonstrate what this would look like for an Apple Silicon Mac:

``` shell
REG_PORT=5001 ARCH=arm64 LOCAL_VERSION=dev make build-cpu
```

To demonstrate what this would look like for an older Intel Mac:

``` shell
REG_PORT=5001 LOCAL_VERSION=dev make build-cpu
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
    # make sure you ar ein the directory with the UDS bundle archive
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
