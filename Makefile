build: api embeddings

.PHONY: api embeddings push

push:
	docker push ghcr.io/defenseunicorns/leapfrogai/api:0.0.1
	docker push ghcr.io/defenseunicorns/leapfrogai/stablelm-3b:0.0.1
	docker push ghcr.io/defenseunicorns/leapfrogai/embeddings:0.0.1

api:
	cd api && \
	docker build --network=host -t ghcr.io/defenseunicorns/leapfrogai/api:0.0.1 .

stablelm:
	cd llms/stablelm && \
	docker build --network=host -t ghcr.io/defenseunicorns/leapfrogai/stablelm-3b:0.0.1 .

embeddings:
	cd embeddings && \
	docker build --network=host -t ghcr.io/defenseunicorns/leapfrogai/embeddings:0.0.1 .

whisper:
	cd models/whisper && \
	docker build --network=host -t ghcr.io/defenseunicorns/leapfrogai/whisper:0.0.1 .

whisper-push:
	docker push ghcr.io/defenseunicorns/leapfrogai/whisper:0.0.1

# This thing is massive, so directly pushing to the zarf registry is quicker/easier
zarf-push-api:
	docker tag ghcr.io/defenseunicorns/leapfrogai/api:0.0.1 localhost:5001/defenseunicorns/leapfrogai/api:0.0.1-zarf-1702594131
	docker push localhost:5001/defenseunicorns/leapfrogai/api:0.0.1-zarf-1702594131


zarf-port-forward:
	kubectl port-forward -n zarf svc/zarf-docker-registry 5001:5000


gen:
	python -m grpc_tools.protoc --proto_path=proto/ generate/generate.proto --python_out=llms/leapfrog  --pyi_out=llms/leapfrog --grpc_python_out=llms/leapfrog
	python -m grpc_tools.protoc --proto_path=proto audio/audio.proto --python_out=llms/leapfrog  --pyi_out=llms/leapfrog --grpc_python_out=llms/leapfrog
	python -m grpc_tools.protoc --proto_path=proto embeddings/embeddings.proto --python_out=llms/leapfrog  --pyi_out=llms/leapfrog --grpc_python_out=llms/leapfrog
	python -m grpc_tools.protoc --proto_path=proto name/name.proto --python_out=llms/leapfrog  --pyi_out=llms/leapfrog --grpc_python_out=llms/leapfrog
	