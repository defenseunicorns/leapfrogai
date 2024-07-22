MAKEFILE_DIR := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

UDS_VERSION := 0.24.1
LOCAL_VERSION ?= $(shell git rev-parse --short HEAD)


build-k3d-gpu:
	@cd ${MAKEFILE_DIR} && \
	docker build \
	--platform linux/amd64 \
	-t ghcr.io/defenseunicorns/leapfrogai/k3d-gpu:${LOCAL_VERSION} .

create-uds-gpu-cluster: build-k3d-gpu
	@uds deploy k3d-core-slim-dev:${UDS_VERSION} \
	--set K3D_EXTRA_ARGS="--gpus=all \
	--image=ghcr.io/defenseunicorns/leapfrogai/k3d-gpu:${LOCAL_VERSION}" --confirm

test-uds-gpu-cluster:
	@cd ${MAKEFILE_DIR} && \
	uds zarf tools kubectl apply -f ./test/cuda-vector-add.yaml
	@uds zarf tools kubectl wait --for=jsonpath='{.status.phase}'=Succeeded --timeout=15s pod -l app=gpu-pod
	@uds zarf tools kubectl logs -l app=gpu-pod
	@cd ${MAKEFILE_DIR} && \
	uds zarf tools kubectl delete -f ./test/cuda-vector-add.yaml

.PHONY: build-k3d-gpu create-uds-gpu-cluster test-uds-gpu-cluster
