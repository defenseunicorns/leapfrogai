# LeapfrogAI llama-cpp-python Backend

A LeapfrogAI API-compatible [llama-cpp-python](https://github.com/abetlen/llama-cpp-python) w wrapper for quantized and un-quantized model inferencing across CPU infrastructures.



See [instructions](#instructions) to get the backend up and running. Then, use the [LeapfrogAI API server](https://github.com/defenseunicorns/leapfrogai-api) to interact with the backend.

## Instructions

The instructions in this section assume the following:

1. Properly installed and configured Python 3.11.x, to include its development tools
2. The LeapfrogAI API server is deployed and running

The following are additional assumptions for GPU inferencing:

3. You have properly installed one or more NVIDIA GPUs and GPU drivers
4. You have properly installed and configured the [cuda-toolkit](https://developer.nvidia.com/cuda-toolkit) and [nvidia-container-toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/index.html)

### Model Selection

The default model that comes with this backend in this repository's officially released images is a [4-bit quantization of the Synthia-7b model](https://huggingface.co/TheBloke/SynthIA-7B-v2.0-GPTQ).

Models are pulled from [HuggingFace Hub](https://huggingface.co/models) via the [model_download.py](/packages/llama-cpp-python/scripts/model_download.py) script. To change what model comes with the llama-cpp-python backend, set the following environment variables:

```bash
REPO_ID   # eg: "TheBloke/SynthIA-7B-v2.0-GGUF"
FILENAME  # eg: "synthia-7b-v2.0.Q4_K_M.gguf"
REVISION  # eg: "3f65d882253d1f15a113dabf473a7c02a004d2b5"
```

## Zarf Package Deployment

To build and deploy just the llama-cpp-python Zarf package (from the root of the repository):

> Deploy a [UDS cluster](/README.md#uds) if one isn't deployed already

```shell
make build-llama-cpp-python LOCAL_VERSION=dev
uds zarf package deploy packages/llama-cpp-python/zarf-package-llama-cpp-python-*-dev.tar.zst --confirm
```

## Run Locally


To run the llama-cpp-python backend locally (starting from the root directory of the repository):

From this directory:
```bash
# Setup Virtual Environment
python -m venv .venv
source .venv/bin/activate
```

```bash
# Install dependencies
python -m pip install src/leapfrogai_sdk
cd packages/llama-cpp-python
python -m pip install ".[dev]"
```

```bash
# Clone Model
# Supply a REPO_ID, FILENAME and REVISION if a different model is desired
python scripts/model_download.py

mv .model/*.gguf .model/model.gguf

# Start Model Backend
lfai-cli --app-dir=. main:Model
```
