install:
	python -m pip install ../../src/leapfrogai_sdk
	python -m pip install -e .

dev:
	make install
	python -m leapfrogai_sdk.cli --app-dir=. main:Model
