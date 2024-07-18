
MAKEFILE_DIR := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
REGISTRY_NAME := registry
REGISTRY_PORT := 5000
SHELL_SCRIPT := build.sh
ORGANIZATION := defenseunicorns
PLATFORM := linux/amd64
TAG := latest
K3D_CLUSTER_NAME := k3d-core-slim-dev:0.24.0

# Create local Docker registry
local-registry:
	@echo "Creating local Docker registry..."
	-@docker run -d -p ${REGISTRY_PORT}:5000 --name ${REGISTRY_NAME} registry:2
	@echo "Local registry created at localhost:${REGISTRY_PORT}"

build-k3d-gpu: local-registry
	@docker build --platform=${PLATFORM} -t ghcr.io/${ORGANIZATION}/k3d-gpu-support:${TAG} -f ${MAKEFILE_DIR}/Dockerfile ${MAKEFILE_DIR}
	@docker tag ghcr.io/${ORGANIZATION}/k3d-gpu-support:${TAG} localhost:${REGISTRY_PORT}/${ORGANIZATION}/k3d-gpu-support:${TAG}

push-k3d-gpu: local-registry build-k3d-gpu
	@docker push localhost:${REGISTRY_PORT}/${ORGANIZATION}/k3d-gpu-support:${TAG}

uds-gpu-cluster: local-registry build-k3d-gpu push-k3d-gpu
	uds deploy ${K3D_CLUSTER_NAME} --set K3D_EXTRA_ARGS="--gpus=all --image=localhost:${REGISTRY_PORT}/${ORGANIZATION}/k3d-gpu-support:${TAG}" --confirm

test-k3d-gpu:
	@uds zarf tools kubectl apply -f ${MAKEFILE_DIR}/test/cuda-vector-add.yaml
	@uds zarf tools kubectl wait --for=jsonpath='{.status.phase}'=Succeeded --timeout=15s pod -l app=gpu-pod
	@uds zarf tools kubectl logs -l app=gpu-pod
	@uds zarf tools kubectl delete -f ${MAKEFILE_DIR}/test/cuda-vector-add.yaml

.PHONY: all local-registry build-k3d-gpu push-k3d-gpu test-k3d-gpu
