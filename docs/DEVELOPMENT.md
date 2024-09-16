# Development

> [!IMPORTANT]
> Please read the entirety of the root [README.md](../README.md) and the [LeapfrogAI documentation website](https://docs.leapfrog.ai/docs/local-deploy-guide/quick_start/) prior to reading this document. Also, please refer to the [CONTRIBUTING.md](../.github/CONTRIBUTING.md) for rules on contributing to the LeapfrogAI project.

The purpose of this document is to describe how to run a development loop on the LeapfrogAI tech stack. Specifics for each component are within the sub-directories identified in the root [README.md](../README.md).

## Local Development

Please first see the pre-requisites listed on the LeapfrogAI documentation website's [Requirements](https://docs.leapfrog.ai/docs/local-deploy-guide/requirements/) and [Dependencies](https://docs.leapfrog.ai/docs/local-deploy-guide/dependencies/), before going to each component's subdirectory README

## PyEnv

It is **_HIGHLY RECOMMENDED_** that PyEnv be installed on your machine, and a new virtual environment is created for every new development branch.

Follow the installation instructions outlined in the [pyenv](https://github.com/pyenv/pyenv?tab=readme-ov-file#installation) repository to install Python 3.11.9:

  ```bash
  # install the correct python version
  pyenv install 3.11.9

  # create a new virtual environment named "leapfrogai"
  pyenv virtualenv 3.11.9 leapfrogai

  # activate the virtual environment
  pyenv activate leapfrogai
  ```

If your installation process completes successfully but indicates missing packages such as `sqlite3`, execute the following command to install the required packages then proceed with the reinstallation of Python 3.11.9:

  ```bash
  sudo apt-get install build-essential zlib1g-dev libffi-dev \
    libssl-dev libbz2-dev libreadline-dev libsqlite3-dev \
    liblzma-dev libncurses-dev
  ```

## UDS CLI Aliasing

Below are instructions for adding UDS CLI aliases that are useful for deployments that occur in an air-gap where the UDS CLI binary is available to the engineer.

For general CLI UX, put the following in your shell configuration (e.g., `/root/.bashrc`, `~/.zshrc`):

```bash
alias k="uds zarf tools kubectl"
alias kubectl="uds zarf tools kubectl"
alias zarf='uds zarf'
alias k9s='uds zarf tools monitor'
alias udsclean="uds zarf tools clear-cache && rm -rf ~/.uds-cache && rm -rf /tmp/zarf-*"
```

For fulfilling `kubectl` binary requirements necessary for running some of the _optional_ deployment helper scripts and for full functionality within `uds zarf tools monitor`:

```bash
touch /usr/local/bin/kubectl
echo -e '#!/bin/bash\nuds zarf tools kubectl "$@"' > /usr/local/bin/kubectl
chmod +x /usr/local/bin/kubectl
```

## Makefiles

Many of the directories and sub-directories within this project contain Make targets that can be executed to simplify repetitive command-line tasks.

Please refer to each Makefile for more arguments and details on what each target does and is dependent on.

## Environment Variables

Be wary of `*config*.yaml` or `.env*` files that are in individual components of the stack. The component's README will usually tell the developer when to fill them out or supply environment variables to a script.

For example, the LeapfrogAI API requires a `config.yaml` be supplied when spun up locally. Use the `config.example.yaml` as an example, and make sure the [ports chosen for applicable backends do not conflict on localhost](#port-conflicts).

## Package Development

If you don't want to [build an entire bundle](#bundle-development), or you want to "dev-loop" on a single package in an existing [UDS Kubernetes cluster](../packages/k3d-gpu/README.md) you can do so by following the instructions below.

For example, this is how you build and (re)deploy a local DEV version of a package:

```bash
# if package is already in the cluster, and you are deploying a new one
uds zarf package remove leapfrogai-api --confirm
uds zarf tools registry prune --confirm

# create and deploy the new package
# FLAVOR can be upstream (default) or registry1 - see README for availability details
LOCAL_VERSION=dev FLAVOR=upstream REGISTRY_PORT=5000 ARCH=amd64 make build-api
LOCAL_VERSION=dev FLAVOR=upstream REGISTRY_PORT=5000 ARCH=amd64 make deploy-api
```

For example, this is how you pull and deploy a LATEST version of a package:

```bash
# pull and deploy latest versions
uds zarf package pull oci://ghcr.io/defenseunicorns/leapfrogai/leapfrogai-api:latest -a amd64
uds zarf package deploy zarf-package-*.tar.zst --confirm
```

## Bundle Development

1. Install all the necessary package creation dependencies:

    ```bash
    python -m pip install ".[dev]"
    python -m pip install ".[dev-whisper]"
    python -m pip install ".[dev-vllm]"
    ```

2. Build all of the packages you need at once with **ONE** of the following Make targets:

    ```bash
    # FLAVOR can be upstream (default) or registry1 - see README for availability details
    LOCAL_VERSION=dev FLAVOR=upstream ARCH=amd64 make build-cpu    # ui, api, llama-cpp-python, text-embeddings, whisper, supabase
    # OR
    LOCAL_VERSION=dev FLAVOR=upstream ARCH=amd64 make build-gpu    # ui, api, vllm, text-embeddings, whisper, supabase
    # OR
    LOCAL_VERSION=dev FLAVOR=upstream ARCH=amd64 make build-all    # all of the components
    ```

    **OR**

    You can build components individually using the following Make targets:

    ```bash
    # FLAVOR can be upstream (default) or registry1 - see README for availability details
    LOCAL_VERSION=dev FLAVOR=upstream ARCH=amd64 make build-ui
    LOCAL_VERSION=dev FLAVOR=upstream ARCH=amd64 make build-api
    LOCAL_VERSION=dev FLAVOR=upstream ARCH=amd64 make build-supabase
    LOCAL_VERSION=dev FLAVOR=upstream ARCH=amd64 make build-vllm                 # if you have NVIDIA GPUs (AMR64 not supported)
    LOCAL_VERSION=dev FLAVOR=upstream ARCH=amd64 make build-llama-cpp-python     # if you have CPU only
    LOCAL_VERSION=dev FLAVOR=upstream ARCH=amd64 make build-text-embeddings
    LOCAL_VERSION=dev FLAVOR=upstream ARCH=amd64 make build-whisper
    ```

3. Create the UDS bundle, modifying the `uds-config.yaml` as required:

  ```bash
  cd bundles/dev/<cpu or gpu>
  uds create . --confirm
  ```

4. Deploy the UDS bundle to an existing [UDS Kubernetes cluster](../packages/k3d-gpu/README.md):

  ```bash
  cd bundles/dev/<cpu or gpu>
  uds deploy <insert bundle name> --confirm
  ```

### Bundle Overrides

Although not provided in the example UDS bundle manifests found in this repository's `bundles/`, the `uds-bundle.yaml` and `uds-config.yaml` can be modified to override values files of a component's deployment. For example, when using UDS CLI to deploy the `bundles/latest/gpu/uds-bundle.yaml` you can add the following lines to the following files to influence a value that is not accessible by any other means (e.g., setting a  Zarf variable):

#### _uds-bundle.yaml_

```yaml
  # OpenAI-like API
  - name: leapfrogai-api
    repository: ghcr.io/defenseunicorns/packages/leapfrogai/leapfrogai-api
    # x-release-please-start-version
    ref: 0.12.2
    # x-release-please-end

    # THE BELOW LINES WERE ADDED FOR DEMONSTRATION PURPOSES
    overrides:
      leapfrogai-api:
        leapfrogai:
          variables:
            name: API_REPLICAS
            description: "Default number of API replicas to deploy"
            path: api.replicas # the path to the value you want to override in packages/api/chart/values.yaml
```

#### _uds-config.yaml_

```yaml
variables:
  # THE BELOW LINES WERE ADDED FOR DEMONSTRATION PURPOSES
  leapfrogai-api:
    api_replicas: 2 # overriding the default value of 1 in the packages/api/chart/values.yaml
```

### MacOS Specifics

To run the same commands in MacOS, you will need to prepend your command with a couple of env vars like so:

**All Macs:** `REG_PORT=5001`

**Apple Silicon (M1/M2/M3/M4 series) Macs:** `ARCH=arm64`

To demonstrate what this would look like for an Apple Silicon Mac:

```bash
# FLAVOR can be upstream (default) or registry1 - see README for availability details
REG_PORT=5001 ARCH=arm64 LOCAL_VERSION=dev FLAVOR=upstream make build-cpu
```

To demonstrate what this would look like for an older Intel Mac:

```bash
# FLAVOR can be upstream (default) or registry1 - see README for availability details
REG_PORT=5001 ARCH=arm64 LOCAL_VERSION=dev FLAVOR=upstream make build-cpu
```

## Access

All LeapfrogAI components exposed as `VirtualService`resources within a [UDS Kubernetes cluster](../packages/k3d-gpu/README.md) can be accessed without port-forwarding if [UDS Core Slim Dev](../packages/k3d-gpu/README.md) is installed with LeapfrogAI packages.

For example, when developing the API and you need access to Supabase, you can point your locally running API to the in-cluster Supabase by setting the Supabase base URL to the in-cluster domain (https://supabase-kong.uds.dev).

The preferred method of testing changes is to fully deploy something to a cluster and run local smoke tests as needed. The GitHub workflows will run all integration and E2E test suites.

### Supabase

Supabase is a special case when spun up inside of a UDS Kubernetes cluster. All of the bitnami Supabase components are served through the Kong service mesh, which is exposed as https://supabase-kong.uds.dev through our Istio tenant gateway. All of the Make commands, and our UI and API, correctly route to the right endpoint for interacting with each sub-component of Supabase. The UI and API use the `supabase` Typescript or Python package to interact with Supabase without issue.

Although not recommended, below are example endpoints for direct interaction with Supabase sub-components is as follows:

- https://supabase-kong.uds.dev/auth/v1/* -> to access auth endpoints
- https://supabase-kong.uds.dev/rest/v1/ -> for postgres

We highly recommend using the published `supabase` packages, or interacting with Supabase via the LeapfrogAI API or UI. Go to https://leapfrogai-api.uds.dev/docs to see the exposed Supabase sub-component routes under the `leapfrogai` namespace / routes.

### Backends

The following sections discuss the nuances of developing on or with the LeapfrogAI model backends.

#### Locally

Backends can also be run locally as Python applications. See each model backend's README in the `packages/` directory for more details on running each in development mode.

#### Cluster

The model backends are the only components within the LeapfrogAI stack that are not readily accessible via a `VirtualService`. These must be port-forwarded if a user wants to test a local deployment of the API against an in-cluster backend.

For example, the following bash script can be used to setup CPU RAG between a deployed UDS Kubernetes cluster and a locally running LeapfrogAI API:

```bash
#!/bin/bash

# Function to kill all background processes when the script exits or is interrupted
cleanup() {
    echo "Cleaning up..."
    kill $PID1 $PID2
}

# Set environment variables
export SUPABASE_URL="https://supabase-kong.uds.dev"
export SUPABASE_ANON_KEY=$(kubectl get secret supabase-bootstrap-jwt -n leapfrogai -o jsonpath='{.data.anon-key}' | base64 --decode)

# Trap SIGINT (Ctrl-C) and SIGTERM (termination signal) to call the cleanup function
trap cleanup SIGINT SIGTERM

# Start Kubectl port-forward services in the background and save their PIDs
# Expose the backends at different ports to prevent localhost conflict
# Make sure to change the config.yaml in the api source directory
uds zarf tools kubectl port-forward svc/text-embeddings-model -n leapfrogai 50052:50051 &
PID1=$!
uds zarf tools kubectl port-forward svc/llama-cpp-python-model -n leapfrogai 50051:50051 &
PID2=$!

# Wait for all background processes to finish
wait $PID1 $PID2
```

#### Port Conflicts

In all cases, port conflicts may arise when outside of a cluster service mesh. As seen in the [Cluster sub-section](#cluster), backends all try to emit at port `50051`; however, on a host machine's localhost, there can only be one on 50051. Using the [Leapfrogai API](../src/leapfrogai_api/config.example.yaml), define the ports at which you plan on making a backend accessible.

## Troubleshooting

Occasionally, a package you are trying to re-deploy, or a namespace you are trying to delete, may hang. To workaround this, be sure to check the events and logs of all resources, to include pods, deployments, daemonsets, clusterpolicies, etc. There may be finalizers, Pepr hooks, and etc. causing the re-deployment or deletion to fail. Use the [`k9s`](https://k9scli.io/topics/commands/) and `kubectl` tools that are vendored with UDS CLI, like in the examples below:

### Clusters

```bash
# k9s CLI for debugging
uds zarf tools monitor

# kubectl command for logs
uds zarf tools kubectl logs -l app=api -n leapfrogai --all-containers=true --follow
```

To describe node-level data, like resource usage, non-terminated pods, taints, etc. run the following command:

```bash
uds zarf tools kubectl describe node
```

### NVIDIA GPUs

#### NVML Errors or Missing CUDA Dependencies

None of the following should ever error or return `unknown version`:

1. Check if your NVIDIA GPU drivers are installed:

    ```bash
    nvidia-smi
    ```

2. Check the version of your NVIDIA Container Toolkit:

    ```bash
    nvidia-ctk --version
    ```

3. Check the version of your CUDA Toolkit (if compiling vLLM locally):

    ```bash
    nvcc --version
    ```

Try looking at your Docker runtime information and make sure the following returns with several lines of information:

```bash
docker info | grep "nvidia"
```

Try running the CUDA sample tests in the cluster: [CUDA Vector Add](../packages/k3d-gpu/test/cuda-vector-add.yaml). This can be deployed by executing the following on an existing cluster with NVIDIA GPU operator and/or NVIDIA device plugin daemonset installed:

```bash
uds zarf tools kubectl apply packages/k3d-gpu/test/cuda-vector-add.yaml
```

#### Memory Errors or Process Locks

If you are,

1. not deploying a fresh cluster or fresh packages (e.g., vLLM is already deployed), or
2. you have a GPU that has other workloads on it (e.g., display)

then there may not be enough resources to offload the model weights to the NVIDIA GPU.

To see what host-level processes are on your NVIDIA GPU(s) run the following:

```bash
nvidia-smi
```

To check which pods are sucking up GPUs in particular, you can run the following `yq` command:

```bash
uds zarf tools kubectl get pods \
--all-namespaces \
--output=yaml \
| uds zarf tools yq eval -o=json '
  ["Pod", "Namespace", "Container", "GPU"] as $header |
  [$header] + [
    .items[] |
    .metadata as $metadata |
    .spec.containers[] |
    select(.resources.requests["nvidia.com/gpu"]) |
    [
      $metadata.name,
      $metadata.namespace,
      .name,
      .resources.requests["nvidia.com/gpu"]
    ]
  ]' - \
| uds zarf tools yq -r '(.[0] | @tsv), (.[1:][] | @tsv)' \
| column -t -s $'\t'
```

When you reinstall or start a new GPU-dependent pod, the previous PID (process) on the GPU may not have been flushed yet.

1. Scale the previous GPU-dependent pod deployment down to 0, as the current `RollingUpdate` strategy for vLLM relies on back-up/secondary GPUs to be available for a graceful turnover
2. Use `nvidia-smi` to check if the process has been flushed upon Pod termination BEFORE you deploy a new GPU-dependent pod, and if not, use `kill -9 <PID>` to manually flush the process
