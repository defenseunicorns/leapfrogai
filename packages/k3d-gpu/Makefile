MAKEFILE_DIR := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

UDS_VERSION := k3d-core-slim-dev:0.26.1
LOCAL_VERSION ?= $(shell git rev-parse --short HEAD)
DOCKER_FLAGS :=
ZARF_FLAGS :=

build-k3d-gpu:
	@cd ${MAKEFILE_DIR} && \
	docker build \
	${DOCKER_FLAGS} \
	--platform linux/amd64 \
	-t ghcr.io/defenseunicorns/leapfrogai/k3d-gpu:${LOCAL_VERSION} .

create-uds-gpu-cluster: build-k3d-gpu
	@uds deploy ${UDS_VERSION} \
	${ZARF_FLAGS} \
	--set K3D_EXTRA_ARGS="--gpus=all \
	--image=ghcr.io/defenseunicorns/leapfrogai/k3d-gpu:${LOCAL_VERSION}" --confirm

create-uds-cpu-cluster:
	@uds deploy ${UDS_VERSION} \
	${ZARF_FLAGS} \
	--confirm

test-uds-gpu-cluster:
	@cd ${MAKEFILE_DIR} && \
	uds zarf tools kubectl apply -f ./test/cuda-vector-add.yaml
	@uds zarf tools kubectl wait --for=jsonpath='{.status.phase}'=Succeeded --timeout=15s pod -l app=gpu-pod
	@uds zarf tools kubectl logs -l app=gpu-pod
	@cd ${MAKEFILE_DIR} && \
	uds zarf tools kubectl delete -f ./test/cuda-vector-add.yaml

.PHONY: build-k3d-gpu create-uds-gpu-cluster create-uds-cpu-cluster test-uds-gpu-cluster
