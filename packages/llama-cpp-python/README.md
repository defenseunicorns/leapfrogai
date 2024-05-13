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

### Run Locally

From this directory:
```bash
# Setup Virtual Environment
python -m venv .venv
source .venv/bin/activate

python -m pip install ../../src/leapfrogai_sdk
python -m pip install .
```

```bash
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
python scripts/model_download.py

mv .model/*.gguf .model/model.gguf

# Start Model Backend
python -u main.py
```
