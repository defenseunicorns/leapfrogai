build: api embeddings

TAG ?= 0.1.2 # want to keep things all aligned here

.PHONY: api embeddings push

build: api stablelm stablelm-7b embeddings whisper

push:
	docker push ghcr.io/defenseunicorns/leapfrogai/api:${TAG}
	docker push ghcr.io/defenseunicorns/leapfrogai/stablelm-3b:${TAG}
	docker push ghcr.io/defenseunicorns/leapfrogai/embeddings:${TAG}

api:
	cd api && \
	docker build --network=host -t ghcr.io/defenseunicorns/leapfrogai/api:${TAG} .

stablelm:
	cd llms/stablelm && \
	docker build --network=host -t ghcr.io/defenseunicorns/leapfrogai/stablelm-3b:${TAG} .

stablelm-7b:
	cd llms/stablelm-7b && \
	docker build --network=host -t ghcr.io/defenseunicorns/leapfrogai/stablelm-7b:${TAG} .


embeddings:
	cd embeddings && \
	docker build --network=host -t ghcr.io/defenseunicorns/leapfrogai/embeddings:${TAG} .

whisper:
	cd models/whisper && \
	docker build --network=host -t ghcr.io/defenseunicorns/leapfrogai/whisper:${TAG} .

whisper-push:
	docker push ghcr.io/defenseunicorns/leapfrogai/whisper:${TAG}

# This thing is massive, so directly pushing to the zarf registry is quicker/easier
zarf-push-api:
	docker tag ghcr.io/defenseunicorns/leapfrogai/api:0.0.1 localhost:5001/defenseunicorns/leapfrogai/api:0.0.1-zarf-1702594131
	docker push localhost:5001/defenseunicorns/leapfrogai/api:0.0.1-zarf-1702594131


zarf-port-forward:
	kubectl port-forward -n zarf svc/zarf-docker-registry 5001:5000