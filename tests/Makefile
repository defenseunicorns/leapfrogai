SUPABASE_URL ?= https://supabase-kong.uds.dev
LEAPFROGAI_MODEL ?= llama-cpp-python
LFAI_RUN_NIAH_TESTS ?= false
LFAI_RUN_REPEATER_TESTS ?= true

install:
	pip install ".[dev]" "src/leapfrogai_api" "src/leapfrogai_sdk" "packages/repeater"

set-supabase:
	$(eval SUPABASE_URL := $(SUPABASE_URL))
	$(eval SUPABASE_ANON_KEY := $(shell uds zarf tools kubectl get secret -n leapfrogai supabase-bootstrap-jwt -o json | uds zarf tools yq '.data.anon-key' | base64 -d))
	$(eval SUPABASE_SERVICE_KEY := $(shell uds zarf tools kubectl get secret supabase-bootstrap-jwt -n leapfrogai -o jsonpath='{.data.service-key}' | base64 -d))

# .env file covers all possible tests use cases where the same variable is named differently
define get_jwt_token
	echo "Getting JWT token from $(3)..."; \
	echo "Email: $(1)"; \
	echo "Password: $(2)"; \
	TOKEN_RESPONSE=$$(curl -s -X POST $(3) \
	-H "apikey: $(SUPABASE_ANON_KEY)" \
	-H "Content-Type: application/json" \
	-d "{\"email\": \"$(1)\", \"password\": \"$(2)\"}"); \
	echo "Extracting token from $$TOKEN_RESPONSE"; \
	JWT=$$(echo $$TOKEN_RESPONSE | grep -o '"access_token":"[^"]*' | cut -d '"' -f 4); \
	echo "SUPABASE_USER_JWT=$$JWT" > .env; \
	echo "SUPABASE_URL=$(SUPABASE_URL)" >> .env; \
	echo "SUPABASE_ANON_KEY=$(SUPABASE_ANON_KEY)" >> .env; \
	echo "ANON_KEY=$(SUPABASE_ANON_KEY)" >> .env; \
	echo "SUPABASE_SERVICE_KEY=$(SUPABASE_SERVICE_KEY)" >> .env; \
	echo "SERVICE_KEY=$(SUPABASE_SERVICE_KEY)" >> .env; \
	echo "LEAPFROGAI_MODEL=$(LEAPFROGAI_MODEL)" >> .env; \
	echo "DONE - variables exported to .env file"
endef

prompt-email:
	@echo "Enter your email address: "; \
	read SUPABASE_EMAIL; \
	echo $$SUPABASE_EMAIL > .env.email

prompt-password:
	@echo "Enter your DEV API password: "; \
	read SUPABASE_PASS; \
	echo $$SUPABASE_PASS > .env.password

test-user: set-supabase prompt-email prompt-password
	SUPABASE_EMAIL=$$(cat .env.email | tr -d '\n'); \
	SUPABASE_PASS=$$(cat .env.password | tr -d '\n'); \
	$(call get_jwt_token,$$SUPABASE_EMAIL,$$SUPABASE_PASS,"$(SUPABASE_URL)/auth/v1/signup")

# Setup for pipeline tests with no interactive terminal
test-user-pipeline: set-supabase
	$(call get_jwt_token,$(SUPABASE_EMAIL),$(SUPABASE_PASS),"$(SUPABASE_URL)/auth/v1/signup")
	$(call get_jwt_token,$(SUPABASE_EMAIL),$(SUPABASE_PASS),"$(SUPABASE_URL)/auth/v1/token?grant_type=password")

test-env: test-user
	SUPABASE_EMAIL=$$(cat .env.email | tr -d '\n'); \
	SUPABASE_PASS=$$(cat .env.password | tr -d '\n'); \
	$(call get_jwt_token,$$SUPABASE_EMAIL,$$SUPABASE_PASS,"$(SUPABASE_URL)/auth/v1/token?grant_type=password")

test-api-integration:
	@if [ ! -f .env ]; then \
		echo ".env file not found!"; \
		exit 1; \
	fi
	@if ! grep -q SUPABASE_USER_JWT .env || ! grep -q SUPABASE_URL .env || ! grep -q SUPABASE_ANON_KEY .env; then \
		echo "Required environment variables (SUPABASE_USER_JWT, SUPABASE_URL, SUPABASE_ANON_KEY) are missing in .env!"; \
		exit 1; \
	fi
	@env $$(cat .env | xargs) LFAI_RUN_NIAH_TESTS=$(LFAI_RUN_NIAH_TESTS) PYTHONPATH=$$(pwd) python -m pytest -vv -s tests/integration/api

test-api-unit:
	LFAI_RUN_REPEATER_TESTS=$(LFAI_RUN_REPEATER_TESTS) PYTHONPATH=$$(pwd) python -m pytest -vv -s tests/unit
	LFAI_RUN_REPEATER_TESTS=$(LFAI_RUN_REPEATER_TESTS) PYTHONPATH=$$(pwd) python -m pytest -vv -s tests/pytest

test-load:
	python -m locust -f $$(pwd)/tests/load/loadtest.py --web-port 8089

test-conformance:
	source .env; PYTHONPATH=$$(pwd) pytest -vv -s tests/conformance
