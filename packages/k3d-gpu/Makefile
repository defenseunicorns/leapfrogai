
REG_PORT ?= 5000
REG_NAME ?= registry

MAKEFILE_DIR := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
ORGANIZATION := defenseunicorns
PLATFORM := linux/amd64
TAG := latest
K3D_CLUSTER_NAME := k3d-core-slim-dev:0.24.0
K3S_TAG := $(shell jq -r .k3s_tag ${MAKEFILE_DIR}/version_config.json)
CUDA_TAG := $(shell jq -r .cuda_tag ${MAKEFILE_DIR}/version_config.json)

echo-config:
	@echo "DIR: ${MAKEFILE_DIR}"
	@echo "K3S_TAG: ${K3S_TAG}"
	@echo "CUDA_TAG: ${CUDA_TAG}"

local-registry: ## Start up a local container registry. Errors in this target are ignored.
	@echo "Creating local Docker registry..."
	-@docker run -d -p ${REG_PORT}:5000 --restart=always --name ${REG_NAME} registry:2
	@echo "Local registry created at localhost:${REG_PORT}"

build-k3d-gpu: local-registry echo-config ## Build the k3d-gpu-support image
# Change to the root of the repository and build the image
	@cd ${MAKEFILE_DIR}/../.. && \
	docker build \
	 --platform=${PLATFORM} \
	 --build-arg K3S_TAG=${K3S_TAG} \
	 --build-arg CUDA_TAG=${CUDA_TAG} \
	 -t ghcr.io/${ORGANIZATION}/k3d-gpu-support:${TAG} \
	 -f ${MAKEFILE_DIR}/Dockerfile .
# Tag the image for the local registry
	@docker tag ghcr.io/${ORGANIZATION}/k3d-gpu-support:${TAG} localhost:${REG_PORT}/${ORGANIZATION}/k3d-gpu-support:${TAG}

push-k3d-gpu: local-registry build-k3d-gpu
	@docker push localhost:${REG_PORT}/${ORGANIZATION}/k3d-gpu-support:${TAG}

uds-gpu-cluster: local-registry build-k3d-gpu push-k3d-gpu
	uds deploy ${K3D_CLUSTER_NAME} --set K3D_EXTRA_ARGS="--gpus=all --image=localhost:${REG_PORT}/${ORGANIZATION}/k3d-gpu-support:${TAG}" --confirm

test-k3d-gpu:
	@uds zarf tools kubectl apply -f ${MAKEFILE_DIR}/test/cuda-vector-add.yaml
	@uds zarf tools kubectl wait --for=jsonpath='{.status.phase}'=Succeeded --timeout=15s pod -l app=gpu-pod
	@uds zarf tools kubectl logs -l app=gpu-pod
	@uds zarf tools kubectl delete -f ${MAKEFILE_DIR}/test/cuda-vector-add.yaml

.PHONY: all local-registry build-k3d-gpu push-k3d-gpu test-k3d-gpu
