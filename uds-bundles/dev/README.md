# LeapfrogAI UDS Dev Deployment Instructions

Follow these instructions to create a local development deployment of LeapfrogAI using [UDS](https://github.com/defenseunicorns/uds-core).

Make sure your system has the [required dependencies](https://docs.leapfrog.ai/docs/local-deploy-guide/quick_start/#prerequisites).

For ease, it's best to create a virtual environment:

```shell
python -m venv .venv
source .venv/bin/activate
```

Each component is built into its own Zarf package. You can build all of the packages you need at once with the following `Make` targets:

```shell
make build-cpu    # api, llama-cpp-python, text-embeddings, whisper, supabase
make build-gpu    # api, vllm, text-embeddings, whisper, supabase
make build-all    # all of the backends
```

**OR**

You can build components individually using the following `Make` targets:

```shell
make build-api
make build-supabase
make build-vllm                 # if you have GPUs
make build-llama-cpp-python     # if you have CPU only
make build-text-embeddings
make build-whisper
```

Once the packages are created, you can deploy either a CPU or GPU-enabled deployment via one of the UDS bundles:

## CPU

```shell
cd uds-bundles/dev/cpu
uds create .
uds deploy k3d-core-slim-dev:0.22.2
uds deploy uds-bundle-leapfrogai*.tar.zst
```

## GPU

```shell
cd uds-bundles/dev/gpu
uds create .
uds deploy k3d-core-slim-dev:0.22.2 --set K3D_EXTRA_ARGS="--gpus=all --image=ghcr.io/justinthelaw/k3d-gpu-support:v1.27.4-k3s1-cuda"     # be sure to check if a newer version exists
uds deploy uds-bundle-leapfrogai-*.tar.zst --confirm
```

## Checking and Managing the Deployment

For tips on how to monitor the deployment, accessing the UI, and clean up, please reference the [Quick Start](https://docs.leapfrog.ai/docs/local-deploy-guide/quick_start/#checking-deployment) guide in the LeapfrogAI docs.
