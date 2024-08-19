# LeapfrogAI vLLM Backend

A LeapfrogAI API-compatible [vllm](https://github.com/vllm-project/vllm) wrapper for quantized and un-quantized model inferencing across GPU infrastructures.

## Usage

### Pre-Requisites

See the LeapfrogAI documentation website for [system requirements](https://docs.leapfrog.ai/docs/local-deploy-guide/requirements/) and [dependencies](https://docs.leapfrog.ai/docs/local-deploy-guide/dependencies/).

#### Dependent Components

- [LeapfrogAI API](../api/README.md) for a fully RESTful application

### Model Selection

The default model that comes with this backend in this repository's officially released images is a [4-bit quantization of the Hermes-2-Pro-Mistral-7B model](https://huggingface.co/defenseunicorns/Hermes-2-Pro-Mistral-7B-4bit-32g).

You can optionally specify different models or quantization types using the following Docker build arguments:

- `--build-arg MAX_CONTEXT_LENGTH="32768"`: Max context length, cannot exceed model's max length - the greater length the greater the vRAM requirements
- `--build-arg TENSOR_PARALLEL_SIZE="1"`: The number of gpus to spread the tensor processing across
- `--build-arg TRUST_REMOTE_CODE="True"`: Whether to trust inferencing code downloaded as part of the model download
- `--build-arg ENGINE_USE_RAY="False"`: Distributed, multi-node inferencing mode for the engine
- `--build-arg WORKER_USE_RAY="False"`: Distributed, multi-node inferencing mode for the worker(s)
- `--build-arg GPU_MEMORY_UTILIZATION="0.90"`: Max memory utilization (fraction, out of 1.0) for the vLLM process
- `--build-arg ENFORCE_EAGER="False"`: Disable CUDA graphs for faster token first-inferencing at the cost of more GPU memory (set to False for production)

## Prompt Formats

The pre-packaged model, defenseunicorns/Hermes-2-Pro-Mistral-7B-4bit-32g, contains special prompt templates for activating the function calling and JSON response modes. The default prompt template is the ChatML format.

These are a result of its training data and process. Please refer to [this section of the Hugging Face model card](https://huggingface.co/defenseunicorns/Hermes-2-Pro-Mistral-7B-4bit-32g#prompt-format-for-function-calling) for more details.

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
python src/model_download.py

# Start the model backend
make dev
```
