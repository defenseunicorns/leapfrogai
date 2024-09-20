ARCH ?= amd64
LOCAL_VERSION ?= $(shell git rev-parse --short HEAD)
DOCKER_FLAGS :=

install:
	python -m pip install ../../src/leapfrogai_sdk
	python -m pip install -e ".[dev]"

download:
	@env $$(cat .env | xargs) python src/model_download.py

dev: download
	@env $$(cat .env | xargs) python -m leapfrogai_sdk.cli --app-dir=src/ main:Model

docker: download
	docker build ${DOCKER_FLAGS} \
		--platform=linux/${ARCH} \
		--build-arg LOCAL_VERSION=${LOCAL_VERSION} \
		-t ghcr.io/defenseunicorns/leapfrogai/vllm:${LOCAL_VERSION} \
		-f packages/vllm/Dockerfile .

	docker run -it --rm \
		--env-file ./.env \
		-v $(PWD)/config.yaml:/home/leapfrogai/config.yaml \
		-v $(PWD)/.model:/home/leapfrogai/.model \
		ghcr.io/defenseunicorns/leapfrogai/vllm:${LOCAL_VERSION}
