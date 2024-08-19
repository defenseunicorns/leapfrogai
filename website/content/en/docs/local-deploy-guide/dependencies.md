---
title: Dependencies
type: docs
weight: 2
---

This documentation addresses the local deployment dependencies of LeapfrogAI, a self-hosted generative AI platform. LeapfrogAI extends the diverse capabilities and modalities of AI models to various environments, ranging from cloud-based deployments to servers with ingress and egress limitations. With LeapfrogAI, teams can deploy APIs aligned with OpenAI's API specifications, empowering teams to create and utilize tools compatible with nearly any model and code library available. Importantly, all operations take place locally, ensuring users can maintain the security of their information and sensitive data within their own environments

Follow the outlined steps to ensure that your device is configured to execute LeapfrogAI workloads across local development scenarios. Please note that these instructions presume you have root access.

### Host Dependencies

Ensure that the following tools and packages are installed in your environment according to the instructions below:

- [Git](https://git-scm.com/)
- [Docker](https://docs.docker.com/engine/install/)
- [K3D](https://k3d.io/)
- [UDS CLI](https://github.com/defenseunicorns/uds-cli)

### Install Git

- Download [Git](https://git-scm.com/downloads) and follow the instructions on the [Git documentation website](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

### Install Docker

- Follow the [instructions](https://docs.docker.com/engine/install/) to install Docker onto your system.
- Systems using an NVIDIA GPU must also follow the [GPU instructions below](#gpu-specific-instructions)

### Install Kubectl

- Follow the [instructions](https://kubernetes.io/docs/tasks/tools/#kubectl) to install kubectl onto your system.

### Install K3d

- Follow the [instructions](https://k3d.io/) to install k3d onto your system.

### Install UDS CLI

- Follow the [instructions](https://github.com/defenseunicorns/uds-cli#install) to install UDS CLI onto your system.

- As Homebrew does not install packages to the root directory, it is advisable to manually add the `uds` binary to the root
- In cases where Docker is installed in a rootless configuration, certain systems may encounter container access issues if Docker is not executed with root privileges
- To install `uds` as root, execute the following command in your terminal and ensure that the version number is replaced with the most recent [release](https://github.com/defenseunicorns/uds-cli/releases):

```bash
# where $UDS_VERSION is the latest UDS CLI release
wget -O uds https://github.com/defenseunicorns/uds-cli/releases/download/$UDS_VERSION/uds-cli_$UDS_VERSION_Linux_amd64 && \
  sudo chmod +x uds && \
  sudo mv uds /usr/local/bin/
```

## GPU Specific Instructions

LeapfrogAI exclusively supports NVIDIA GPUs at this point in time. The following instructions are tailored for users utilizing an NVIDIA GPU.

If you are experiencing issues even after carefully following the instructions below, please refer to the [Developer Documentation](https://github.com/defenseunicorns/leapfrogai/tree/main/docs/DEVELOPMENT.md) troubleshooting section in the GitHub repository.

### NVIDIA Drivers

- Ensure that the proper [NVIDIA drivers](https://www.nvidia.com/download/index.aspx) are installed (>=525.60).
- Follow the [driver download](https://www.nvidia.com/download/index.aspx) by identifying your hardware from the provided list.

### CUDA Toolkit

- Follow the [instructions](https://developer.nvidia.com/cuda-downloads) to download the CUDA toolkit (>=12.2x). This toolkit is only required on the system that is building the Zarf Packages.

### NVIDIA Container Toolkit

- Read the pre-requisites for installation and follow the [instructions](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html#installing-with-apt) to download and install the NVIDIA container toolkit (>=1.14).
- After the successful installation off the toolkit, follow the [toolkit instructions](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html#configuring-docker) to verify that your default Docker runtime is configured for NVIDIA:

  ```bash
  nvidia-ctk runtime configure --runtime=docker --config=$HOME/.config/docker/daemon.json
  ```

- Verify that `nvidia` is now a runtime available to the Docker daemon to use:

  ```bash
  # the expected output should be similar to: `Runtimes: io.containerd.runc.v2 nvidia runc`
  docker info | grep -i nvidia
  ```

- [Try out a sample CUDA workload](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/sample-workload.html) to ensure your Docker containers have access to the GPUs after configuration.
- (OPTIONAL) You can configure Docker to use the `nvidia` runtime by default by adding the `--set-as-default` flag during the container toolkit post-installation configuration step by running the following command:

  ```bash
  nvidia-ctk runtime configure --runtime=docker --config=$HOME/.config/docker/daemon.json --set-as-default
  ```

- (OPTIONAL) Verify that the default runtime is changed by running the following command:

  ```bash
  # the expected output should be similar to: `Default Runtime: nvidia`
  docker info | grep "Default Runtime"
  ```

### Deploy LeapfrogAI

- After ensuring that all system dependencies and requirements are fulfilled, refer to the Quick Start guide for comprehensive instructions on deploying LeapfrogAI within your local environment.
