---
title: Requirements 
type: docs
weight: 3
---

Prior to deploying LeapfrogAI, ensure that the following tools, packages, and requirements are met and present in your environment.

## Tested Environments

The following operating systems, hardware, architectures, and system specifications have been tested and validated for our deployment instructions:

### Operating Systems

- Ubuntu LTS (jammy)
  - 22.04.2
  - 22.04.3
  - 22.04.4
  - 22.04.5
- Pop!_OS 22.04 LTS

### Hardware

- 64 CPU cores (`Unknown Compute via Virtual Machine`) and ~250 GB RAM, no GPU.
- 32 CPU cores (`AMD Ryzen Threadripper PRO 5955WX`) and ~250 GB RAM, 2x `NVIDIA RTX A4000` (16Gb vRAM each).
- 64 CPU cores (`Intel Xeon Platinum 8358 CPU`) and ~200Gb RAM, 1x `NVIDIA RTX A10` (16Gb vRAM each).
- 10 CPU cores (`Apple M1 Pro`) and ~32 GB of free RAM, 1x `Apple M1 Pro`.
- 32 CPU cores (`13th Gen Intel Core i9-13900KF`) and ~190GB RAM, 1x `NVIDIA RTX 4090` (24Gb vRAM each).
- 2x 128 CPU cores (`AMD EPYC 9004`) and ~1.4Tb RAM, 8x `NVIDIA H100` (80Gb vRAM each).
- 32 CPU cores (`13th Gen Intel Core i9-13900HX`) and ~64Gb RAM, 1x `NVIDIA RTX 4070` (8Gb vRAM each).

### Architecure

- Linux/AMD64
- Linux/ARM64

 Differentiated instructions will be provided for two scenarios: "Internet Access" and "Isolated Network":

- **Internet Access:**
  - Indicates a system capable of fetching and executing remote dependencies from the internet.
- **Isolated Network:**
  - Indicates a system that is isolated and lacks connectivity to external networks or remote repositories.
  - Note that "Isolated Network" instructions are also compatible with devices that have internet access.
  - For all "Isolated Network" installs, `wget`, `git` `clone` and `zarf package create` commands are assumed to have been completed prior to entering the isolated network.
  - For "Isolated Network" installs, ensure files and binaries from these commands are stored on a removable media device and subsequently uploaded to the isolated machine.
  - For specific tool versions, it is recommended to follow the "Isolated Network" instructions.
  
## System Requirements

- Standard Unix-based operating system installed.
  - Some commands may need to be modified depending on your CLI and package manager.
- Have root `sudo su` access.
  - Rootless mode details can be found in the [Docker documentation](https://docs.docker.com/engine/security/rootless/).

Additional considerations are necessary for GPU deployments:

- NVIDIA GPU must have the most up-to-date drivers installed.
- NVIDIA GPU drivers compatible with CUDA (>=12.2).
- NVIDIA Container Toolkit is available via internet access, pre-installed, or on a mirrored package repository in the air gap.

## GPU Deployments

- The speed and quality of LeapfrogAI, along with its hosted AI models, are significantly influenced by the availability of a robust GPU for offloading model layers.
- By default, each backend is configured to request 1x GPU device.
- Presently, these instructions do not support time-slicing or configuring multi-instance GPU setups.
- Over-scheduling GPU resources beyond their availability may result in the crash of backend pods.
- To prevent crashing, install backends as CPU-only if all available GPU devices are already allocated.
  
## Additional User Information

- All `cd` commands should be executed with respect to your project's working directory (PWD) within the development environment. Each new step should be considered as initiating from the root of that directory.
- For optimal organization, we recommend creating a new PWD named `/leapfrogai` in your home directory and consolidating all components there.
- In cases where a tagged version of a LeapfrogAI or Defense Unicorns release is not desired, the option to build an image from source prior to executing `zarf package create` is available:

``` bash
docker build -t "ghcr.io/defenseunicorns/leapfrogai/<NAME_OF_PACKAGE>:<DESIRED_TAG>" .
# find and replace any manifests referencing the image tag (e.g., zarf.yaml, zarf-config.yaml, etc.)
zarf package create zarf-package-<NAME_OF_PACKAGE>-*.tar.zst
```

- When building your Docker image from source, it is advisable to re-tag and push these images to a local registry container. This practice enhances the efficiency of zarf package creation. Below is an example of how to accomplish this using our whisper backend:

``` bash
docker run -d -p 5000:5000 --restart=always --name registry registry:2
docker build -t ghcr.io/defenseunicorns/leapfrogai/whisper:0.4.0 .
docker tag ghcr.io/defenseunicorns/leapfrogai/whisper:0.4.0 localhost:5000/defenseunicorns/leapfrogai/whisper:0.4.0
docker push localhost:5000/defenseunicorns/leapfrogai/whisper:0.4.0
zarf package create --registry-override ghcr.io=localhost:5000 --set IMG=defenseunicorns/leapfrogai/whisper:0.4.0
```
