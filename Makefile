build: api embeddings

TAG ?= 0.2.0
# want to keep things all aligned here

.PHONY: api embeddings push

build: api stablelm stablelm-7b embeddings whisper

requirements:
	pip-compile -o leapfrogai/requirements.txt pyproject.toml

push:
	docker push ghcr.io/defenseunicorns/leapfrogai/stablelm-3b:${TAG}
	docker push ghcr.io/defenseunicorns/leapfrogai/embeddings:${TAG}

base:
	docker build --network=host -t ghcr.io/defenseunicorns/leapfrogai/base:${TAG} -f leapfrogai/Dockerfile leapfrogai

api:
	docker build --network=host -t ghcr.io/defenseunicorns/leapfrogai/api:${TAG} .
api-push:
	docker push ghcr.io/defenseunicorns/leapfrogai/api:${TAG}

stablelm:
	cd models/llms/stablelm && \
	docker build --network=host --build-arg IMAGE_TAG=${TAG} -t ghcr.io/defenseunicorns/leapfrogai/stablelm-3b:${TAG} .

embeddings:
	cd  models/text2vec/all-minilm-l6-v2/ && \
	docker build --network=host --build-arg IMAGE_TAG=${TAG} -t ghcr.io/defenseunicorns/leapfrogai/embeddings:${TAG} .

whisper:
	cd models/speech2text/whisper && \
	docker build --network=host --build-arg IMAGE_TAG=${TAG} -t ghcr.io/defenseunicorns/leapfrogai/whisper:${TAG} .

whisper-push:
	docker push ghcr.io/defenseunicorns/leapfrogai/whisper:${TAG}

repeater:
	cd models/test/repeater && \
	docker build --network=host --build-arg IMAGE_TAG=${TAG} -t ghcr.io/defenseunicorns/leapfrogai/repeater:${TAG} .

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
	python3 -m grpc_tools.protoc --proto_path=proto/ generate/generate.proto --python_out=leapfrogai  --pyi_out=leapfrogai --grpc_python_out=leapfrogai
	python3 -m grpc_tools.protoc --proto_path=proto audio/audio.proto --python_out=leapfrogai  --pyi_out=leapfrogai --grpc_python_out=leapfrogai
	python3 -m grpc_tools.protoc --proto_path=proto embeddings/embeddings.proto --python_out=leapfrogai  --pyi_out=leapfrogai --grpc_python_out=leapfrogai
	python3 -m grpc_tools.protoc --proto_path=proto name/name.proto --python_out=leapfrogai  --pyi_out=leapfrogai --grpc_python_out=leapfrogai


gen-go:
	rm -rf pkg/client
	mkdir -p pkg/client
	protoc --go_out=pkg/client --go_opt=paths=source_relative --go-grpc_out=pkg/client --go-grpc_opt=paths=source_relative --proto_path=proto/ generate/generate.proto
	protoc --go_out=pkg/client --go_opt=paths=source_relative --go-grpc_out=pkg/client --go-grpc_opt=paths=source_relative --proto_path=proto/ audio/audio.proto
	protoc --go_out=pkg/client --go_opt=paths=source_relative --go-grpc_out=pkg/client --go-grpc_opt=paths=source_relative --proto_path=proto/ name/name.proto
	protoc --go_out=pkg/client --go_opt=paths=source_relative --go-grpc_out=pkg/client --go-grpc_opt=paths=source_relative --proto_path=proto/ embeddings/embeddings.proto


update-embeddings: embeddings
	docker tag ghcr.io/defenseunicorns/leapfrogai/embeddings:${TAG} localhost:5001/defenseunicorns/leapfrogai/embeddings:${TAG}-zarf-230844594
	docker push localhost:5001/defenseunicorns/leapfrogai/embeddings:${TAG}-zarf-230844594
	kubectl delete pods -n leapfrogai -l app=embeddings
update-api: api
	docker tag ghcr.io/defenseunicorns/leapfrogai/api:${TAG} localhost:5001/defenseunicorns/leapfrogai/api:${TAG}-zarf-1702594131
	docker push localhost:5001/defenseunicorns/leapfrogai/api:${TAG}-zarf-1702594131
	kubectl delete pods -n leapfrogai -l app=api

update-repeater: repeater
	docker tag ghcr.io/defenseunicorns/leapfrogai/repeater:${TAG} localhost:5001/defenseunicorns/leapfrogai/repeater:${TAG}-zarf-4122428005
	docker push localhost:5001/defenseunicorns/leapfrogai/repeater:${TAG}-zarf-4122428005
	kubectl delete pods -n leapfrogai -l app=repeater

update-stablelm: stablelm
	docker tag ghcr.io/defenseunicorns/leapfrogai/stablelm-3b:${TAG} localhost:5001/defenseunicorns/leapfrogai/stablelm-3b:${TAG}-zarf-1442747400
	docker push localhost:5001/defenseunicorns/leapfrogai/stablelm-3b:${TAG}-zarf-1442747400
	kubectl delete pods -n leapfrogai -l app=stablelm

test-init:
	docker run -p 50051:50051 -d --rm --name repeater  ghcr.io/defenseunicorns/leapfrogai/repeater:${TAG}
	
test:
	PYTHONPATH="." python3 models/test/repeater/test.py
teardown:
	docker kill repeater