install:
	python -m pip install build/lfai_vllm*.whl --no-index --find-links=build/
	python -m pip install -e .

dev:
	make install
	python -m leapfrogai_sdk.cli --app-dir=src/ main:Model
