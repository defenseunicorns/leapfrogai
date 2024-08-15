# LeapfrogAI vLLM Backend

A LeapfrogAI API-compatible [vllm](https://github.com/vllm-project/vllm) wrapper for quantized and un-quantized model inferencing across GPU infrastructures.

## Usage

### Pre-Requisites

See the LeapfrogAI documentation website for [system requirements](https://docs.leapfrog.ai/docs/local-deploy-guide/requirements/) and [dependencies](https://docs.leapfrog.ai/docs/local-deploy-guide/dependencies/).

#### Dependent Components

- [LeapfrogAI API](../api/README.md) for a fully RESTful application

### Model Selection

The default model that comes with this backend in this repository's officially released images is a [4-bit quantization of the Synthia-7b model](https://huggingface.co/TheBloke/SynthIA-7B-v2.0-GPTQ).

You can optionally specify different models or quantization types using the following Docker build arguments:

- `--build-arg HF_HUB_ENABLE_HF_TRANSFER="1"`: Enable or disable HuggingFace Hub transfer (default: 1)
- `--build-arg REPO_ID="TheBloke/Synthia-7B-v2.0-GPTQ"`: HuggingFace repository ID for the model
- `--build-arg REVISION="gptq-4bit-32g-actorder_True"`: Revision or commit hash for the model
- `--build-arg QUANTIZATION="gptq"`: Quantization type (e.g., gptq, awq, or empty for un-quantized)
- `--build-arg TENSOR_PARALLEL_SIZE="1"`: The number of gpus to spread the tensor processing across

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

To run the vllm backend locally:

> [!IMPORTANT]
> Execute the following commands from this sub-directory

```bash
# Install dev and runtime dependencies
make install

# Clone Model
python scripts/model_download.py

# Start the model backend
make dev
```
