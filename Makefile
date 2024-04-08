ARCH ?= amd64
KEY ?= ""

VERSION ?= $(shell git describe --abbrev=0 --tags)
LOCAL_VERSION ?= $(shell git rev-parse --short HEAD)
######################################################################################

.PHONY: help
help: ## Display this help information
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| sort | awk 'BEGIN {FS = ":.*?## "}; \
		{printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


clean: ## Clean up all the things (packages, build dirs, compiled .whl files, python eggs)
	-rm zarf-package-*.tar.zst
	-rm -rf build/*
	find . -name '*.whl' -delete
	find . -name '*.egg-info' -type d -exec rm -rf {} +


build-wheel: ## Build the wheel for the leapfrogai_api module
	python -m pip wheel . -w build


gen-python: ## Generate the protobufs for the OpenAI typing within the leapfrogai_api module
	python3 -m grpc_tools.protoc -I src/leapfrogai_api/types/proto \
			--pyi_out=src/. \
			--python_out=src/. \
			--grpc_python_out=src/. \
			src/leapfrogai_api/types/proto/leapfrogai_api/types/**/*.proto

local-registry: ## Start up a local container registry. Errors in this target are ignored.
	-docker run -d -p 5000:5000 --restart=always --name registry registry:2


setup-api-deps: ## Download the wheels for the leapfrogai_api dependencies
	-rm packages/api/build/*.whl
	python -m pip wheel . -w packages/api/build

build-api: local-registry setup-api-deps ## Build the leapfrogai_api container and Zarf package
	## Build the image (and tag it for the local registry)
	docker build -t ghcr.io/defenseunicorns/leapfrogai/leapfrogai-api:${LOCAL_VERSION} packages/api
	docker tag ghcr.io/defenseunicorns/leapfrogai/leapfrogai-api:${LOCAL_VERSION} localhost:5000/defenseunicorns/leapfrogai/leapfrogai-api:${LOCAL_VERSION}

	## Push the image to the local registry (Zarf is super slow if the image is only in the local daemon)
	docker push localhost:5000/defenseunicorns/leapfrogai/leapfrogai-api:${LOCAL_VERSION}

	## Build the Zarf package
	uds zarf package create packages/api -o packages/api --registry-override=ghcr.io=localhost:5000 --insecure --set LEAPFROGAI_IMAGE_VERSION=${LOCAL_VERSION} --confirm


setup-llama-cpp-python-deps:  ## Download the wheels for the optional 'llama-cpp-python' dependencies
	-rm packages/llama-cpp-python/build/*.whl
	python -m pip wheel ".[llama-cpp-python]" -w packages/llama-cpp-python/build

build-llama-cpp-python: local-registry setup-llama-cpp-python-deps ## Build the llama-cpp-python (cpu) container and Zarf package
	## Build the image (and tag it for the local registry)
	docker build -t ghcr.io/defenseunicorns/leapfrogai/llama-cpp-python:${LOCAL_VERSION} packages/llama-cpp-python
	docker tag ghcr.io/defenseunicorns/leapfrogai/llama-cpp-python:${LOCAL_VERSION} localhost:5000/defenseunicorns/leapfrogai/llama-cpp-python:${LOCAL_VERSION}

	## Push the image to the local registry (Zarf is super slow if the image is only in the local daemon)
	docker push localhost:5000/defenseunicorns/leapfrogai/llama-cpp-python:${LOCAL_VERSION}

	## Build the Zarf package
	uds zarf package create packages/llama-cpp-python -o packages/llama-cpp-python --registry-override=ghcr.io=localhost:5000 --insecure --set IMAGE_VERSION=${LOCAL_VERSION} --confirm


setup-vllm-deps: ## Download the wheels for the optional 'vllm' dependencies
	-rm packages/vllm/build/*.whl
	python -m pip wheel ".[vllm]" -w packages/vllm/build

build-vllm: local-registry setup-vllm-deps ## Build the vllm container and Zarf package
	## Build the image (and tag it for the local registry)
	docker build -t ghcr.io/defenseunicorns/leapfrogai/vllm:${LOCAL_VERSION} packages/vllm
	docker tag ghcr.io/defenseunicorns/leapfrogai/vllm:${LOCAL_VERSION} localhost:5000/defenseunicorns/leapfrogai/vllm:${LOCAL_VERSION}

	## Push the image to the local registry (Zarf is super slow if the image is only in the local daemon)
	docker push localhost:5000/defenseunicorns/leapfrogai/vllm:${LOCAL_VERSION}

	## Build the Zarf package
	uds zarf package create packages/vllm -o packages/vllm --registry-override=ghcr.io=localhost:5000 --insecure --set IMAGE_VERSION=${LOCAL_VERSION} --confirm


setup-text-embeddings-deps: ## Download the wheels for the optional 'text-embeddings' dependencies
	-rm packages/text-embeddings/build/*.whl
	python -m pip wheel ".[text-embeddings]" -w packages/text-embeddings/build

build-text-embeddings: local-registry setup-text-embeddings-deps ## Build the text-embeddings container and Zarf package
	## Build the image (and tag it for the local registry)
	docker build -t ghcr.io/defenseunicorns/leapfrogai/text-embeddings:${LOCAL_VERSION} packages/text-embeddings
	docker tag ghcr.io/defenseunicorns/leapfrogai/text-embeddings:${LOCAL_VERSION} localhost:5000/defenseunicorns/leapfrogai/text-embeddings:${LOCAL_VERSION}

	## Push the image to the local registry (Zarf is super slow if the image is only in the local daemon)
	docker push localhost:5000/defenseunicorns/leapfrogai/text-embeddings:${LOCAL_VERSION}

	## Build the Zarf package
	uds zarf package create packages/text-embeddings -o packages/text-embeddings --registry-override=ghcr.io=localhost:5000 --insecure --set IMAGE_VERSION=${LOCAL_VERSION} --confirm


setup-whisper-deps: ## Download the wheels for the optional 'whisper' dependencies
	-rm packages/whisper/build/*.whl
	python -m pip wheel ".[whisper]" -w packages/whisper/build

build-whisper: local-registry setup-whisper-deps ## Build the whisper container and zarf package
	## Build the image (and tag it for the local registry)
	docker build -t ghcr.io/defenseunicorns/leapfrogai/whisper:${LOCAL_VERSION} packages/whisper
	docker tag ghcr.io/defenseunicorns/leapfrogai/whisper:${LOCAL_VERSION} localhost:5000/defenseunicorns/leapfrogai/whisper:${LOCAL_VERSION}

	## Push the image to the local registry (Zarf is super slow if the image is only in the local daemon)
	docker push localhost:5000/defenseunicorns/leapfrogai/whisper:${LOCAL_VERSION}

	## Build the Zarf package
	uds zarf package create packages/whisper -o packages/whisper --registry-override=ghcr.io=localhost:5000 --insecure --set IMAGE_VERSION=${LOCAL_VERSION} --confirm

build-cpu: build-api build-llama-cpp-python build-text-embeddings build-whisper ## Build all zarf packages for a cpu-enabled deployment of LFAI

build-gpu: build-api build-vllm build-text-embeddings build-whisper ## Build all zarf packages for a gpu-enabled deployment of LFAI

build-all: build-api build-llama-cpp-python build-vllm build-text-embeddings build-whisper ## Build all of the LFAI packages
