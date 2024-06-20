
test-api-integration:
	pytest tests/integration/api

test-unit:
	PYTHONPATH=$$(pwd) pytest tests/unit