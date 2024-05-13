install:
	python -m pip install leapfrogai_api*.whl --no-index --find-links=build/
	python -m pip install -e .

dev:
	make install
	python -m uvicorn main:app --port 3000 --reload
