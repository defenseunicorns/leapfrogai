---
title: Deployment 
type: docs
weight: 5
---

To successfully proceed with the installation and deployment of LeapfrogAI, steps must be executed in the order that they are presented in the following instructions. The LeapfrogAI deployment instructions are designed to guide advanced users through the process of deploying the latest version of LeapfrogAI on Kubernetes.

## Switch to Sudo

```bash
# login as required
sudo su
```

## Deploy Tools

### Zarf

Internet Access:

```bash
# deploys latest version of Zarf
brew install zarf
```

Isolated Network:

```bash
# download and store on removable media
wget https://github.com/defenseunicorns/zarf/releases/download/v0.31.0/zarf_v0.31.0_Linux_amd64

# upload from removable media and install
mv zarf_v0.31.0_Linux_amd64 /usr/local/bin/zarf
chmod +x /usr/local/bin/zarf

# check
zarf version
```

### Kubectl

Internet Access:

```bash
apt install kubectl
```

Isolated Network:

```bash
# download and store on removable media
wget https://dl.k8s.io/release/v1.28.3/bin/linux/amd64/kubectl

# upload from removable media and install
install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# check
kubectl version
```

## Deploy Kubernetes Cluster

The following commands are divided into three parts: download, create, and deploy. The main variation between "Internet Access" and "Isolated Network" is that, for an isolated network, users will execute the download and create steps outside the isolated network's environment, while the deploy step is done inside the isolated network.

### Bootstrap k3d

```git
# download
git clone https://github.com/defenseunicorns/zarf-package-k3d-airgap.git
cd zarf-package-k3d-airgap

# create
zarf package create --confirm

zarf tools download-init

cd metallb
zarf package create --confirm
```

```git
# deploy
cd ../ # if still in metallb folder
mkdir temp && cd temp
zarf package deploy --set enable_traefik=false --set enable_service_lb=true --set enable_metrics_server=false --set enable_gpus=false ../zarf-package-*.tar.zst

cd ../
zarf init --components git-server --confirm

cd metallb
zarf package deploy --confirm zarf-package-*.tar.zst
```

Additional considerations are necessary for GPU deployments:

```git
# deploy
cd ../ # if still in metallb folder
# temp folder to catch extra files generated during deploy
mkdir temp && cd temp
# largest difference is setting `enable_gpus` to `true`
zarf package deploy --set enable_traefik=false --set enable_service_lb=true --set enable_metrics_server=false --set enable_gpus=true ../zarf-package-*.tar.zst

cd ../
zarf init --components git-server --confirm

cd metallb
zarf package deploy --confirm zarf-package-*.tar.zst
```

### UDS DUBBD

```git
# download
git clone https://github.com/defenseunicorns/uds-package-dubbd.git
cd uds-package-dubbd/k3d/

# create
docker login registry1.dso.mil # account creation is required
zarf package create --confirm

# deploy
zarf package deploy --confirm zarf-package-*.tar.zst
```

### Kyverno Configuration

As of UDS DUBBD, v0.12+, a recently implemented Kyverno policy is causing certain LeapfrogAI pods to be restricted from execution. As we undergo refactoring efforts transitioning towards [Pepr](https://github.com/defenseunicorns/pepr), Kyverno's abstract replacement, the following guidelines outline the process for temporarily modifying the policy status from `Enforce` to `Audit`.

```git
zarf tools kubectl patch clusterpolicy require-non-root-user --type='json' -p='[{"op": "replace", "path": "/spec/validationFailureAction", "value":"Audit"}]'
zarf tools kubectl patch clusterpolicy require-non-root-group --type='json' -p='[{"op": "replace", "path": "/spec/validationFailureAction", "value":"Audit"}]'
```

### GPU Support Test (Optional)

The following support test is an optional addition for GPU deployments and helps confirm that the cluster's pods have access to expected GPU resources:

```git
# download
git clone https://github.com/justinthelaw/gpu-support-test
cd leapfrogai-gpu-support-test

# create
zarf package create --confirm

# deploy
zarf package deploy zarf-package-*.tar.zst
# press "y" for prompt on deployment confirmation
# enter the number of GPU(s) that are expected to be available when prompted

# clean-up
zarf package remove gpu-support-test
zarf tools registry prune --confirm
```

## Deploy LeapfrogAI

### LeapfrogAI API

```git
# download
git clone https://github.com/defenseunicorns/leapfrogai-api.git
cd leapfrogai-api/

# create
zarf package create --confirm

# deploy
zarf package deploy zarf-package-*.zst --set ISTIO_ENABLED=true --set ISTIO_INJECTION=enabled --set ISTIO_GATEWAY=leapfrogai --components metallb-config --confirm
# if used without the `--confirm` flag, there are many prompted variables
# please read the variable descriptions in the zarf.yaml for more details
# after deploying the leapfrogai gateway, you may need to terminate the existing tenant gateway

# configure, this will be removed in a future API release
zarf tools kubectl patch virtualservice leapfrogai -n leapfrogai --type='json' -p '
[
  {
    "op": "replace",
    "path": "/spec",
    "value": {
      "gateways": [
        "istio-system/leapfrogai"
      ],
      "hosts": [
        "*"
      ],
      "http": [
        {
          "match": [
            {
              "uri": {
                "prefix": "/leapfrogai-api/"
              }
            }
          ],
          "rewrite": {
            "uri": "/"
          },
          "route": [
            {
              "destination": {
                "host": "api",
                "port": {
                  "number": 8080
                }
              }
            }
          ]
        },
        {
          "match": [
            {
              "uri": {
                "prefix": "/openapi.json"
              }
            }
          ],
          "redirect": {
            "uri": "/leapfrogai-api/openapi.json"
          }
        }
      ]
    }
  }
]'
```

### Whisper Model (Optional)

Deploy the Whisper Model for automatic speech recognition that transcribes speech to text. The Whisper Model backend is bundled with pre-packaged components, including Whisper-Base (limited to English language) and Faster-Whisper, which serves as the dedicated inferencing engine.

```git
# download
git clone https://github.com/defenseunicorns/leapfrogai-backend-whisper.git
cd leapfrogai-backend-whisper

# create
zarf package create --confirm

# deploy
zarf package deploy zarf-package-*.tar.zst --confirm
```

Additional considerations are necessary for GPU deployments:

The package deployment command is modified for GPU deployments:

```git
# deploy
zarf package deploy zarf-package-*.tar.zst --set GPU_ENABLED=true --confirm
```

### LLaMA CPP Python

This backend comes pre-packaged with synthia-7b-v2.0.Q4_K_M, and `llama-cpp-python` as the inferencing engine.

```git
# download
git clone https://github.com/defenseunicorns/leapfrogai-backend-llama-cpp-python.git
cd leapfrogai-backend-llama-cpp-python

# create
zarf package create --confirm
```

Additional considerations are necessary for GPU deployments:

The package deployment command is modified for GPU deployments:

```git
# deploy
zarf package deploy zarf-package-*.tar.zst --set GPU_ENABLED=true --confirm
```

### LeapfrogAI UI (Optional)

```git
# download
git clone https://github.com/defenseunicorns/leapfrogai-ui
cd leapfrogai-ui

# create
zarf package create --confirm

# deploy
cd leapfrogai-ui
zarf package deploy zarf-package-*.tar.zst --confirm
# if used without the `--confirm` flag, there are many prompted variables
# please read the variable descriptions in the zarf.yaml for more details
```

### Setup Ingress/Egress

```git
k3d cluster edit zarf-k3d --port-add "443:30535@loadbalancer"
k3d cluster edit zarf-k3d --port-add "8080:30535@loadbalancer"

# if the load balancer does not restart
k3d cluster start zarf-k3d
```

## LeapfrogAI UI and API

- Navigate to `https://localhost:8080` to interact with LeapfrogAI UI.
- Navigate to `https://localhost:8080/leapfrogai-api/docs` to see usage details for the LeapfrogAI API.

## Termination and Cleanup Procedures

### Stop k3d Cluster

Perform one of the following cleanup methods. The k3d command is the preferred method:

```git
k3d cluster stop zarf-k3d
```

OR:

```git
docker ps
# obtain the k3d cluster's container ID
docker stop <K3D_CLUSTER_CONTAINER_ID>
```

### Stop Zarf Registry

```git
docker ps
# obtain the registry container ID
docker stop <REGISTRY_CONTAINER_ID>
```

### Cleanup

Executing this command will remove all entities that are not associated with an active process.

```git
docker system prune -a -f && docker volume prune -f
zarf tools clear-cache
rm -rf /tmp/zarf-*
```

## Troubleshooting

The following outlines occasional deployment issues our teams have identified, which you may also encounter.

### Cluster Connection

**Issue:** After performing a restart or restarting the docker service, the cluster cannot be connected with.

**Action:**

```git
k3d cluster list
# verify that the cluster has `LOADBALANCER` set to true
# if not, try the following
k3d cluster stop zarf-k3d
k3d cluster start zarf-k3d
```

### Disk Pressure

**Issue:** In certain scenarios, uploading multiple large AI models may lead to storage issues. To address this, there are several measures you can take to either optimize disk space usage or augment available space within a designated partition.

**Action:**  Remove unused files and storage. *Executing this command will remove all entities that are not associated with an active process.* Execute the following command sets to eliminate dangling or extraneous items. Additionally, consider deleting any previously deployed Zarf Packages to free up storage space.

```git
# prune images stored in the local registry
zarf tools registry prune --confirm
# prune docker images, press "y" to confirm
docker image prune
# prune volumes, press "y" to confirm
docker volume prune
# clear zarf cache and temp files
zarf tools clear-cache
rm -rf /tmp/zarf-*
```

OR:

**Action:**

Check your disk's or mount's remaining space and utilization.

```git
df -h
```

Go to the disk or mount in question, and check on the following paths:

```git
ls -la /tmp
ls -la /var/lib/docker
```

In addition to your present working directory, the above paths are commonly identified as potential sources of excessive space consumption. To resolve this issue, it may be necessary to conduct manual cleanup or allocate additional space for the disks or mounts associated with these paths.

### GPU Acceleration

**Issue:** GPU access for Docker containers or pods in the Kubernetes cluster.

**Action:** Please navigate to and read the [`gpu-support-test`](https://github.com/justinthelaw/gpu-support-test) repository.
