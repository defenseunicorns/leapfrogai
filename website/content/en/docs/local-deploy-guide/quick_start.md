---
title: Quick Start
type: docs
weight: 2
---

# LeapfrogAI UDS Deployment

The fastest and easiest way to get started with a deployment of LeapfrogAI is by using [UDS](https://github.com/defenseunicorns/uds-core). These quick start instructions show how to deploy LeapfrogAI in either a CPU or GPU-enabled environment.

## Pre-Requisites

See the [Dependencies](https://docs.leapfrog.ai/docs/local-deploy-guide/dependencies/) and [Requirements](https://docs.leapfrog.ai/docs/local-deploy-guide/requirements/) pages for more details.

## Default Models

LeapfrogAI deploys with certain default models. The following models were selected to balance portability and performance for a base deployment:

| Backend          | CPU/GPU Support | Default Model                                                                |
|------------------|-----------------|------------------------------------------------------------------------------|
| llama-cpp-python | CPU             | [SynthIA-7B-v2.0-GGUF](https://huggingface.co/TheBloke/SynthIA-7B-v2.0-GGUF) |
| vllm             | GPU             | [Synthia-7B-v2.0-GPTQ](https://huggingface.co/TheBloke/SynthIA-7B-v2.0-GPTQ) |
| text-embeddings  | CPU/GPU         | [Instructor-XL](https://huggingface.co/hkunlp/instructor-xl)                 |
| whisper          | CPU/GPU         | [OpenAI whisper-base](https://huggingface.co/openai/whisper-base)            |

If a user's system specifications exceed the [minimum requirements](https://docs.leapfrog.ai/docs/local-deploy-guide/requirements/), advanced users are able to swap out the default model choices with larger or fine-tuned models. Examples of other models include:

- [defenseunicorns/Hermes-2-Pro-Mistral-7B-4bit-32g](https://huggingface.co/defenseunicorns/Hermes-2-Pro-Mistral-7B-4bit-32g)
- [justinthelaw/Phi-3-mini-128k-instruct-4bit-128g](https://huggingface.co/justinthelaw/Phi-3-mini-128k-instruct-4bit-128g)
- [NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO-GGUF](https://huggingface.co/NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO-GGUF)

## Disclaimers

The default configuration when deploying with GPU support assumes a single GPU. `vllm` is assigned the GPU resource. GPU workloads **_WILL NOT_** run if GPU resources are unavailable to the pod(s). You must provide sufficient NVIDIA GPU scheduling or else the pod(s) will go into a crash loop.

## Instructions

Start by cloning the [LeapfrogAI Repository](https://github.com/defenseunicorns/leapfrogai.git):

``` bash
git clone https://github.com/defenseunicorns/leapfrogai.git
```

### CPU

From within the cloned repository, deploy K3D and the LeapfrogAI bundle:

``` bash
make create-uds-cpu-cluster

cd bundles/latest/cpu/
uds create .
uds deploy uds-bundle-leapfrogai-*.tar.zst --confirm
```

### GPU

In order to test the GPU deployment locally on K3d, use the following command when deploying UDS-Core:

```bash
 make create-uds-gpu-cluster
 make test-uds-gpu-cluster # deploy a test gpu pod to see if everything is working

 cd bundles/latest/gpu/
 uds create .
 uds deploy uds-bundle-leapfrogai-*.tar.zst --confirm
```

## Checking Deployment

Once the cluster and LFAI have deployed, the cluster and pods can be inspected using uds:

```bash
uds zarf tools monitor
```

The following URLs should now also be available to view LFAI resources:

**DISCLAIMER**: These URls will only be available *after* both K3D-core and LFAI have been deployed. They will also only be available on the host system that deployed the cluster.

| Tool       | URL                                   |
| ---------- | ------------------------------------- |
| UI         | <https://ai.uds.dev>                  |
| API        | <https://leapfrogai-api.uds.dev/docs> |

## Clean-up

To clean-up or perform a fresh install, run the following commands in the context in which you had previously installed UDS Core and LeapfrogAI:

```bash
k3d cluster delete uds  # kills a running uds cluster
uds zarf tools clear-cache # clears the Zarf tool cache
rm -rf ~/.uds-cache # clears the UDS cache
docker system prune -a -f # removes all hanging containers and images
docker volume prune -f # removes all hanging container volumes
```

## References

- [UDS Core](https://github.com/defenseunicorns/uds-core)
- [UDS CLI](https://github.com/defenseunicorns/uds-cli)
