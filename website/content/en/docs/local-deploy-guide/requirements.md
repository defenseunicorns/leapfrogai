---
title: Requirements
type: docs
weight: 4
---

Prior to deploying LeapfrogAI, ensure that the following tools, packages, and requirements are met and present in your environment. See the [Dependencies](https://docs.leapfrog.ai/docs/local-deploy-guide/dependencies/) page fro more details.

## System Requirements

Please review the following table to ensure your system meets the minimum requirements. GPU requirements only apply when your system is capable of deploying a GPU-accelerated version of the LeapfrogAI stack.

|      | Minimum            | Recommended (Performance) |
|------|--------------------|---------------------------|
| DISK | 256 GB             | 1 TB                      |
| RAM  | 32 GB              | 128 GB                    |
| CPU  | 8 Cores @ 3.0 GHz  | 32 Cores @ 3.0 GHz        |
| GPU  | N/A                | 2x NVIDIA RTX 4090 GPUs   |

## Tested Environments

The following operating systems, hardware, architectures, and system specifications have been tested and validated for our deployment instructions:

### Operating Systems

- Ubuntu LTS
  - 22.04.2
  - 22.04.3
  - 22.04.4
  - 22.04.5
- Ubuntu
  - 20.04.6
- Pop!_OS LTS
  - 22.04.x
- MacOS Sonoma / ARM64 (CPU-only)
  - 14.x

### Hardware

- 64 CPU cores (`Unknown Compute via Virtual Machine`) and ~250 GB RAM, no GPU.
- 32 CPU cores (`AMD Ryzen Threadripper PRO 5955WX`) and ~250 GB RAM, 2x `NVIDIA RTX A4000` (16Gb vRAM each).
- 64 CPU cores (`Intel Xeon Platinum 8358 CPU`) and ~200Gb RAM, 1x `NVIDIA RTX A10` (16Gb vRAM each).
- 10 CPU cores (`Apple M1 Pro`) and ~32 GB of free RAM, 1x `Apple M1 Pro`.
- 32 CPU cores (`13th Gen Intel Core i9-13900KF`) and ~190GB RAM, 1x `NVIDIA RTX 4090` (24Gb vRAM each).
- 2x 128 CPU cores (`AMD EPYC 9004`) and ~1.4Tb RAM, 8x `NVIDIA H100` (80Gb vRAM each).
- 32 CPU cores (`13th Gen Intel Core i9-13900HX`) and ~64Gb RAM, 1x `NVIDIA RTX 4070` (8Gb vRAM each).

### Architectures

- Linux/AMD64
- Linux/ARM64
