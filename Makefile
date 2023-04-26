build: api llama embeddings

.PHONY: api llama embeddings push

push:
	docker push ghcr.io/defenseunicorns/leapfrogai/api:0.0.1
	docker push ghcr.io/defenseunicorns/leapfrogai/llama:0.0.1
	docker push ghcr.io/defenseunicorns/leapfrogai/embeddings:0.0.1

api:
	cd api && \
	docker build --network=host -t ghcr.io/defenseunicorns/leapfrogai/api:0.0.1 .

llama:
	cd alpaca && \
	docker build --network=host -t ghcr.io/defenseunicorns/leapfrogai/llama:0.0.1 .

embeddings:
	cd embeddings && \
	docker build --network=host -t ghcr.io/defenseunicorns/leapfrogai/embeddings:0.0.1 .