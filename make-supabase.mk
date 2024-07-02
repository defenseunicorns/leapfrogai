SHELL := /bin/bash


export SUPABASE_URL=$(shell cd src/leapfrogai_api; supabase status | grep -oP '(?<=API URL: ).*')
export SUPABASE_ANON_KEY=$(shell cd src/leapfrogai_api; supabase status | grep -oP '(?<=anon key: ).*')

define get_jwt_token
	echo "Getting JWT token from ${SUPABASE_URL}..."; \
	TOKEN_RESPONSE=$$(curl -s -X POST $(1) \
	-H "apikey: ${SUPABASE_ANON_KEY}" \
	-H "Content-Type: application/json" \
	-d '{ "email": "admin@localhost", "password": "$$SUPABASE_PASS"}'); \
	echo "Extracting token from $(TOKEN_RESPONSE)"; \
	JWT=$$(echo $$TOKEN_RESPONSE | grep -oP '(?<="access_token":")[^"]*'); \
	echo "SUPABASE_USER_JWT=$$JWT" > .env; \
	echo "SUPABASE_URL=$$SUPABASE_URL" >> .env; \
	echo "SUPABASE_ANON_KEY=$$SUPABASE_ANON_KEY" >> .env; \
	echo "DONE - `.env` file updated"
endef

supabase-new-user:
	@read -s -p "Enter a new DEV API password: " SUPABASE_PASS; echo; \
	echo "Creating new supabase user..."; \
	$(call get_jwt_token,"${SUPABASE_URL}/auth/v1/signup")

env:
	@read -s -p "Enter your DEV API password: " SUPABASE_PASS; echo; \
	$(call get_jwt_token,"${SUPABASE_URL}/auth/v1/token?grant_type=password")