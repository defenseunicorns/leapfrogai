install:
	python -m pip install -e .

dev:
	make install
	python -m uvicorn main:app --port 3000 --reload

test-integration:
	cd ../../ && python -m pytest tests/integration/api
