install:
	python -m pip install ../../src/leapfrogai_sdk
	python -m pip install -e .

dev:
	make install
	python -m uvicorn main:app --port 3000 --reload
