ARCH ?= amd64
FLAVOR ?= upstream
REG_PORT ?= 5000
REG_NAME ?= registry
LOCAL_VERSION ?= $(shell git rev-parse --short HEAD)
DOCKER_FLAGS :=
ZARF_FLAGS :=
SILENT_DOCKER_FLAGS := --quiet
SILENT_ZARF_FLAGS := --no-progress -l warn --no-color
MAX_JOBS := 4
######################################################################################


gen-python: ## Generate the protobufs for the OpenAI typing within the leapfrogai_api module
	python3 -m grpc_tools.protoc -I src/leapfrogai_sdk/proto \
			--pyi_out=src/. \
			--python_out=src/. \
			--grpc_python_out=src/. \
			src/leapfrogai_sdk/proto/leapfrogai_sdk/**/*.proto

# Clean up: Stop and remove the local registry
clean-registry:
	@echo "Cleaning up..."
	@docker stop ${REG_NAME}
	@docker rm ${REG_NAME}

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
