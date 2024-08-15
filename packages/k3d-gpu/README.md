# K3D GPU

Prepares a `k3s` + `nvidia/cuda` base image that enables a K3D cluster to utilize your host machine's NVIDIA, CUDA-capable GPU(s).

This is for development and demonstration purposes, and should not be used to deploy LeapfrogAI in a production environment.

## Usage

### Pre-Requisites

All system requirements and pre-requisites from the [LeapfrogAI documentation website](https://docs.leapfrog.ai/docs/local-deploy-guide/quick_start/).

### Deployment

> [!NOTE]
> The following Make targets from the root of the LeapfrogAI repository or within this sub-directory.

To deploy a new K3d cluster with [UDS Core Slim Dev](https://github.com/defenseunicorns/uds-core#uds-package-development), use one of the following Make targets.

```bash
make create-uds-gpu-cluster # create a uds cluster equipped with the k3d-gpu image

make test-uds-gpu-cluster # deploy a test gpu pod to see if everything is working
```

### Local Development

> [!NOTE]
> The following Make targets can be executed from the root of the LeapfrogAI repository or within this sub-directory

To build **just** the K3s CUDA image for container debugging, use the following Make target.

```bash
make build-k3d-gpu # build the image
```

## References

* https://k3d.io/v5.7.2/usage/advanced/cuda/
