ARCH ?= amd64
REG_PORT ?= 5000
REG_NAME ?= registry
LOCAL_VERSION ?= $(shell git rev-parse --short HEAD)
DOCKER_FLAGS :=
ZARF_FLAGS :=
FLAVOR := upstream
SILENT_DOCKER_FLAGS := --quiet
SILENT_ZARF_FLAGS := --no-progress -l warn --no-color
MAX_JOBS := 4
######################################################################################

.PHONY: help
help: ## Display this help information
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| sort | awk 'BEGIN {FS = ":.*?## "}; \
		{printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

## Clean up targets for test artifacts, cachce, etc.
include mk-clean.mk

gen-python: ## Generate the protobufs for the OpenAI typing within the leapfrogai_api module
	python3 -m grpc_tools.protoc -I src/leapfrogai_sdk/proto \
			--pyi_out=src/. \
			--python_out=src/. \
			--grpc_python_out=src/. \
			src/leapfrogai_sdk/proto/leapfrogai_sdk/**/*.proto

local-registry: ## Start up a local container registry. Errors in this target are ignored.
	@echo "Creating local Docker registry..."
	-@docker run -d -p ${REG_PORT}:5000 --restart=always --name ${REG_NAME} registry:2
	@echo "Local registry created at localhost:${REG_PORT}"


# Clean up: Stop and remove the local registry
clean-registry:
	@echo "Cleaning up..."
	@docker stop ${REG_NAME}
	@docker rm ${REG_NAME}

sdk-wheel: ## build wheels for the leapfrogai_sdk package as a dependency for other lfai components
	docker build ${DOCKER_FLAGS} --platform=linux/${ARCH} -t ghcr.io/defenseunicorns/leapfrogai/leapfrogai-sdk:${LOCAL_VERSION} -f src/leapfrogai_sdk/Dockerfile .

docker-supabase:
	## Build the migration container for this version of the supabase package
	docker build ${DOCKER_FLAGS} -t ghcr.io/defenseunicorns/leapfrogai/supabase-migrations:${LOCAL_VERSION} -f Dockerfile.migrations --build-arg="MIGRATIONS_DIR=packages/supabase/migrations" .
	docker tag ghcr.io/defenseunicorns/leapfrogai/supabase-migrations:${LOCAL_VERSION} localhost:${REG_PORT}/defenseunicorns/leapfrogai/supabase-migrations:${LOCAL_VERSION}

build-supabase: local-registry docker-supabase
	docker push ${DOCKER_FLAGS} localhost:${REG_PORT}/defenseunicorns/leapfrogai/supabase-migrations:${LOCAL_VERSION}

	## Build the Zarf package
	uds zarf package create packages/supabase --flavor ${FLAVOR} -a ${ARCH} -o packages/supabase --registry-override=ghcr.io=localhost:${REG_PORT} --set IMAGE_VERSION=${LOCAL_VERSION} ${ZARF_FLAGS} --confirm

docker-api: local-registry sdk-wheel
	@echo $(DOCKER_FLAGS)
	@echo $(ZARF_FLAGS)
ifeq ($(FLAVOR),upstream)
	## Build the API image (and tag it for the local registry)
	docker build ${DOCKER_FLAGS} --platform=linux/${ARCH} --build-arg LOCAL_VERSION=${LOCAL_VERSION} -t ghcr.io/defenseunicorns/leapfrogai/leapfrogai-api:${LOCAL_VERSION} -f packages/api/Dockerfile .
	docker tag ghcr.io/defenseunicorns/leapfrogai/leapfrogai-api:${LOCAL_VERSION} localhost:${REG_PORT}/defenseunicorns/leapfrogai/leapfrogai-api:${LOCAL_VERSION}
endif
	## Build the migration container for this version of the API
	docker build ${DOCKER_FLAGS} --platform=linux/${ARCH} -t ghcr.io/defenseunicorns/leapfrogai/api-migrations:${LOCAL_VERSION} -f Dockerfile.migrations --build-arg="MIGRATIONS_DIR=packages/api/supabase/migrations" .
	docker tag ghcr.io/defenseunicorns/leapfrogai/api-migrations:${LOCAL_VERSION} localhost:${REG_PORT}/defenseunicorns/leapfrogai/api-migrations:${LOCAL_VERSION}

build-api: local-registry docker-api ## Build the leapfrogai_api container and Zarf package
ifeq ($(FLAVOR),upstream)
	## Push the images to the local registry (Zarf is super slow if the image is only in the local daemon)
	docker push ${DOCKER_FLAGS} localhost:${REG_PORT}/defenseunicorns/leapfrogai/leapfrogai-api:${LOCAL_VERSION}
endif
	docker push ${DOCKER_FLAGS} localhost:${REG_PORT}/defenseunicorns/leapfrogai/api-migrations:${LOCAL_VERSION}

	## Build the Zarf package
	uds zarf package create packages/api --flavor ${FLAVOR} -a ${ARCH} -o packages/api --registry-override=ghcr.io=localhost:${REG_PORT} --insecure --set IMAGE_VERSION=${LOCAL_VERSION} ${ZARF_FLAGS} --confirm

docker-ui:
	## Build the UI image (and tag it for the local registry)
	docker build ${DOCKER_FLAGS} --platform=linux/${ARCH} -t ghcr.io/defenseunicorns/leapfrogai/leapfrogai-ui:${LOCAL_VERSION} src/leapfrogai_ui
	docker tag ghcr.io/defenseunicorns/leapfrogai/leapfrogai-ui:${LOCAL_VERSION} localhost:${REG_PORT}/defenseunicorns/leapfrogai/leapfrogai-ui:${LOCAL_VERSION}

	## Build the migration container for the version of the UI
	docker build ${DOCKER_FLAGS} --platform=linux/${ARCH} -t ghcr.io/defenseunicorns/leapfrogai/ui-migrations:${LOCAL_VERSION} -f Dockerfile.migrations --build-arg="MIGRATIONS_DIR=src/leapfrogai_ui/supabase/migrations" .
	docker tag ghcr.io/defenseunicorns/leapfrogai/ui-migrations:${LOCAL_VERSION} localhost:${REG_PORT}/defenseunicorns/leapfrogai/ui-migrations:${LOCAL_VERSION}

build-ui: local-registry docker-ui ## Build the leapfrogai_ui container and Zarf package
	## Push the image to the local registry (Zarf is super slow if the image is only in the local daemon)
	docker push ${DOCKER_FLAGS} localhost:${REG_PORT}/defenseunicorns/leapfrogai/leapfrogai-ui:${LOCAL_VERSION}
	docker push ${DOCKER_FLAGS} localhost:${REG_PORT}/defenseunicorns/leapfrogai/ui-migrations:${LOCAL_VERSION}

	## Build the Zarf package
	uds zarf package create packages/ui --flavor ${FLAVOR} -a ${ARCH} -o packages/ui --registry-override=ghcr.io=localhost:${REG_PORT} --insecure --set IMAGE_VERSION=${LOCAL_VERSION} ${ZARF_FLAGS} --confirm

docker-llama-cpp-python: sdk-wheel
	## Build the image (and tag it for the local registry)
	docker build ${DOCKER_FLAGS} --platform=linux/${ARCH} --build-arg LOCAL_VERSION=${LOCAL_VERSION} -t ghcr.io/defenseunicorns/leapfrogai/llama-cpp-python:${LOCAL_VERSION} -f packages/llama-cpp-python/Dockerfile .
	docker tag ghcr.io/defenseunicorns/leapfrogai/llama-cpp-python:${LOCAL_VERSION} localhost:${REG_PORT}/defenseunicorns/leapfrogai/llama-cpp-python:${LOCAL_VERSION}

build-llama-cpp-python: local-registry docker-llama-cpp-python ## Build the llama-cpp-python (cpu) container and Zarf package
	## Push the image to the local registry (Zarf is super slow if the image is only in the local daemon)
	docker push ${DOCKER_FLAGS} localhost:${REG_PORT}/defenseunicorns/leapfrogai/llama-cpp-python:${LOCAL_VERSION}

	## Build the Zarf package
	uds zarf package create packages/llama-cpp-python --flavor ${FLAVOR} -a ${ARCH} -o packages/llama-cpp-python --registry-override=ghcr.io=localhost:${REG_PORT} --insecure --set IMAGE_VERSION=${LOCAL_VERSION} ${ZARF_FLAGS} --confirm

docker-vllm: sdk-wheel
	## Build the image (and tag it for the local registry)
	docker build ${DOCKER_FLAGS} --platform=linux/${ARCH} --build-arg LOCAL_VERSION=${LOCAL_VERSION} -t ghcr.io/defenseunicorns/leapfrogai/vllm:${LOCAL_VERSION} -f packages/vllm/Dockerfile .
	docker tag ghcr.io/defenseunicorns/leapfrogai/vllm:${LOCAL_VERSION} localhost:${REG_PORT}/defenseunicorns/leapfrogai/vllm:${LOCAL_VERSION}

build-vllm: local-registry docker-vllm ## Build the vllm container and Zarf package
	## Push the image to the local registry (Zarf is super slow if the image is only in the local daemon)
	docker push ${DOCKER_FLAGS} localhost:${REG_PORT}/defenseunicorns/leapfrogai/vllm:${LOCAL_VERSION}

	## Build the Zarf package
	ZARF_CONFIG=packages/vllm/zarf-config.yaml uds zarf package create packages/vllm --flavor ${FLAVOR} -a ${ARCH} -o packages/vllm --registry-override=ghcr.io=localhost:${REG_PORT} --insecure --set IMAGE_VERSION=${LOCAL_VERSION} ${ZARF_FLAGS} --confirm

docker-text-embeddings: sdk-wheel
	## Build the image (and tag it for the local registry)
	docker build ${DOCKER_FLAGS} --platform=linux/${ARCH} --build-arg LOCAL_VERSION=${LOCAL_VERSION} -t ghcr.io/defenseunicorns/leapfrogai/text-embeddings:${LOCAL_VERSION} -f packages/text-embeddings/Dockerfile .
	docker tag ghcr.io/defenseunicorns/leapfrogai/text-embeddings:${LOCAL_VERSION} localhost:${REG_PORT}/defenseunicorns/leapfrogai/text-embeddings:${LOCAL_VERSION}

build-text-embeddings: local-registry docker-text-embeddings ## Build the text-embeddings container and Zarf package
	## Push the image to the local registry (Zarf is super slow if the image is only in the local daemon)
	docker push ${DOCKER_FLAGS} localhost:${REG_PORT}/defenseunicorns/leapfrogai/text-embeddings:${LOCAL_VERSION}

	## Build the Zarf package
	uds zarf package create packages/text-embeddings --flavor ${FLAVOR} -a ${ARCH} -o packages/text-embeddings --registry-override=ghcr.io=localhost:${REG_PORT} --insecure --set IMAGE_VERSION=${LOCAL_VERSION} ${ZARF_FLAGS} --confirm


docker-whisper: sdk-wheel
	## Build the image (and tag it for the local registry)
	docker build ${DOCKER_FLAGS} --platform=linux/${ARCH} --build-arg LOCAL_VERSION=${LOCAL_VERSION} -t ghcr.io/defenseunicorns/leapfrogai/whisper:${LOCAL_VERSION} -f packages/whisper/Dockerfile .
	docker tag ghcr.io/defenseunicorns/leapfrogai/whisper:${LOCAL_VERSION} localhost:${REG_PORT}/defenseunicorns/leapfrogai/whisper:${LOCAL_VERSION}

build-whisper: local-registry docker-whisper ## Build the whisper container and zarf package
	## Push the image to the local registry (Zarf is super slow if the image is only in the local daemon)
	docker push ${DOCKER_FLAGS} localhost:${REG_PORT}/defenseunicorns/leapfrogai/whisper:${LOCAL_VERSION}

	## Build the Zarf package
	uds zarf package create packages/whisper --flavor ${FLAVOR} -a ${ARCH} -o packages/whisper --registry-override=ghcr.io=localhost:${REG_PORT} --insecure --set IMAGE_VERSION=${LOCAL_VERSION} ${ZARF_FLAGS} --confirm

docker-repeater: sdk-wheel
	## Build the image (and tag it for the local registry)
	docker build ${DOCKER_FLAGS} --platform=linux/${ARCH} --build-arg LOCAL_VERSION=${LOCAL_VERSION} -t ghcr.io/defenseunicorns/leapfrogai/repeater:${LOCAL_VERSION} -f packages/repeater/Dockerfile .
	docker tag ghcr.io/defenseunicorns/leapfrogai/repeater:${LOCAL_VERSION} localhost:${REG_PORT}/defenseunicorns/leapfrogai/repeater:${LOCAL_VERSION}

build-repeater: local-registry docker-repeater ## Build the repeater container and zarf package
	## Push the image to the local registry (Zarf is super slow if the image is only in the local daemon)
	docker push ${DOCKER_FLAGS} localhost:${REG_PORT}/defenseunicorns/leapfrogai/repeater:${LOCAL_VERSION}

	## Build the Zarf package
	uds zarf package create packages/repeater --flavor ${FLAVOR} -a ${ARCH} -o packages/repeater --registry-override=ghcr.io=localhost:${REG_PORT} --insecure --set IMAGE_VERSION=${LOCAL_VERSION} ${ZARF_FLAGS} --confirm

build-cpu: build-supabase build-api build-ui build-llama-cpp-python build-text-embeddings build-whisper ## Build all zarf packages for a cpu-enabled deployment of LFAI

build-gpu: build-supabase build-api build-ui build-vllm build-text-embeddings build-whisper ## Build all zarf packages for a gpu-enabled deployment of LFAI

build-all: build-cpu build-gpu ## Build all of the LFAI packages

include tests/Makefile

include packages/k3d-gpu/Makefile

silent-build-api-parallel:
	@echo "API build started"
	@mkdir -p .logs
	@$(MAKE) build-api DOCKER_FLAGS="$(DOCKER_FLAGS) $(SILENT_DOCKER_FLAGS)" ZARF_FLAGS="$(ZARF_FLAGS) $(SILENT_ZARF_FLAGS)" > .logs/build-api.log 2>&1
	@echo "API build completed"

silent-build-supabase-parallel:
	@echo "Supabase build started"
	@mkdir -p .logs
	@$(MAKE) build-supabase DOCKER_FLAGS="$(DOCKER_FLAGS) $(SILENT_DOCKER_FLAGS)" ZARF_FLAGS="$(ZARF_FLAGS) $(SILENT_ZARF_FLAGS)" > .logs/build-supabase.log 2>&1
	@echo "Supabase build completed"

silent-build-ui-parallel:
	@echo "UI build started"
	@mkdir -p .logs
	@$(MAKE) build-ui DOCKER_FLAGS="$(DOCKER_FLAGS) $(SILENT_DOCKER_FLAGS)" ZARF_FLAGS="$(ZARF_FLAGS) $(SILENT_ZARF_FLAGS)" > .logs/build-ui.log 2>&1
	@echo "UI build completed"

silent-build-vllm-parallel:
	@echo "VLLM build started"
	@mkdir -p .logs
	@$(MAKE) build-vllm DOCKER_FLAGS="$(DOCKER_FLAGS) $(SILENT_DOCKER_FLAGS)" ZARF_FLAGS="$(ZARF_FLAGS) $(SILENT_ZARF_FLAGS)" > .logs/build-vllm.log 2>&1
	@echo "VLLM build completed"

silent-build-llama-cpp-python-parallel:
	@echo "llama-cpp-python build started"
	@mkdir -p .logs
	@$(MAKE) build-llama-cpp-python DOCKER_FLAGS="$(DOCKER_FLAGS) $(SILENT_DOCKER_FLAGS)" ZARF_FLAGS="$(ZARF_FLAGS) $(SILENT_ZARF_FLAGS)" > .logs/build-llama-cpp-python.log 2>&1
	@echo "llama-cpp-python build completed"

silent-build-text-embeddings-parallel:
	@echo "text-embeddings build started"
	@mkdir -p .logs
	@$(MAKE) build-text-embeddings DOCKER_FLAGS="$(DOCKER_FLAGS) $(SILENT_DOCKER_FLAGS)" ZARF_FLAGS="$(ZARF_FLAGS) $(SILENT_ZARF_FLAGS)" > .logs/build-text-embeddings.log 2>&1
	@echo "text-embeddings build completed"

silent-build-whisper-parallel:
	@echo "whisper build started"
	@mkdir -p .logs
	@$(MAKE) build-whisper DOCKER_FLAGS="$(DOCKER_FLAGS) $(SILENT_DOCKER_FLAGS)" ZARF_FLAGS="$(ZARF_FLAGS) $(SILENT_ZARF_FLAGS)" > .logs/build-whisper.log 2>&1
	@echo "whisper build completed"

silent-build-all:
	@echo "Starting parallel builds..."
	@echo "Logs at .logs/*.log"
	@mkdir -p .logs
	@$(MAKE) -j${MAX_JOBS} silent-build-api-parallel silent-build-supabase-parallel silent-build-ui-parallel silent-build-vllm-parallel silent-build-llama-cpp-python-parallel silent-build-text-embeddings-parallel silent-build-whisper-parallel
	@echo "All builds completed"

silent-build-gpu:
	@echo "Starting parallel builds..."
	@echo "Logs at .logs/*.log"
	@mkdir -p .logs
	@$(MAKE) -j${MAX_JOBS} silent-build-api-parallel silent-build-supabase-parallel silent-build-ui-parallel silent-build-vllm-parallel silent-build-text-embeddings-parallel silent-build-whisper-parallel
	@echo "All builds completed"

silent-build-cpu:
	@echo "Starting parallel builds..."
	@echo "Logs at .logs/*.log"
	@mkdir -p .logs
	@$(MAKE) -j${MAX_JOBS} silent-build-api-parallel silent-build-supabase-parallel silent-build-ui-parallel silent-build-llama-cpp-python-parallel silent-build-text-embeddings-parallel silent-build-whisper-parallel
	@echo "All builds completed"

# Define individual deployment targets
silent-deploy-supabase-package:
	@echo "Starting Supabase deployment..."
	@mkdir -p .logs
	@uds zarf package deploy packages/supabase/zarf-package-supabase-${ARCH}-${LOCAL_VERSION}.tar.zst ${ZARF_FLAGS} --confirm > .logs/deploy-supabase.log 2>&1
	@echo "Supabase deployment completed"

silent-deploy-api-package:
	@echo "Starting API deployment..."
	@mkdir -p .logs
	@uds zarf package deploy packages/api/zarf-package-leapfrogai-api-${ARCH}-${LOCAL_VERSION}.tar.zst ${ZARF_FLAGS} --confirm > .logs/deploy-api.log 2>&1
	@echo "API deployment completed"

silent-deploy-ui-package:
	@echo "Starting UI deployment..."
	@mkdir -p .logs
	@uds zarf package deploy packages/ui/zarf-package-leapfrogai-ui-${ARCH}-${LOCAL_VERSION}.tar.zst ${ZARF_FLAGS} --confirm > .logs/deploy-ui.log 2>&1
	@echo "UI deployment completed"

silent-deploy-llama-cpp-python-package:
	@echo "Starting llama-cpp-python deployment..."
	@mkdir -p .logs
	@uds zarf package deploy packages/llama-cpp-python/zarf-package-llama-cpp-python-${ARCH}-${LOCAL_VERSION}.tar.zst ${ZARF_FLAGS} --confirm > .logs/deploy-llama-cpp-python.log 2>&1
	@echo "llama-cpp-python deployment completed"

silent-deploy-vllm-package:
	@echo "Starting VLLM deployment..."
	@mkdir -p .logs
	@ZARF_CONFIG=packages/vllm/zarf-config.yaml uds zarf package deploy packages/vllm/zarf-package-vllm-${ARCH}-${LOCAL_VERSION}.tar.zst ${ZARF_FLAGS} --confirm > .logs/deploy-vllm.log 2>&1
	@echo "VLLM deployment completed"

silent-deploy-text-embeddings-package:
	@echo "Starting text-embeddings deployment..."
	@mkdir -p .logs
	@uds zarf package deploy packages/text-embeddings/zarf-package-text-embeddings-${ARCH}-${LOCAL_VERSION}.tar.zst ${ZARF_FLAGS} --confirm > .logs/deploy-text-embeddings.log 2>&1
	@echo "text-embeddings deployment completed"

silent-deploy-whisper-package:
	@echo "Starting whisper deployment..."
	@mkdir -p .logs
	@uds zarf package deploy packages/whisper/zarf-package-whisper-${ARCH}-${LOCAL_VERSION}.tar.zst ${ZARF_FLAGS} --confirm > .logs/deploy-whisper.log 2>&1
	@echo "whisper deployment completed"

silent-deploy-cpu:
	@echo "Logs at .logs/*.log"
	@echo "Starting parallel deployments..."
	@echo "Deploying Supabase first to avoid migration issues."
	@$(MAKE) silent-deploy-supabase-package ZARF_FLAGS="$(ZARF_FLAGS) $(SILENT_ZARF_FLAGS)"
	@echo "Deploying the rest of the packages..."
	@$(MAKE) -j${MAX_JOBS} \
		silent-deploy-api-package ZARF_FLAGS="$(ZARF_FLAGS) $(SILENT_ZARF_FLAGS)" \
		silent-deploy-ui-package ZARF_FLAGS="$(ZARF_FLAGS) $(SILENT_ZARF_FLAGS)" \
		silent-deploy-llama-cpp-python-package ZARF_FLAGS="$(ZARF_FLAGS) $(SILENT_ZARF_FLAGS)" \
		silent-deploy-text-embeddings-package ZARF_FLAGS="$(ZARF_FLAGS) $(SILENT_ZARF_FLAGS)" \
		silent-deploy-whisper-package ZARF_FLAGS="$(ZARF_FLAGS) $(SILENT_ZARF_FLAGS)"
	@echo "All deployments completed"

silent-deploy-gpu:
	@echo "Logs at .logs/*.log"
	@echo "Starting parallel deployments..."
	@echo "Deploying Supabase first to avoid migration issues."
	@$(MAKE) silent-deploy-supabase-package ZARF_FLAGS="$(ZARF_FLAGS) $(SILENT_ZARF_FLAGS)"
	@echo "Deploying API and models..."
	@$(MAKE) -j${MAX_JOBS} \
		silent-deploy-api-package ZARF_FLAGS="${ZARF_FLAGS} ${SILENT_ZARF_FLAGS}" \
		silent-deploy-vllm-package ZARF_FLAGS="${ZARF_FLAGS} ${SILENT_ZARF_FLAGS}" \
		silent-deploy-text-embeddings-package ZARF_FLAGS="${ZARF_FLAGS} ${SILENT_ZARF_FLAGS} --set=GPU_RUNTIME='nvidia'" \
		silent-deploy-whisper-package ZARF_FLAGS="${ZARF_FLAGS} ${SILENT_ZARF_FLAGS} --set=GPU_RUNTIME='nvidia'"
	@echo "Deploying UI..."
	@$(MAKE) silent-deploy-ui-package ZARF_FLAGS="${ZARF_FLAGS} ${SILENT_ZARF_FLAGS} --set=MODEL='vllm'"
	@echo "All deployments completed"

silent-fresh-leapfrogai-gpu:
	@echo "Cleaning up previous artifacts..."
	@$(MAKE) clean-artifacts > /dev/null 2>&1
	@echo "Logs at .logs/*.log"
	@mkdir -p .logs
	@echo "Creating a uds gpu enabled cluster..."
	@$(MAKE) create-uds-gpu-cluster DOCKER_FLAGS="${SILENT_DOCKER_FLAGS}" ZARF_FLAGS="${SILENT_ZARF_FLAGS}" > .logs/create-uds-gpu-cluster.log 2>&1
	@echo "Testing the uds gpu cluster..."
	@$(MAKE) test-uds-gpu-cluster > .logs/test-uds-gpu-cluster.log 2>&1
	@echo "Building all packages..."
	@$(MAKE) silent-build-gpu
	@echo "Deploying all packages..."
	@$(MAKE) silent-deploy-gpu
	@echo "Done!"
	@echo "UI is available at https://ai.uds.dev"
	@echo "API is available at https://leapfrogai-api.uds.dev"

silent-fresh-leapfrogai-cpu:
	@echo "Cleaning up previous artifacts..."
	@$(MAKE) clean-artifacts > /dev/null 2>&1
	@echo "Logs at .logs/*.log"
	@mkdir -p .logs
	@echo "Creating a uds cpu-only cluster..."
	@$(MAKE) create-uds-cpu-cluster DOCKER_FLAGS="${SILENT_DOCKER_FLAGS}" ZARF_FLAGS="${SILENT_ZARF_FLAGS}" > .logs/create-uds-cpu-cluster.log 2>&1
	@echo "Building all packages..."
	@$(MAKE) silent-build-cpu
	@echo "Deploying all packages..."
	@$(MAKE) silent-deploy-cpu
	@echo "Done!"
	@echo "UI is available at https://ai.uds.dev"
	@echo "API is available at https://leapfrogai-api.uds.dev"
