# Development

> [!IMPORTANT]
> Please read the entirety of the root [README.md](../README.md) and the [LeapfrogAI documentation website](https://docs.leapfrog.ai/docs/local-deploy-guide/quick_start/) prior to reading this document. Also, please refer to the [CONTRIBUTING.md](../.github/CONTRIBUTING.md) for rules on contributing to the LeapfrogAI project.

The purpose of this document is to describe how to run a development loop on the LeapfrogAI tech stack. Specifics for each component are within the sub-directories identified in the root [README.md](../README.md).

## Local Development

Please first see the pre-requisites listed on the LeapfrogAI documentation website's [Requirements](https://docs.leapfrog.ai/docs/local-deploy-guide/requirements/) and [Dependencies](https://docs.leapfrog.ai/docs/local-deploy-guide/dependencies/), before going to each component's subdirectory README.

## UDS CLI Aliasing

Below are instructions for adding UDS CLI aliases that are useful for deployments that occur in an air-gap where only the UDS CLI binary available to the engineer.

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

## Makefile

Many of the directories and sub-directories within this project contain Make targets that can be executed to simplify repetitive command-line tasks.

Please refer to each Makefile for more arguments and details on what each target does and is dependent on.

## Package Development

If you don't want to build an entire bundle, or you want to dev-loop on a single package in an existing [UDS Kubernetes cluster](../packages/k3d-gpu/README.md) you can do so by performing the following.

For example, this is how you build and (re)deploy a local DEV version of a package:

```bash
# if package is already in the cluster, and you are deploying a new one
uds zarf package remove leapfrogai-api --confirm
uds zarf tools registry prune --confirm

# create and deploy the new package
LOCAL_VERSION=dev REGISTRY_PORT=5000 ARCH=amd64 make build-api
LOCAL_VERSION=dev REGISTRY_PORT=5000 ARCH=amd64 make deploy-api
```

For example, this is how you pull and deploy a LATEST version of a package:

```bash
# pull and deploy latest versions
uds zarf package pull oci://ghcr.io/defenseunicorns/leapfrogai/leapfrogai-api:latest -a amd64
uds zarf package deploy zarf-package-*.tar.zst --confirm
```

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
