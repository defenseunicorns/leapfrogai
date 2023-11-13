TAG ?= 0.3.2
requirements:
	pip-compile -o requirements.txt pyproject.toml

gen: gen-python

gen-python:
	python3 -m grpc_tools.protoc -I proto --pyi_out=src/. --python_out=src/. --grpc_python_out=src/. proto/leapfrogai/**/*.proto

test:
	pytest -v