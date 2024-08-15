API_PORT := 3000
API_BASE_URL := https://leapfrogai-api.uds.dev
SUPABASE_BASE_URL := https://supabase-kong.uds.dev
EXPIRATION_TIME := $(shell date -d "+30 days" +%s)
SUPABASE_ANON_KEY := $(shell uds zarf tools kubectl get secret -n leapfrogai supabase-bootstrap-jwt -o json | uds zarf tools yq '.data.anon-key' | base64 -d)

install: set-env
	python -m pip install ../../src/leapfrogai_sdk
	python -m pip install -e ".[dev]"

set-env:
	echo "SUPABASE_URL=${SUPABASE_BASE_URL}" > .env
	echo "SUPABASE_ANON_KEY=${SUPABASE_ANON_KEY}" >> .env

dev: set-env
	. ./.env && python -m uvicorn main:app --port ${API_PORT} --reload --log-level info

api-key:
	curl -s -X POST '${SUPABASE_BASE_URL}/auth/v1/signup' \
	-H "apikey:  ${SUPABASE_ANON_KEY}" \
	-H "Content-Type: application/json" \
	-H "Authorization: Bearer  ${SUPABASE_ANON_KEY}" \
	-d '{ "email": "leapfrogai@defenseunicorns.com", "password": "password", "confirmPassword": "password"}' | \
	uds zarf tools yq '.access_token' | \
	xargs -I {} curl -s --insecure -X POST '${API_BASE_URL}/leapfrogai/v1/auth/api-keys' \
	-H "apikey: {}" \
	-H "Content-Type: application/json" \
	-H "Authorization: Bearer {}" \
	-d '{ "name": "api-key", "expires_at": "${EXPIRATION_TIME}" }' | \
	uds zarf tools yq '.api_key'

new-api-key:
	curl -s -X POST '${SUPABASE_BASE_URL}/auth/v1/token?grant_type=password' \
	-H "apikey:  ${SUPABASE_ANON_KEY}" \
	-H "Content-Type: application/json" \
	-H "Authorization: Bearer  ${SUPABASE_ANON_KEY}" \
	-d '{ "email": "leapfrogai@defenseunicorns.com", "password": "password"}' | \
	uds zarf tools yq '.access_token' | \
	xargs -I {} curl -s --insecure -X POST '${API_BASE_URL}/leapfrogai/v1/auth/api-keys' \
	-H "apikey: {}" \
	-H "Content-Type: application/json" \
	-H "Authorization: Bearer {}" \
	-d '{ "name": "api-key", "expires_at": "${EXPIRATION_TIME}" }' | \
	uds zarf tools yq '.api_key'
