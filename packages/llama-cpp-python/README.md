# LeapfrogAI LLaMA C++ Python Backend

A LeapfrogAI API-compatible [llama-cpp-python](https://github.com/abetlen/llama-cpp-python) wrapper for quantized and un-quantized model inferencing across CPU infrastructures.

## Usage

### Pre-Requisites

See the LeapfrogAI documentation website for [system requirements](https://docs.leapfrog.ai/docs/local-deploy-guide/requirements/) and [dependencies](https://docs.leapfrog.ai/docs/local-deploy-guide/dependencies/).

#### Dependent Components

- [LeapfrogAI API](../api/README.md) for a fully RESTful application

### Model Selection

The default model that comes with this backend in this repository's officially released images is a [quantization of the Synthia-7b model](https://huggingface.co/TheBloke/SynthIA-7B-v2.0-GPTQ).

Models are pulled from [HuggingFace Hub](https://huggingface.co/models) via the [model_download.py](/packages/llama-cpp-python/scripts/model_download.py) script. To change what model comes with the llama-cpp-python backend, set the following environment variables:

```bash
REPO_ID   # eg: "TheBloke/SynthIA-7B-v2.0-GGUF"
FILENAME  # eg: "synthia-7b-v2.0.Q4_K_M.gguf"
REVISION  # eg: "3f65d882253d1f15a113dabf473a7c02a004d2b5"
```

If you choose a different model, make sure to modify the default [config.yaml](./config.yaml) using the Hugging Face model repository's model files and model card.

### Deployment

To build and deploy the llama-cpp-python backend Zarf package into an existing [UDS Kubernetes cluster](../k3d-gpu/README.md):

> [!IMPORTANT]
> Execute the following commands from the root of the LeapfrogAI repository

```bash
pip install 'huggingface_hub[cli,hf_transfer]'  # Used to download the model weights from huggingface
make build-llama-cpp-python LOCAL_VERSION=dev
uds zarf package deploy packages/llama-cpp-python/zarf-package-llama-cpp-python-*-dev.tar.zst --confirm
```

### Local Development

To run the llama-cpp-python backend locally:

> [!IMPORTANT]
> Execute the following commands from this sub-directory

```bash
# Install dev and runtime dependencies
make install

# Clone Model
# Supply a REPO_ID, FILENAME and REVISION, as seen in the "Model Selection" section
python scripts/model_download.py
mv .model/*.gguf .model/model.gguf

# Start the model backend
make dev
```
