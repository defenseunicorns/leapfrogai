MODEL_NAME ?= openai/whisper-base

install:
	python -m pip install ../../src/leapfrogai_sdk
	python -m pip install -e ".[dev]"

download-model:
	mkdir -p .model
	ct2-transformers-converter --model $(MODEL_NAME) \
		--output_dir .model \
		--copy_files tokenizer.json special_tokens_map.json preprocessor_config.json normalizer.json tokenizer_config.json vocab.json \
		--quantization float32 \
		--force

dev:
	make install
	python -m leapfrogai_sdk.cli --app-dir=src/ main:Model
