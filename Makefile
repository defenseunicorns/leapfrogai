ARCH ?= amd64
KEY ?= ""
REG_PORT ?= 5000

VERSION ?= $(shell git describe --abbrev=0 --tags)
LOCAL_VERSION ?= $(shell git rev-parse --short HEAD)

SDK_SRC = src/leapfrogai_sdk
SDK_DEST = src/leapfrogai_sdk/build

######################################################################################

.PHONY: help
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
	find . -name '*.whl' -delete
	find . -name '*.egg-info' -type d -exec rm -rf {} +

gen-python: ## Generate the protobufs for the OpenAI typing within the leapfrogai_api module
	python3 -m grpc_tools.protoc -I src/leapfrogai_sdk/proto \
			--pyi_out=src/. \
			--python_out=src/. \
			--grpc_python_out=src/. \
			src/leapfrogai_sdk/proto/leapfrogai_sdk/**/*.proto

local-registry: ## Start up a local container registry. Errors in this target are ignored.
	-docker run -d -p ${REG_PORT}:5000 --restart=always --name registry registry:2

sdk-wheel: ## build wheels for the leapfrogai_sdk package as a dependency for other lfai components
	-mkdir -p ${PKG_DEST}/${SDK_SRC}
	-rm -rf ${PKG_DEST}/${SDK_SRC}
	cp -r ${SDK_SRC} ${PKG_DEST}/${SDK_SRC}

setup-package: sdk-wheel
	-mkdir -p ${PKG_DEST}/src

	-rm ${PKG_DEST}/build/*.whl
	-rm ${PKG_DEST}/*.tar.zst

setup-api-deps: PKG_DEST = packages/api
setup-api-deps: setup-package ## Download the wheels for the leapfrogai_api dependencies
	-rm -rf ${PKG_DEST}/src/leapfrogai_api
	cp -r "src/leapfrogai_api" "${PKG_DEST}/src/leapfrogai_api"

	-rm ${PKG_DEST}/build/*.whl

build-api: local-registry setup-api-deps ## Build the leapfrogai_api container and Zarf package
	## Build the image (and tag it for the local registry)
	docker build --platform=linux/${ARCH} -t ghcr.io/defenseunicorns/leapfrogai/leapfrogai-api:${LOCAL_VERSION} packages/api --build-arg ARCH=${ARCH} --build-arg SDK_SRC=${SDK_SRC}
	docker tag ghcr.io/defenseunicorns/leapfrogai/leapfrogai-api:${LOCAL_VERSION} localhost:${REG_PORT}/defenseunicorns/leapfrogai/leapfrogai-api:${LOCAL_VERSION}

	## Push the image to the local registry (Zarf is super slow if the image is only in the local daemon)
	docker push localhost:${REG_PORT}/defenseunicorns/leapfrogai/leapfrogai-api:${LOCAL_VERSION}

	## Build the Zarf package
	uds zarf package create packages/api -o packages/api --registry-override=ghcr.io=localhost:${REG_PORT} --insecure --set LEAPFROGAI_IMAGE_VERSION=${LOCAL_VERSION} --confirm

build-ui: local-registry ## Build the leapfrogai_ui container and Zarf package
	## Build the image (and tag it for the local registry)
	docker build --platform=linux/${ARCH} -t ghcr.io/defenseunicorns/leapfrogai/leapfrogai-ui:${LOCAL_VERSION} src/leapfrogai_ui --build-arg ARCH=${ARCH}
	docker tag ghcr.io/defenseunicorns/leapfrogai/leapfrogai-ui:${LOCAL_VERSION} localhost:${REG_PORT}/defenseunicorns/leapfrogai/leapfrogai-ui:${LOCAL_VERSION}

	## Push the image to the local registry (Zarf is super slow if the image is only in the local daemon)
	docker push localhost:${REG_PORT}/defenseunicorns/leapfrogai/leapfrogai-ui:${LOCAL_VERSION}

	## Build the Zarf package
	uds zarf package create packages/ui -o packages/ui --registry-override=ghcr.io=localhost:${REG_PORT} --insecure --set IMAGE_VERSION=${LOCAL_VERSION} --confirm

build-llama-cpp-python: PKG_DEST = packages/llama-cpp-python
build-llama-cpp-python: local-registry setup-package ## Build the llama-cpp-python (cpu) container and Zarf package
	## Build the image (and tag it for the local registry)
	docker build --platform=linux/${ARCH} -t ghcr.io/defenseunicorns/leapfrogai/llama-cpp-python:${LOCAL_VERSION} packages/llama-cpp-python --build-arg ARCH=${ARCH}
	docker tag ghcr.io/defenseunicorns/leapfrogai/llama-cpp-python:${LOCAL_VERSION} localhost:${REG_PORT}/defenseunicorns/leapfrogai/llama-cpp-python:${LOCAL_VERSION}

	## Push the image to the local registry (Zarf is super slow if the image is only in the local daemon)
	docker push localhost:${REG_PORT}/defenseunicorns/leapfrogai/llama-cpp-python:${LOCAL_VERSION}

	## Build the Zarf package
	uds zarf package create packages/llama-cpp-python -o packages/llama-cpp-python --registry-override=ghcr.io=localhost:${REG_PORT} --insecure --set IMAGE_VERSION=${LOCAL_VERSION} --confirm

setup-vllm-deps: sdk-wheel ## Download the wheels for the optional 'vllm' dependencies
	-rm packages/vllm/build/*.whl
	python -m pip wheel packages/vllm -w packages/vllm/build --find-links=${SDK_DEST}

build-vllm: local-registry setup-vllm-deps ## Build the vllm container and Zarf package
	## Build the image (and tag it for the local registry)
	docker build -t ghcr.io/defenseunicorns/leapfrogai/vllm:${LOCAL_VERSION} packages/vllm --build-arg ARCH=${ARCH}
	docker tag ghcr.io/defenseunicorns/leapfrogai/vllm:${LOCAL_VERSION} localhost:${REG_PORT}/defenseunicorns/leapfrogai/vllm:${LOCAL_VERSION}

	## Push the image to the local registry (Zarf is super slow if the image is only in the local daemon)
	docker push localhost:${REG_PORT}/defenseunicorns/leapfrogai/vllm:${LOCAL_VERSION}

	## Build the Zarf package
	uds zarf package create packages/vllm -o packages/vllm --registry-override=ghcr.io=localhost:${REG_PORT} --insecure --set IMAGE_VERSION=${LOCAL_VERSION} --confirm

build-text-embeddings: PKG_DEST = packages/text-embeddings
build-text-embeddings: local-registry setup-package ## Build the text-embeddings container and Zarf package
	## Build the image (and tag it for the local registry)
	docker build --platform=linux/${ARCH} -t ghcr.io/defenseunicorns/leapfrogai/text-embeddings:${LOCAL_VERSION} packages/text-embeddings --build-arg ARCH=${ARCH}
	docker tag ghcr.io/defenseunicorns/leapfrogai/text-embeddings:${LOCAL_VERSION} localhost:${REG_PORT}/defenseunicorns/leapfrogai/text-embeddings:${LOCAL_VERSION}

	## Push the image to the local registry (Zarf is super slow if the image is only in the local daemon)
	docker push localhost:${REG_PORT}/defenseunicorns/leapfrogai/text-embeddings:${LOCAL_VERSION}

	## Build the Zarf package
	uds zarf package create packages/text-embeddings -o packages/text-embeddings --registry-override=ghcr.io=localhost:${REG_PORT} --insecure --set IMAGE_VERSION=${LOCAL_VERSION} --confirm

build-whisper: PKG_DEST = packages/whisper
build-whisper: local-registry setup-package ## Build the whisper container and zarf package
	## Build the image (and tag it for the local registry)
	docker build --platform=linux/${ARCH} -t ghcr.io/defenseunicorns/leapfrogai/whisper:${LOCAL_VERSION} packages/whisper --build-arg ARCH=${ARCH}
	docker tag ghcr.io/defenseunicorns/leapfrogai/whisper:${LOCAL_VERSION} localhost:${REG_PORT}/defenseunicorns/leapfrogai/whisper:${LOCAL_VERSION}

	## Push the image to the local registry (Zarf is super slow if the image is only in the local daemon)
	docker push localhost:${REG_PORT}/defenseunicorns/leapfrogai/whisper:${LOCAL_VERSION}

	## Build the Zarf package
	uds zarf package create packages/whisper -o packages/whisper --registry-override=ghcr.io=localhost:${REG_PORT} --insecure --set IMAGE_VERSION=${LOCAL_VERSION} --confirm

build-repeater: PKG_DEST = packages/repeater
build-repeater: local-registry setup-package ## Build the repeater container and zarf package
	## Build the image (and tag it for the local registry)
	docker build --platform=linux/${ARCH} -t ghcr.io/defenseunicorns/leapfrogai/repeater:${LOCAL_VERSION} packages/repeater --build-arg ARCH=${ARCH}
	docker tag ghcr.io/defenseunicorns/leapfrogai/repeater:${LOCAL_VERSION} localhost:${REG_PORT}/defenseunicorns/leapfrogai/repeater:${LOCAL_VERSION}

	## Push the image to the local registry (Zarf is super slow if the image is only in the local daemon)
	docker push localhost:${REG_PORT}/defenseunicorns/leapfrogai/repeater:${LOCAL_VERSION}

	## Build the Zarf package
	uds zarf package create packages/repeater -o packages/repeater --registry-override=ghcr.io=localhost:${REG_PORT} --insecure --set IMAGE_VERSION=${LOCAL_VERSION} --confirm

build-cpu: build-api build-llama-cpp-python build-text-embeddings build-whisper ## Build all zarf packages for a cpu-enabled deployment of LFAI

build-gpu: build-api build-vllm build-text-embeddings build-whisper ## Build all zarf packages for a gpu-enabled deployment of LFAI

build-all: build-api build-llama-cpp-python build-vllm build-text-embeddings build-whisper build-repeater ## Build all of the LFAI packages
