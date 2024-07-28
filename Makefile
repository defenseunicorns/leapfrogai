ARCH ?= amd64
REG_PORT ?= 5000
REG_NAME ?= registry
LOCAL_VERSION ?= $(shell git rev-parse --short HEAD)
DOCKER_FLAGS :=
ZARF_FLAGS :=
SILENT_DOCKER_FLAGS := --quiet
SILENT_ZARF_FLAGS := --no-progress -l warn --no-color
MAX_JOBS := 4
######################################################################################

.PHONY: help silent-flags
help: ## Display this help information
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| sort | awk 'BEGIN {FS = ":.*?## "}; \
		{printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

clean: ## Clean up all the things (packages, build dirs, compiled .whl files, python eggs)
	-rm zarf-package-*.tar.zst
	-rm packages/**/zarf-package-*.tar.zst
	-rm -rf build/*
	-rm -rf src/**/build/*
	-rm -rf packages/**/build/*
	find . -name 'uds-bundle-*-*.tar.zst' -delete
	find . -type d -name 'zarf-sbom' -exec rm -rf {} +
	find . -name '*.whl' -delete
	find . -type d -name '*.egg-info' -exec rm -rf {} +


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
	uds zarf package create packages/supabase -a ${ARCH} -o packages/supabase --registry-override=ghcr.io=localhost:${REG_PORT} --set IMAGE_VERSION=${LOCAL_VERSION} ${ZARF_FLAGS} --confirm

docker-api: local-registry sdk-wheel
	@echo $(DOCKER_FLAGS)
	@echo $(ZARF_FLAGS)
	## Build the API image (and tag it for the local registry)
	docker build ${DOCKER_FLAGS} --platform=linux/${ARCH} --build-arg LOCAL_VERSION=${LOCAL_VERSION} -t ghcr.io/defenseunicorns/leapfrogai/leapfrogai-api:${LOCAL_VERSION} -f packages/api/Dockerfile .
	docker tag ghcr.io/defenseunicorns/leapfrogai/leapfrogai-api:${LOCAL_VERSION} localhost:${REG_PORT}/defenseunicorns/leapfrogai/leapfrogai-api:${LOCAL_VERSION}

	## Build the migration container for this version of the API
	docker build ${DOCKER_FLAGS} --platform=linux/${ARCH} -t ghcr.io/defenseunicorns/leapfrogai/api-migrations:${LOCAL_VERSION} -f Dockerfile.migrations --build-arg="MIGRATIONS_DIR=packages/api/supabase/migrations" .
	docker tag ghcr.io/defenseunicorns/leapfrogai/api-migrations:${LOCAL_VERSION} localhost:${REG_PORT}/defenseunicorns/leapfrogai/api-migrations:${LOCAL_VERSION}

build-api: local-registry docker-api ## Build the leapfrogai_api container and Zarf package
	## Push the images to the local registry (Zarf is super slow if the image is only in the local daemon)
	docker push ${DOCKER_FLAGS} localhost:${REG_PORT}/defenseunicorns/leapfrogai/leapfrogai-api:${LOCAL_VERSION}
	docker push ${DOCKER_FLAGS} localhost:${REG_PORT}/defenseunicorns/leapfrogai/api-migrations:${LOCAL_VERSION}

	## Build the Zarf package
	uds zarf package create packages/api -a ${ARCH} -o packages/api --registry-override=ghcr.io=localhost:${REG_PORT} --insecure --set LEAPFROGAI_IMAGE_VERSION=${LOCAL_VERSION} ${ZARF_FLAGS} --confirm

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
	uds zarf package create packages/ui -a ${ARCH} -o packages/ui --registry-override=ghcr.io=localhost:${REG_PORT} --insecure --set IMAGE_VERSION=${LOCAL_VERSION} ${ZARF_FLAGS} --confirm

docker-llama-cpp-python: sdk-wheel
	## Build the image (and tag it for the local registry)
	docker build ${DOCKER_FLAGS} --platform=linux/${ARCH} --build-arg LOCAL_VERSION=${LOCAL_VERSION} -t ghcr.io/defenseunicorns/leapfrogai/llama-cpp-python:${LOCAL_VERSION} -f packages/llama-cpp-python/Dockerfile .
	docker tag ghcr.io/defenseunicorns/leapfrogai/llama-cpp-python:${LOCAL_VERSION} localhost:${REG_PORT}/defenseunicorns/leapfrogai/llama-cpp-python:${LOCAL_VERSION}

build-llama-cpp-python: local-registry docker-llama-cpp-python ## Build the llama-cpp-python (cpu) container and Zarf package
	## Push the image to the local registry (Zarf is super slow if the image is only in the local daemon)
	docker push ${DOCKER_FLAGS} localhost:${REG_PORT}/defenseunicorns/leapfrogai/llama-cpp-python:${LOCAL_VERSION}

	## Build the Zarf package
	uds zarf package create packages/llama-cpp-python -a ${ARCH} -o packages/llama-cpp-python --registry-override=ghcr.io=localhost:${REG_PORT} --insecure --set IMAGE_VERSION=${LOCAL_VERSION} ${ZARF_FLAGS} --confirm

docker-vllm: sdk-wheel
	## Build the image (and tag it for the local registry)
	docker build ${DOCKER_FLAGS} --platform=linux/${ARCH} --build-arg LOCAL_VERSION=${LOCAL_VERSION} -t ghcr.io/defenseunicorns/leapfrogai/vllm:${LOCAL_VERSION} -f packages/vllm/Dockerfile .
	docker tag ghcr.io/defenseunicorns/leapfrogai/vllm:${LOCAL_VERSION} localhost:${REG_PORT}/defenseunicorns/leapfrogai/vllm:${LOCAL_VERSION}

build-vllm: local-registry docker-vllm ## Build the vllm container and Zarf package
	## Push the image to the local registry (Zarf is super slow if the image is only in the local daemon)
	docker push ${DOCKER_FLAGS} localhost:${REG_PORT}/defenseunicorns/leapfrogai/vllm:${LOCAL_VERSION}

	## Build the Zarf package
	uds zarf package create packages/vllm -a ${ARCH} -o packages/vllm --registry-override=ghcr.io=localhost:${REG_PORT} --insecure --set IMAGE_VERSION=${LOCAL_VERSION} ${ZARF_FLAGS} --confirm

docker-text-embeddings: sdk-wheel
	## Build the image (and tag it for the local registry)
	docker build ${DOCKER_FLAGS} --platform=linux/${ARCH} --build-arg LOCAL_VERSION=${LOCAL_VERSION} -t ghcr.io/defenseunicorns/leapfrogai/text-embeddings:${LOCAL_VERSION} -f packages/text-embeddings/Dockerfile .
	docker tag ghcr.io/defenseunicorns/leapfrogai/text-embeddings:${LOCAL_VERSION} localhost:${REG_PORT}/defenseunicorns/leapfrogai/text-embeddings:${LOCAL_VERSION}

build-text-embeddings: local-registry docker-text-embeddings ## Build the text-embeddings container and Zarf package
	## Push the image to the local registry (Zarf is super slow if the image is only in the local daemon)
	docker push ${DOCKER_FLAGS} localhost:${REG_PORT}/defenseunicorns/leapfrogai/text-embeddings:${LOCAL_VERSION}

	## Build the Zarf package
	uds zarf package create packages/text-embeddings -a ${ARCH} -o packages/text-embeddings --registry-override=ghcr.io=localhost:${REG_PORT} --insecure --set IMAGE_VERSION=${LOCAL_VERSION} ${ZARF_FLAGS} --confirm


docker-whisper: sdk-wheel
	## Build the image (and tag it for the local registry)
	docker build ${DOCKER_FLAGS} --platform=linux/${ARCH} --build-arg LOCAL_VERSION=${LOCAL_VERSION} -t ghcr.io/defenseunicorns/leapfrogai/whisper:${LOCAL_VERSION} -f packages/whisper/Dockerfile .
	docker tag ghcr.io/defenseunicorns/leapfrogai/whisper:${LOCAL_VERSION} localhost:${REG_PORT}/defenseunicorns/leapfrogai/whisper:${LOCAL_VERSION}

build-whisper: local-registry docker-whisper ## Build the whisper container and zarf package
	## Push the image to the local registry (Zarf is super slow if the image is only in the local daemon)
	docker push ${DOCKER_FLAGS} localhost:${REG_PORT}/defenseunicorns/leapfrogai/whisper:${LOCAL_VERSION}

	## Build the Zarf package
	uds zarf package create packages/whisper -a ${ARCH} -o packages/whisper --registry-override=ghcr.io=localhost:${REG_PORT} --insecure --set IMAGE_VERSION=${LOCAL_VERSION} ${ZARF_FLAGS} --confirm

docker-repeater: sdk-wheel
	## Build the image (and tag it for the local registry)
	docker build ${DOCKER_FLAGS} --platform=linux/${ARCH} --build-arg LOCAL_VERSION=${LOCAL_VERSION} -t ghcr.io/defenseunicorns/leapfrogai/repeater:${LOCAL_VERSION} -f packages/repeater/Dockerfile .
	docker tag ghcr.io/defenseunicorns/leapfrogai/repeater:${LOCAL_VERSION} localhost:${REG_PORT}/defenseunicorns/leapfrogai/repeater:${LOCAL_VERSION}

build-repeater: local-registry docker-repeater ## Build the repeater container and zarf package
	## Push the image to the local registry (Zarf is super slow if the image is only in the local daemon)
	docker push ${DOCKER_FLAGS} localhost:${REG_PORT}/defenseunicorns/leapfrogai/repeater:${LOCAL_VERSION}

	## Build the Zarf package
	uds zarf package create packages/repeater -a ${ARCH} -o packages/repeater --registry-override=ghcr.io=localhost:${REG_PORT} --insecure --set IMAGE_VERSION=${LOCAL_VERSION} ${ZARF_FLAGS} --confirm

build-cpu: build-supabase build-api build-ui build-llama-cpp-python build-text-embeddings build-whisper ## Build all zarf packages for a cpu-enabled deployment of LFAI

build-gpu: build-supabase build-api build-ui build-vllm build-text-embeddings build-whisper ## Build all zarf packages for a gpu-enabled deployment of LFAI

build-all: build-cpu build-gpu ## Build all of the LFAI packages

include tests/make-tests.mk

include packages/k3d-gpu/Makefile

silent-build-api-parallel:
	@echo "API build started"
	@touch .build/api.log
	@$(MAKE) build-api DOCKER_FLAGS="$(DOCKER_FLAGS) $(SILENT_DOCKER_FLAGS)" ZARF_FLAGS="$(ZARF_FLAGS) $(SILENT_ZARF_FLAGS)" > .build/api.log 2>&1
	@echo "API build completed"

silent-build-supabase-parallel:
	@echo "Supabase build started"
	@touch .build/supabase.log
	@$(MAKE) build-supabase DOCKER_FLAGS="$(DOCKER_FLAGS) $(SILENT_DOCKER_FLAGS)" ZARF_FLAGS="$(ZARF_FLAGS) $(SILENT_ZARF_FLAGS)" > .build/supabase.log 2>&1
	@echo "Supabase build completed"

silent-build-ui-parallel:
	@echo "UI build started"
	@touch .build/ui.log
	@$(MAKE) build-ui DOCKER_FLAGS="$(DOCKER_FLAGS) $(SILENT_DOCKER_FLAGS)" ZARF_FLAGS="$(ZARF_FLAGS) $(SILENT_ZARF_FLAGS)" > .build/ui.log 2>&1
	@echo "UI build completed"

silent-build-vllm-parallel:
	@echo "VLLM build started"
	@touch .build/vllm.log
	@$(MAKE) build-vllm DOCKER_FLAGS="$(DOCKER_FLAGS) $(SILENT_DOCKER_FLAGS)" ZARF_FLAGS="$(ZARF_FLAGS) $(SILENT_ZARF_FLAGS)" > .build/vllm.log 2>&1
	@echo "VLLM build completed"

silent-build-llama-cpp-python-parallel:
	@echo "llama-cpp-python build started"
	@touch .build/llama-cpp-python.log
	@$(MAKE) build-llama-cpp-python DOCKER_FLAGS="$(DOCKER_FLAGS) $(SILENT_DOCKER_FLAGS)" ZARF_FLAGS="$(ZARF_FLAGS) $(SILENT_ZARF_FLAGS)" > .build/llama-cpp-python.log 2>&1
	@echo "llama-cpp-python build completed"

silent-build-text-embeddings-parallel:
	@echo "text-embeddings build started"
	@touch .build/text-embeddings.log
	@$(MAKE) build-text-embeddings DOCKER_FLAGS="$(DOCKER_FLAGS) $(SILENT_DOCKER_FLAGS)" ZARF_FLAGS="$(ZARF_FLAGS) $(SILENT_ZARF_FLAGS)" > .build/text-embeddings.log 2>&1
	@echo "text-embeddings build completed"

silent-build-whisper-parallel:
	@echo "whisper build started"
	@touch .build/whisper.log
	@$(MAKE) build-whisper DOCKER_FLAGS="$(DOCKER_FLAGS) $(SILENT_DOCKER_FLAGS)" ZARF_FLAGS="$(ZARF_FLAGS) $(SILENT_ZARF_FLAGS)" > .build/whisper.log 2>&1
	@echo "whisper build completed"

silent-build-all:
	@mkdir -p .build
	@echo "Starting parallel builds..."
	@echo "Logs at .build/*.log"
	@$(MAKE) -j${MAX_JOBS} silent-build-api-parallel silent-build-supabase-parallel silent-build-ui-parallel silent-build-vllm-parallel silent-build-llama-cpp-python-parallel silent-build-text-embeddings-parallel silent-build-whisper-parallel
	@echo "All builds completed"
