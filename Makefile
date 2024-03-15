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


build-wheel: ## Build the wheel for the leapfrogai_api module
	python -m pip wheel . -w build


gen-python: ## Generate the protobufs for the OpenAI typing within the leapfrogai_api module
	python3 -m grpc_tools.protoc -I src/leapfrogai_api/types/proto \
			--pyi_out=src/. \
			--python_out=src/. \
			--grpc_python_out=src/. \
			src/leapfrogai_api/types/proto/leapfrogai_api/types/**/*.proto

