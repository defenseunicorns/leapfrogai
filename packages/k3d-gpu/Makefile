MAKEFILE_DIR := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

k3d-gpu-package:
	@cd ${MAKEFILE_DIR} && \
	uds zarf package create

create-uds-gpu-cluster:
	@cd ${MAKEFILE_DIR} && \
	uds zarf package deploy zarf-package-k3d-gpu-amd64-*.tar.zst --confirm

.PHONY: k3d-gpu-package create-uds-gpu-cluster
