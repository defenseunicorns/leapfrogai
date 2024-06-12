SHELL := /bin/bash


export SUPABASE_URL=$(shell supabase status | grep -oP '(?<=API URL: ).*')
export SUPABASE_ANON_KEY=$(shell supabase status | grep -oP '(?<=anon key: ).*')

install:
	python -m pip install ../../src/leapfrogai_sdk
	python -m pip install -e .

dev:
	python -m uvicorn main:app --port 3000 --reload --log-level info

test-integration:
	cd ../../ && python -m pytest tests/integration/api

define get_jwt_token
	echo "Getting JWT token from ${SUPABASE_URL}..."; \
	TOKEN_RESPONSE=$$(curl -s -X POST $(1) \
	-H "apikey: ${SUPABASE_ANON_KEY}" \
	-H "Content-Type: application/json" \
	-d '{ "email": "admin@localhost", "password": "$$SUPABASE_PASS"}'); \
	echo "Extracting token from $(TOKEN_RESPONSE)"; \
	JWT=$$(echo $$TOKEN_RESPONSE | grep -oP '(?<="access_token":")[^"]*'); \
	echo -n "$$JWT" | xclip -selection clipboard; \
	echo "export SUPABASE_USER_JWT=$$JWT" > .jwt; \
	echo "DONE - JWT token copied to clipboard"
endef

supabase-user:
	@read -s -p "Enter your Supabase password: " SUPABASE_PASS; echo; \
	echo "Creating new supabase user..."; \
	$(call get_jwt_token,"${SUPABASE_URL}/auth/v1/signup")

supabase-jwt-token:
	@read -s -p "Enter your Supabase password: " SUPABASE_PASS; echo; \
	$(call get_jwt_token,"${SUPABASE_URL}/auth/v1/token?grant_type=password")

