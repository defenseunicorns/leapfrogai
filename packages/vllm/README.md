# LeapfrogAI vLLM Backend

A LeapfrogAI API-compatible [vllm](https://github.com/vllm-project/vllm) wrapper for quantized and un-quantized model inferencing across GPU infrastructures.

## Usage

### Pre-Requisites

See the LeapfrogAI documentation website for [system requirements](https://docs.leapfrog.ai/docs/local-deploy-guide/requirements/) and [dependencies](https://docs.leapfrog.ai/docs/local-deploy-guide/dependencies/).

#### Dependent Components

- [LeapfrogAI API](../api/README.md) for a fully RESTful application

### Model Selection

The default model that comes with this backend in this repository's officially released images is a [4-bit quantization of the Synthia-7b model](https://huggingface.co/TheBloke/SynthIA-7B-v2.0-GPTQ).

All of the commands in this sub-section are executed with the `packages/vllm` sub-directory.

Optionally, you can specify a different model during Zarf create:

```bash
uds zarf package create --confirm --set MODEL_REPO_ID=defenseunicorns/Hermes-2-Pro-Mistral-7B-4bit-32g --set MODEL_REVISION=main
```

If you decide to use a different model, there will likely be a need to change generation and engine runtime configurations, please see the [Zarf Package Config](./zarf-config.yaml) and the [values override file](./values/upstream-values.yaml) for details on what runtime parameters can be modified. These parameters are model-specific, and can be found in the HuggingFace model cards and/or configuration files (e.g., prompt templates).

For example, during deployment, you can override the Zarf Package Config defaults by doing the following:

```bash
uds zarf package deploy zarf-package-vllm-amd64-dev.tar.zst --confirm --set ENFORCE_EAGER=True
```

### Deployment

To build and deploy the vllm backend Zarf package into an existing [UDS Kubernetes cluster](../k3d-gpu/README.md):

> [!IMPORTANT]
> Execute the following commands from the root of the LeapfrogAI repository

```bash
pip install 'huggingface_hub[cli,hf_transfer]'  # Used to download the model weights from huggingface
make build-vllm LOCAL_VERSION=dev
uds zarf package deploy packages/vllm/zarf-package-vllm-*-dev.tar.zst --confirm
```

### Local Development

The [config.yaml](./config.yaml) and [.env.example](./.env.example) must be modified if the model has changed away from the default.

Create a `.env` file based on the [.env.example](./.env.example):

```bash
cp .env.example .env
```

To run the vllm backend locally:

> [!IMPORTANT]
> Execute the following commands from this sub-directory

```bash
# Install dev and runtime dependencies
make install

# Clone Model
python src/model_download.py

# Start the model backend
make dev
```
