test-api-integration:
	pytest tests/integration/api

test-unit:
	PYTHONPATH=$$(pwd) pytest tests/unit

test-e2e:
	pytest tests/e2e
