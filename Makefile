TAG ?= 0.3.2
requirements:
	pip-compile -o leapfrogai/requirements.txt pyproject.toml

gen: gen-python

gen-python:
	python3 -m grpc_tools.protoc --proto_path=proto chat/chat.proto --python_out=leapfrogai  --pyi_out=leapfrogai --grpc_python_out=leapfrogai
	python3 -m grpc_tools.protoc --proto_path=proto completion/completion.proto --python_out=leapfrogai  --pyi_out=leapfrogai --grpc_python_out=leapfrogai
	python3 -m grpc_tools.protoc --proto_path=proto audio/audio.proto --python_out=leapfrogai  --pyi_out=leapfrogai --grpc_python_out=leapfrogai
	python3 -m grpc_tools.protoc --proto_path=proto embeddings/embeddings.proto --python_out=leapfrogai  --pyi_out=leapfrogai --grpc_python_out=leapfrogai
	python3 -m grpc_tools.protoc --proto_path=proto name/name.proto --python_out=leapfrogai  --pyi_out=leapfrogai --grpc_python_out=leapfrogai

test:
	pytest