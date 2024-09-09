install:
	python -m pip install ../../src/leapfrogai_sdk
	python -m pip install -e ".[dev]"

download:
	@env $$(cat .env | xargs) python src/model_download.py

dev: download
	@env $$(cat .env | xargs) python -m leapfrogai_sdk.cli --app-dir=src/ main:Model
