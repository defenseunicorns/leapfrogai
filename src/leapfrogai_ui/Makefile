VERSION ?= $(shell git fetch --tags && git tag -l "*.*.*" | sort -V | tail -n 1 | sed -e 's/^v//')

docker-build:
	docker build -t ghcr.io/defenseunicorns/leapfrogai/leapfrogai-ui:${VERSION} .

zarf-build:
	zarf package create . --confirm --set IMAGE_VERSION=${VERSION}