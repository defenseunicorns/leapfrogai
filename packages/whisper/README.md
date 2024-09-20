# LeapfrogAI Whisper Backend

A LeapfrogAI API-compatible [faster-whisper](https://github.com/SYSTRAN/faster-whisper) wrapper for audio transcription inferencing across CPU & GPU infrastructures.

## Usage

### Pre-Requisites

See the LeapfrogAI documentation website for [system requirements](https://docs.leapfrog.ai/docs/local-deploy-guide/requirements/) and [dependencies](https://docs.leapfrog.ai/docs/local-deploy-guide/dependencies/).

#### Dependent Components

- [LeapfrogAI API](../api/README.md) for a fully RESTful application

### Model Selection

See the [Deployment section](#deployment) for the CTranslate2 command for pulling and converting a model for inferencing.

### Deployment

To build and deploy the whisper backend Zarf package into an existing [UDS Kubernetes cluster](../k3d-gpu/README.md):

> [!IMPORTANT]
> Execute the following commands from the root of the LeapfrogAI repository

```bash
pip install 'ctranslate2'          # Used to download and convert the model weights
pip install 'transformers[torch]'  # Used to download and convert the model weights
make build-whisper LOCAL_VERSION=dev
uds zarf package deploy packages/whisper/zarf-package-whisper-*-dev.tar.zst --confirm
```

### Local Development

To run the vllm backend locally without K8s (starting from the root directory of the repository):

```bash
# Install dev and runtime dependencies
make install

# Download and convert model
# Change the MODEL_NAME to change the whisper base
export MODEL_NAME=openai/whisper-base
make download-model

# Start the model backend
make dev
```
