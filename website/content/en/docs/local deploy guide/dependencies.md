---
title: Dependencies 
type: docs
weight: 4
---

This documentation addresses the local deployment dependencies of LeapfrogAI, a self-hosted generative AI platform. LeapfrogAI extends the diverse capabilities and modalities of AI models to various environments, ranging from cloud-based deployments to servers with ingress and egress limitations. With LeapfrogAI, teams can deploy APIs aligned with OpenAI's API specifications, empowering teams to create and utilize tools compatible with nearly any model and code library available. Importantly, all operations take place locally, ensuring users can maintain the security of their information and sensitive data within their own environments

Follow the outlined steps to ensure that your device is configured to execute LeapfrogAI workloads across local development scenarios. Please note that these instructions presume you have root access.

### Host Dependencies

Ensure that the following tools and packages are present in your environment:

- [Jq](https://jqlang.github.io/jq/)
- [Docker](https://www.docker.com/get-started/)
- [build-essential](https://packages.ubuntu.com/focal/build-essential)
- [iptables](https://help.ubuntu.com/community/IptablesHowTo?action=show&redirect=Iptables)
- [Git](https://git-scm.com/)
- [procps](https://gitlab.com/procps-ng/procps)

### Install pyenv

- Follow the installation instructions outlined in the [pyenv](https://github.com/pyenv/pyenv?tab=readme-ov-file#installation) repository to install Python 3.11.6.
- If your installation process completes successfully but indicates missing packages such as `sqlite3`, execute the following command to install the required packages then proceed with the reinstallation of Python 3.11.6:

```git
sudo apt-get install build-essential zlib1g-dev libffi-dev
libssl-dev libbz2-dev libreadline-dev libsqlite3-dev
liblzma-dev libncurses-dev
```

### Install Homebrew

- Follow the [instructions](https://brew.sh/) to install the Homebrew package manager onto your system.

### Install Docker

- Follow the [instructions](https://docs.docker.com/engine/install/) to install Docker onto your system.
- For systems using an NVIDIA GPU, it is necessary to modify the Docker runtime to NVIDIA. Refer to the GPU instructions below for guidance on making this adjustment.

### Install Kubectl

- Follow the [instructions](https://kubernetes.io/docs/tasks/tools/#kubectl) to install kubectl onto your system.

### Install K3d

- Follow the [instructions](https://k3d.io/) to install k3d onto your system.

### Install Zarf

- Install [Zarf](https://zarf.dev/) using Homebrew:

```git
brew tap defenseunicorns/tap && brew install zarf
```

- As Homebrew does not install packages to the root directory, it is advisable to manually add the `zarf` binary to the root. Even in cases where Docker is installed in a rootless configuration, certain systems may encounter container access issues if Docker is not executed with root privileges.
- To install as root, execute the following command in your terminal and ensure that the version number is replaced with the most recent [release](https://github.com/defenseunicorns/zarf/releases):

```git
# switch to sudo
sudo su
# download and store on removable media
wget https://github.com/defenseunicorns/ uds-cli /releases/download/v0. 9.0/ uds-cli _v0. 9.0 _Linux_amd64
# upload from removable media and install
mv uds-cli_v0.9.0_Linux_amd64 /bin/uds
chmod +x /bin/uds
```

## GPU Specific Intructions

LeapfrogAI exclusively supports NVIDIA GPUs at this point in time. The following instructions are tailored for users utilizing an NVIDIA GPU.

### NVIDIA Drivers

- Ensure that the proper [NVIDIA drivers](https://www.nvidia.com/download/index.aspx) are installed (>=525.60).
- Follow the [driver download](https://www.nvidia.com/download/index.aspx) by identifying your hardware from the provided list.

### CUDA Toolkit

- Follow the [instructions](https://developer.nvidia.com/cuda-downloads) to download the CUDA toolkit (>=12.2x). This toolkit is only required on the system that is building the Zarf Packages.

### NVIDIA Container Toolkit

- Follow the [instructions](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html#installing-with-apt) to download the NVIDIA container toolkit (>=1.14).
- After the successful installation of the toolkit, follow the [toolkit instructions](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html#installing-with-apt) to verify that your default Docker runtime is configured for NVIDIA.
- Verify that the default runtime is changed by running the following command:

```git
docker info | grep "Default Runtime"
```

- The expected output should be similar to: `Default Runtime: nvidia`.

### GPU Support Test

- Test that your GPU is visible through Docker by deploying the [GPU Support Test](https://github.com/justinthelaw/gpu-support-test).

### Deploy LeapfrogAI

- After ensuring that all system dependencies and requirements are fulfilled, refer to the LeapfrogAI deployment guide for comprehensive instructions on deploying LeapfrogAI within your local environment.
