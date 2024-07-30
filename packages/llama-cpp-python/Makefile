MAKEFILE_DIR := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
PORT := 50051

install-llama-cpp-python:
	@cd ${MAKEFILE_DIR} && \
	python -m pip install ../../src/leapfrogai_sdk
	@cd ${MAKEFILE_DIR} && \
	python -m pip install ".[dev]"

setup-llama-cpp-python-model:
	@cd ${MAKEFILE_DIR} && \
	rm -rf .model && mkdir .model
	@cd ${MAKEFILE_DIR} && \
	python scripts/model_download.py
	@cd ${MAKEFILE_DIR} && \
	mv .model/*.gguf .model/model.gguf

dev-run-llama-cpp-python:
	@cd ${MAKEFILE_DIR} && \
	python -m leapfrogai_sdk.cli --app-dir=. main:Model --port=${PORT}
