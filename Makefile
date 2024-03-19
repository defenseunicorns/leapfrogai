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
	-rm -rf build
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


build-api: local-registry build-wheel ## Build the leapfrogai_api container and Zarf package
	cp build/leapfrogai_api-*.whl packages/api/
	docker build -t ghcr.io/defenseunicorns/leapfrogai/api:${LOCAL_VERSION} packages/api
	docker tag ghcr.io/defenseunicorns/leapfrogai/api:${LOCAL_VERSION} localhost:5000/defenseunicorns/leapfrogai/api:${LOCAL_VERSION}
	docker push localhost:5000/defenseunicorns/leapfrogai/api:${LOCAL_VERSION}
	zarf package create packages/api --registry-override=ghcr.io=localhost:5000 --insecure --set LEAPFROGAI_IMAGE_VERSION=${LOCAL_VERSION} --confirm
