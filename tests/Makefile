set-supabase:
	SUPABASE_URL := $(shell cd src/leapfrogai_api; supabase status | awk '/LEAPFROGAI API URL:/ {print $$3}')
	SUPABASE_ANON_KEY := $(shell uds zarf tools kubectl get secret -n leapfrogai supabase-bootstrap-jwt -o json | uds zarf tools yq '.data.anon-key' | base64 -d)

define get_jwt_token
	echo "Getting JWT token from ${SUPABASE_URL}..."; \
	TOKEN_RESPONSE=$$(curl -s -X POST $(1) \
	-H "apikey: ${SUPABASE_ANON_KEY}" \
	-H "Content-Type: application/json" \
	-d '{ "email": "admin@localhost", "password": "$$SUPABASE_PASS"}'); \
	echo "Extracting token from $${TOKEN_RESPONSE}"; \
	JWT=$$(echo $${TOKEN_RESPONSE} | grep -o '"access_token":"[^"]*' | cut -d '"' -f 4); \
	echo "SUPABASE_USER_JWT=$$JWT" > .env; \
	echo "SUPABASE_URL=$$SUPABASE_URL" >> .env; \
	echo "SUPABASE_ANON_KEY=$$SUPABASE_ANON_KEY" >> .env; \
	echo "DONE - variables exported to .env file"
endef

test-user: set-supabase
	@read -s -p "Enter a new DEV API password: " SUPABASE_PASS; echo; \
	echo "Creating new supabase user..."; \
	$(call get_jwt_token,"${SUPABASE_URL}/auth/v1/signup")

test-env: set-supabase
	@read -s -p "Enter your DEV API password: " SUPABASE_PASS; echo; \
	$(call get_jwt_token,"${SUPABASE_URL}/auth/v1/token?grant_type=password")

test-api-intergation: set-supabase
	source .env; PYTHONPATH=$$(pwd) pytest -vv -s tests/integration/api

test-api-unit: set-supabase
	PYTHONPATH=$$(pwd) pytest -vv -s tests/unit

test-load:
	locust -f ${PWD}/tests/load/loadtest.py --web-port 8089

debug: set-supabase
	@echo ${SUPABASE_URL}
	@echo ${SUPABASE_ANON_KEY}
