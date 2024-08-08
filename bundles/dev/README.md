# LeapfrogAI UDS Dev Deployment Instructions

Follow these instructions to create a local development deployment of LeapfrogAI using [UDS](https://github.com/defenseunicorns/uds-core).

Make sure your system has the [required dependencies](https://docs.leapfrog.ai/docs/local-deploy-guide/quick_start/#prerequisites).

For ease, it's best to create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

## Linux and Windows (via WSL2)

Each component is built into its own Zarf package. You can build all of the packages you need at once with the following `Make` targets:

> [!NOTE]
> You need to build with `make build-* LOCAL_VERSION=dev` to set the tag to `dev` instead of the commit hash locally.

> [!NOTE]
> Some of the packages have Python dev dependencies that need to be installed when building them locally. These dependencies are used to download the model weights that will be included in the final Zarf package. These dependencies are listed as `dev` in the `project.optional-dependencies` section of each models `pyproject.toml`.

You can build all of the packages you need at once with the following `Make` targets:

```bash
LOCAL_VERSION=dev make build-cpu    # api, llama-cpp-python, text-embeddings, whisper, supabase
LOCAL_VERSION=dev make build-gpu    # api, vllm, text-embeddings, whisper, supabase
LOCAL_VERSION=dev make build-all    # all of the backends
```

**OR**

You can build components individually using the following `Make` targets:

```bash
LOCAL_VERSION=dev make build-api
LOCAL_VERSION=dev make build-supabase
LOCAL_VERSION=dev make build-vllm                 # if you have GPUs (macOS not supported)
LOCAL_VERSION=dev make build-llama-cpp-python     # if you have CPU only
LOCAL_VERSION=dev make build-text-embeddings
LOCAL_VERSION=dev make build-whisper
```

**NOTE: If you do not prepend your commands with `LOCAL_VERSION=dev`, uds will not find the generated zarf packages, as
they will be tagged with your current git hash instead of `dev` which uds expects**

## MacOS

To run the same commands in macOS, you will need to prepend your command with a couple of env vars like so:

All Macs: `REG_PORT=5001`

Apple Silicon (M1/M2/M3/M4 series) Macs: `ARCH=arm64`

To demonstrate what this would look like for an Apple Silicon Mac:

``` shell
REG_PORT=5001 ARCH=arm64 LOCAL_VERSION=dev make build-cpu
```

To demonstrate what this would look like for an older Intel Mac (not officially supported):

``` shell
REG_PORT=5001 LOCAL_VERSION=dev make build-cpu
```

**OR**

You can build components individually using the following `Make` targets, just like in the Linux section except ensuring
to prepend the env vars detailed above.

> [!NOTE]
> Once the packages are created, you can deploy either a CPU or GPU-enabled deployment via one of the UDS bundles (macOS only supports cpu)

## Deploying via UDS bundle

### CPU UDS Deployment

Create the uds CPU bundle:

```bash
cd uds-bundles/dev/cpu
uds create .
```

Deploy a [UDS cluster](/README.md#uds) if one isn't deployed already

Deploy the LeapfrogAI bundle:

```bash
uds deploy uds-bundle-leapfrogai*.tar.zst
```

### GPU UDS Deployment

Create the uds GPU bundle:

```bash
cd uds-bundles/dev/gpu
uds create .
```

Deploy a [UDS cluster](/README.md#uds) with the following flags, as so:

```bash
uds deploy {k3d-cluster-name} --set K3D_EXTRA_ARGS="--gpus=all --image=ghcr.io/justinthelaw/k3d-gpu-support:v1.27.4-k3s1-cuda"
```

Deploy the LeapfrogAI bundle:

```bash
uds deploy uds-bundle-leapfrogai-*.tar.zst --confirm
```

Once running you can access the various components, if deployed and exposed, at the following URLS:

```bash
https://ai.uds.dev              # UI
https://leapfrogai-api.uds.dev  # API
https://supabase-kong.uds.dev   # Supabase Kong
https://keycloak.uds.dev        # Keycloak
```

## Checking and Managing the Deployment

For tips on how to monitor the deployment, accessing the UI, and clean up, please reference the [Quick Start](https://docs.leapfrog.ai/docs/local-deploy-guide/quick_start/#checking-deployment) guide in the LeapfrogAI docs.
