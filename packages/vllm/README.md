# LeapfrogAI vLLM Backend

A LeapfrogAI API-compatible [vLLM](https://github.com/vllm-project/vllm) wrapper for quantized and un-quantized model inferencing across GPU infrastructures.

## Usage

See [instructions](#instructions) to get the backend up and running. Then, use the [LeapfrogAI API server](https://github.com/defenseunicorns/leapfrogai-api) to interact with the backend.

## Instructions

The instructions in this section assume the following:

1. Properly installed and configured Python 3.11.x, to include its development tools
2. The LeapfrogAI API server is deployed and running

The following are additional assumptions for GPU inferencing:

3. You have properly installed one or more NVIDIA GPUs and GPU drivers
4. You have properly installed and configured the [cuda-toolkit](https://developer.nvidia.com/cuda-toolkit) and [nvidia-container-toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/index.html)

### Model Selection

The default model that comes with this backend in this repository's officially released images is a [4-bit quantization of the Hermes-2-Pro-Mistral-7B model](defenseunicorns/Hermes-2-Pro-Mistral-7B-4bit-32g).

You can optionally specify different models or quantization types using the following Docker build arguments:

- `--build-arg MAX_CONTEXT_LENGTH="32768"`: Max context length, cannot exceed model's max length - the greater length the greater the vRAM requirements
- `--build-arg TENSOR_PARALLEL_SIZE="1"`: The number of gpus to spread the tensor processing across
- `--build-arg TRUST_REMOTE_CODE="True"`: Whether to trust inferencing code downloaded as part of the model download
- `--build-arg ENGINE_USE_RAY="False"`: Distributed, multi-node inferencing mode for the engine
- `--build-arg WORKER_USE_RAY="False"`: Distributed, multi-node inferencing mode for the worker(s)
- `--build-arg GPU_MEMORY_UTILIZATION="0.99"`: Max memory utilization (fraction, out of 1.0) for the vLLM process
- `--build-arg ENFORCE_EAGER="False"`: Disable CUDA graphs for faster token first-inferencing at the cost of more GPU memory (set to False for production)

## Prompt Formats

The pre-packaged model, defenseunicorns/Hermes-2-Pro-Mistral-7B-4bit-32g, contains special prompt templates for activating the function calling and JSON response modes. The default prompt template is the ChatML format.

These are a result of its training data and process. Please refer to [this section of the Hugging Face model card](https://huggingface.co/defenseunicorns/Hermes-2-Pro-Mistral-7B-4bit-32g#prompt-format-for-function-calling) for more details.

## Zarf Package Deployment

To build and deploy just the VLLM Zarf package (from the root of the repository):

> Deploy a [UDS cluster](/README.md#uds) if one isn't deployed already

```shell
pip install 'huggingface_hub[cli,hf_transfer]'  # Used to download the model weights from huggingface
make build-vllm LOCAL_VERSION=dev
uds zarf package deploy packages/vllm/zarf-package-vllm-*-dev.tar.zst --confirm
```

## Run Locally

To run the vllm backend locally (starting from the root directory of the repository):

```bash
# Setup Virtual Environment if you haven't done so already
python -m venv .venv
source .venv/bin/activate
```

```bash
# Install dependencies
python -m pip install src/leapfrogai_sdk
cd packages/vllm
# To support Huggingface Hub model downloads
python -m pip install ".[dev]"
```

```bash
# Copy the environment variable file, change this if different params are needed
cp .env.example .env

# Make sure environment variables are set
source .env

# Clone Model
# Supply a REPO_ID, FILENAME and REVISION if a different model is desired
python src/model_download.py

mv .model/*.gguf .model/model.gguf

# Start Model Backend
lfai-cli --app-dir=src/ main:Model
```
