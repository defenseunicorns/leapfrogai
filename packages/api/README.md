# LeapfrogAI Python API

A Python API that exposes LLM backends, via FastAPI and gRPC, in the [OpenAI API specification](https://platform.openai.com/docs/api-reference).

## Usage

See [instructions](#instructions) to get the backend up and running.

### Instructions

The instructions in this section assume the following:

1. Properly installed and configured Python 3.11.x, to include its development tools

### Zarf Package Deployment

To build and deploy just the llama-cpp-python Zarf package (from the root of the repository):

> Deploy a [UDS cluster](/README.md#uds) if one isn't deployed already

```bash
make build-api LOCAL_VERSION=dev
uds zarf package deploy packages/api/zarf-package-leapfrogai-api-*-dev.tar.zst --confirm
```

### Local Development

To run the API locally (starting from the root directory of the repository):

From this directory:

```bash
# Setup Virtual Environment
python -m venv .venv
source .venv/bin/activate
```

```bash
# Install dependencies
python -m pip install src/leapfrogai_sdk
cd packages/api
python -m pip install ".[dev]"
```

```bash
# Run the API application
cd packages/api && make dev
```
