# LeapfrogAI Text Embeddings Backend

A LeapfrogAI API-compatible text embeddings wrapper for producing embeddings from text content.

## Usage

### Pre-Requisites

See the LeapfrogAI documentation website for [system requirements](https://docs.leapfrog.ai/docs/local-deploy-guide/requirements/) and [dependencies](https://docs.leapfrog.ai/docs/local-deploy-guide/dependencies/).

#### Dependent Components

- [LeapfrogAI API](../api/README.md) for a fully RESTful application
- [Supabase](../supabase/README.md) for a vector database to store resulting embeddings in

### Model Selection

The default model that comes with this backend in this repository's officially released images is [instructor-xl](https://huggingface.co/hkunlp/instructor-xl).

### Deployment

To build and deploy the text-embeddings backend Zarf package into an existing [UDS Kubernetes cluster](../k3d-gpu/README.md):

> [!IMPORTANT]
> Execute the following commands from the root of the LeapfrogAI repository

```bash
pip install 'huggingface_hub[cli,hf_transfer]'  # Used to download the model weights from huggingface
make build-text-embeddings LOCAL_VERSION=dev
uds zarf package deploy packages/text-embeddings/zarf-package-text-embeddings-*-dev.tar.zst --confirm
```

### Local Development

To run the text-embeddings backend locally:

> [!IMPORTANT]
> Execute the following commands from this sub-directory

```bash
# Setup Virtual Environment
python -m venv .venv
source .venv/bin/activate

# Clone Model
python scripts/model_download.py

# Install dependencies and start the model backend
make dev
```
