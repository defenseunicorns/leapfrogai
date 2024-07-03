---
title: Quick Start
type: docs
weight: 2
---

# LeapfrogAI UDS Deployment

The fastest and easiest way to get started with a deployment of LeapfrogAI is by using [UDS](https://github.com/defenseunicorns/uds-core). These quick start instructions show how to deploy LeapfrogAI in either a CPU or GPU-enabled environment.

## System Requirements

Please review the following table to ensure your system meets the minimum requirements. LFAI can be run with or without GPU-access, but GPU-enabled systems are recommended due to the performance gains. The following assumes a single personal device:

|     | Minimum           | Recommended (Performance) |
|-----|-------------------|---------------------------|
| RAM | 32 GB             | 128 GB                    |
| CPU | 8 Cores @ 3.0 GHz | 32 Cores @ 3.0 GHz        |
| GPU | N/A               | 2x NVIDIA RTX 4090 GPUs   |

Additionally, please check the list of tested [operating systems](https://docs.leapfrog.ai/docs/local-deploy-guide/requirements/#operating-systems) for compatibility.

## Prerequisites

- [Docker](https://docs.docker.com/engine/install/)
- [K3D](https://k3d.io/)
- [Zarf](https://docs.zarf.dev/getting-started/install/)
- [UDS CLI](https://github.com/defenseunicorns/uds-cli)

GPU considerations (NVIDIA GPUs only):

- NVIDIA GPU must have the most up-to-date drivers installed.
- NVIDIA GPU drivers compatible with CUDA (>=12.2).
- NVIDIA Container Toolkit is available via internet access, pre-installed, or on a mirrored package repository in the air gap.

## Default Models
LeapfrogAI deploys with certain default models. The following models were selected to balance portability and performance for a base deployment:

| Backend          | CPU/GPU Support | Default Model                                                                |
|------------------|-----------------|------------------------------------------------------------------------------|
| llama-cpp-python | CPU             | [SynthIA-7B-v2.0-GGUF](https://huggingface.co/TheBloke/SynthIA-7B-v2.0-GGUF) |
| vllm             | GPU             | [Synthia-7B-v2.0-GPTQ](https://huggingface.co/TheBloke/SynthIA-7B-v2.0-GPTQ) |
| text-embeddings  | CPU/GPU         | [Instructor-XL](https://huggingface.co/hkunlp/instructor-xl)                 |
| whisper          | CPU/GPU         | [OpenAI whisper-base](https://huggingface.co/openai/whisper-base)            |

**NOTE:** If a user's system specifications are beyond the minimum requirements, advanced users are able to swap out the default model choices with larger or fine-tuned models.

## Disclaimers

GPU workloads **_WILL NOT_** run if GPU resources are unavailable to the pod(s). You must provide sufficient NVIDIA GPU scheduling or else the pod(s) will go into a crash loop.

`whisper` can run without GPU scheduling - just set the `GPU_LIMIT` value to `0`.

If `vllm` is being used with:

- A quantized model, then `QUANTIZATION` must be set to the quantization method (e.g., `awq`, `gptq`, etc.)
- Tensor parallelism for spreading a model's heads across multiple GPUs, then `TENSOR_PARALLEL_SIZE` must be set to an integer value that:
  a) falls within the number of GPU resources (`nvidia.com/gpu`) that are allocatable in the cluster
  b) divisible by the number of attention heads in the model architecture (if number of heads is 32, then `TENSOR_PARALLEL_SIZE` could be 2, 4, etc.)

These `vllm` specific environment variables must be set at the model skeleton level or when the model is deployed into the cluster.

## Instructions

Start by cloning the [LeapfrogAI Repository](https://github.com/defenseunicorns/leapfrogai.git):

``` bash
git clone https://github.com/defenseunicorns/leapfrogai.git
```

### CPU

From within the cloned repository, deploy K3D and the LeapfrogAI bundle:

``` bash
cd uds-bundles/latest/cpu/
uds create .
uds deploy k3d-core-slim-dev:0.22.2      # be sure to check if a newer version exists
uds deploy uds-bundle-leapfrogai-*.tar.zst --confirm
```

### GPU

In order to test the GPU deployment locally on K3d, use the following command when deploying UDS-Core:

```bash
 cd uds-bundles/latest/gpu/
 uds create .
 uds deploy k3d-core-slim-dev:0.22.2 --set K3D_EXTRA_ARGS="--gpus=all --image=ghcr.io/justinthelaw/k3d-gpu-support:v1.27.4-k3s1-cuda"     # be sure to check if a newer version exists
 uds deploy uds-bundle-leapfrogai-*.tar.zst --confirm
```

## Checking Deployment

Inspect the cluster using:

```bash
uds zarf tools monitor
```

| Tool       | URL                                   |
| ---------- | ------------------------------------- |
| UI         | <https://ai.uds.dev>                  |
| API        | <https://leapfrogai-api.uds.dev/docs> |
| RAG Server | <https://leapfrogai-rag.uds.dev/docs> |

## Accessing the UI

LeapfrogAI is integrated with the UDS Core KeyCloak service, which provides authentication via SSO. Below are general instructions for accessing the LeapfrogAI UI after a successful UDS deployment of UDS Core and LeapfrogAI.

1. Connect to the KeyCloak admin panel
  a. Run the following to get a port-forwarded tunnel:  `uds zarf connect keycloak`
  b. Go to the resulting localhost URL and create an admin account
2. Go to ai.uds.dev and press "Login using SSO"
3. Register a new user by pressing "Register Here"
4. Fill-in all of the information
  a. The bot detection requires you to scroll and click around in a natural way, so if the Register button is not activated despite correct information, try moving around the page until the bot detection says 100% verified
5. Using an authenticator, follow the MFA steps
6. Go to sso.uds.dev
  a. Login using the admin account you created earlier
7. Approve the newly registered user
  a. Click on the hamburger menu in the top left to open/close the sidebar
  b. Go to the dropdown that likely says "Keycloak" and switch to the "uds" context
  c. Click "Users" in the sidebar
  d. Click on the newly registered user's username
  e. Go to the "Email Verified" switch and toggle it to be "Yes"
  f. Scroll to the bottom and press "Save"
8. Go back to ai.uds.dev and login as the registered user to access the UI

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

- [UDS-Core](https://github.com/defenseunicorns/uds-core)
