install:
	python -m pip install build/leapfrogai_api*.whl --no-index --find-links=build/
	python -m pip install -e .

dev:
	make install
	python -m build/leapfrog_sdk.cli --app-dir=src/ main:Model
