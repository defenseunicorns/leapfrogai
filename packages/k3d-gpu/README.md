# K3D GPU

Prepares `k3s` + `nvidia/cuda` base image that enables a K3D cluster to have access to your host machine's NVIDIA, CUDA-capable GPU(s).

## Pre-Requisites

* Docker: https://www.docker.com/
* K3D: https://k3d.io/
* UDS-CLI: https://github.com/defenseunicorns/uds-cli
* Modern NVIDIA GPU with CUDA cores and drivers must be present. Additionally, the CUDA toolkit and NVIDIA container toolkit must be installed.

## Usage

Check out the Make targets for the various options.

### Local

```shell
make build-k3d-gpu # build the image

make create-uds-gpu-cluster # create a uds cluster equipped with the k3d-gpu image

make test-uds-gpu-cluster # deploy a test gpu pod to see if everything is working
```

## References

* https://k3d.io/v5.7.2/usage/advanced/cuda/
