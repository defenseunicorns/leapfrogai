build: api embeddings

TAG ?= 0.0.4 # want to keep things all aligned here

.PHONY: api embeddings push

build: api stablelm stablelm-7b embeddings whisper

push:
	
	docker push ghcr.io/defenseunicorns/leapfrogai/stablelm-3b:${TAG}
	docker push ghcr.io/defenseunicorns/leapfrogai/embeddings:${TAG}

api:
	docker build --network=host -t ghcr.io/defenseunicorns/leapfrogai/api:${TAG} .
api-push:
	docker push ghcr.io/defenseunicorns/leapfrogai/api:${TAG}

stablelm:
	cd llms/stablelm && \
	docker build --network=host -t ghcr.io/defenseunicorns/leapfrogai/stablelm-3b:${TAG} .

embeddings:
	cd embeddings && \
	docker build --network=host -t ghcr.io/defenseunicorns/leapfrogai/embeddings:${TAG} .

whisper:
	cd models/whisper && \
	docker build --network=host -t ghcr.io/defenseunicorns/leapfrogai/whisper:${TAG} .

whisper-push:
	docker push ghcr.io/defenseunicorns/leapfrogai/whisper:${TAG}

repeater:
	cd models/test/repeater && \
	docker build --network=host -t ghcr.io/defenseunicorns/leapfrogai/repeater:${TAG} .

repeater-push:
	docker push ghcr.io/defenseunicorns/leapfrogai/repeater:${TAG}

# This thing is massive, so directly pushing to the zarf registry is quicker/easier
zarf-push-api:
	docker tag ghcr.io/defenseunicorns/leapfrogai/api:0.0.1 localhost:5001/defenseunicorns/leapfrogai/api:0.0.1-zarf-1702594131
	docker push localhost:5001/defenseunicorns/leapfrogai/api:0.0.1-zarf-1702594131


zarf-port-forward:
	kubectl port-forward -n zarf svc/zarf-docker-registry 5001:5000


gen: gen-go gen-python


gen-python:
	python3 -m grpc_tools.protoc --proto_path=proto/ generate/generate.proto --python_out=leapfrog  --pyi_out=leapfrog --grpc_python_out=leapfrog
	python3 -m grpc_tools.protoc --proto_path=proto audio/audio.proto --python_out=leapfrog  --pyi_out=leapfrog --grpc_python_out=leapfrog
	python3 -m grpc_tools.protoc --proto_path=proto embeddings/embeddings.proto --python_out=leapfrog  --pyi_out=leapfrog --grpc_python_out=leapfrog
	python3 -m grpc_tools.protoc --proto_path=proto name/name.proto --python_out=leapfrog  --pyi_out=leapfrog --grpc_python_out=leapfrog


gen-go:
	rm -rf pkg/client
	mkdir -p pkg/client
	protoc --go_out=pkg/client --go_opt=paths=source_relative --go-grpc_out=pkg/client --go-grpc_opt=paths=source_relative --proto_path=proto/ generate/generate.proto
	protoc --go_out=pkg/client --go_opt=paths=source_relative --go-grpc_out=pkg/client --go-grpc_opt=paths=source_relative --proto_path=proto/ audio/audio.proto
	protoc --go_out=pkg/client --go_opt=paths=source_relative --go-grpc_out=pkg/client --go-grpc_opt=paths=source_relative --proto_path=proto/ name/name.proto
	protoc --go_out=pkg/client --go_opt=paths=source_relative --go-grpc_out=pkg/client --go-grpc_opt=paths=source_relative --proto_path=proto/ embeddings/embeddings.proto

