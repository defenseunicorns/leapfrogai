build: api embeddings

TAG ?= 0.3.3
# want to keep things all aligned here

.PHONY: api embeddings push

build: api stablelm stablelm-7b embeddings whisper

requirements:
	pip-compile -o leapfrogai/requirements.txt pyproject.toml

push:
	docker push ghcr.io/defenseunicorns/leapfrogai/stablelm-3b:${TAG}
	docker push ghcr.io/defenseunicorns/leapfrogai/all-minilm-l6-v2:${TAG}

base:
	docker build --network=host -t ghcr.io/defenseunicorns/leapfrogai/base:${TAG} -f leapfrogai/Dockerfile leapfrogai

base-push:
	docker push ghcr.io/defenseunicorns/leapfrogai/base:${TAG}

api:
	docker build --network=host -t ghcr.io/defenseunicorns/leapfrogai/api:${TAG} .
api-push:
	docker push ghcr.io/defenseunicorns/leapfrogai/api:${TAG}

stablelm: base
	cd models/llms/stablelm && \
	docker build --network=host --build-arg IMAGE_TAG=${TAG} -t ghcr.io/defenseunicorns/leapfrogai/stablelm-3b:${TAG} .

embeddings: base
	cd  models/text2vec/all-minilm-l6-v2/ && \
	docker build --network=host --build-arg IMAGE_TAG=${TAG} -t ghcr.io/defenseunicorns/leapfrogai/all-minilm-l6-v2:${TAG} .

mpt-7b-chat: base
	cd models/llms/mpt-7b-chat && \
	docker build --network=host --build-arg IMAGE_TAG=${TAG} -t ghcr.io/defenseunicorns/leapfrogai/mpt-7b-chat:${TAG} .


whisper: base
	cd models/speech2text/whisper && \
	docker build --network=host --build-arg IMAGE_TAG=${TAG} -t ghcr.io/defenseunicorns/leapfrogai/whisper:${TAG} .

whisper-push:
	docker push ghcr.io/defenseunicorns/leapfrogai/whisper:${TAG}

repeater: base
	cd models/test/repeater && \
	docker build --network=host --build-arg IMAGE_TAG=${TAG} -t ghcr.io/defenseunicorns/leapfrogai/repeater:${TAG} .

repeater-push:
	docker push ghcr.io/defenseunicorns/leapfrogai/repeater:${TAG}


zarf-port-forward:
	kubectl port-forward -n zarf svc/zarf-docker-registry 5001:5000


gen: gen-go gen-python


gen-python:
	python3 -m grpc_tools.protoc --proto_path=proto chat/chat.proto --python_out=leapfrogai  --pyi_out=leapfrogai --grpc_python_out=leapfrogai
	python3 -m grpc_tools.protoc --proto_path=proto completion/completion.proto --python_out=leapfrogai  --pyi_out=leapfrogai --grpc_python_out=leapfrogai
	python3 -m grpc_tools.protoc --proto_path=proto audio/audio.proto --python_out=leapfrogai  --pyi_out=leapfrogai --grpc_python_out=leapfrogai
	python3 -m grpc_tools.protoc --proto_path=proto embeddings/embeddings.proto --python_out=leapfrogai  --pyi_out=leapfrogai --grpc_python_out=leapfrogai
	python3 -m grpc_tools.protoc --proto_path=proto name/name.proto --python_out=leapfrogai  --pyi_out=leapfrogai --grpc_python_out=leapfrogai


gen-go:
	rm -rf pkg/client
	mkdir -p pkg/client
	protoc --go_out=pkg/client --go_opt=paths=source_relative --go-grpc_out=pkg/client --go-grpc_opt=paths=source_relative --proto_path=proto/ --experimental_allow_proto3_optional completion/completion.proto
	protoc --go_out=pkg/client --go_opt=paths=source_relative --go-grpc_out=pkg/client --go-grpc_opt=paths=source_relative --proto_path=proto/ --experimental_allow_proto3_optional chat/chat.proto
	protoc --go_out=pkg/client --go_opt=paths=source_relative --go-grpc_out=pkg/client --go-grpc_opt=paths=source_relative --proto_path=proto/ audio/audio.proto
	protoc --go_out=pkg/client --go_opt=paths=source_relative --go-grpc_out=pkg/client --go-grpc_opt=paths=source_relative --proto_path=proto/ name/name.proto
	protoc --go_out=pkg/client --go_opt=paths=source_relative --go-grpc_out=pkg/client --go-grpc_opt=paths=source_relative --proto_path=proto/ embeddings/embeddings.proto


update-embeddings: embeddings
	docker tag ghcr.io/defenseunicorns/leapfrogai/all-minilm-l6-v2:${TAG} localhost:5001/defenseunicorns/leapfrogai/embeddings:${TAG}-zarf-230844594
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

ctransformers: base
	cd models/llms/ctransformers && \
	docker build --network=host --build-arg IMAGE_TAG=${TAG} -t ghcr.io/defenseunicorns/leapfrogai/ctransformers:${TAG} .

update-ctransformers: ctransformers
	docker tag ghcr.io/defenseunicorns/leapfrogai/ctransformers:0.3.3 127.0.0.1:5001/defenseunicorns/leapfrogai/ctransformers:0.3.3-zarf-721929940
	docker push 127.0.0.1:5001/defenseunicorns/leapfrogai/ctransformers:0.3.3-zarf-721929940
	kubectl delete pods -n leapfrogai -l app.kubernetes.io/instance=mpt-30b-chat-ggml-model
	kubectl delete pods -n leapfrogai -l app.kubernetes.io/instance=mpt-30b-instruct-ggml-model

test-init:
	docker run -p 50051:50051 -d --rm --name repeater  ghcr.io/defenseunicorns/leapfrogai/repeater:${TAG}
	
test:
	PYTHONPATH="." python3 models/test/repeater/test.py
teardown:
	docker kill repeater


images: api base stablelm whisper repeater mpt-7b-chat embeddings