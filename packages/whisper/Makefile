install:
	python -m pip install ../../src/leapfrogai_sdk
	python -m pip install -e ".[dev]"

dev:
	make install
	python -m leapfrogai_sdk.cli --app-dir=src/ main:Model
