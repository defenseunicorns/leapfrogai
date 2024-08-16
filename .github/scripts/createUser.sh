KEYCLOAK_ADMIN_PASSWORD=$(uds zarf tools kubectl get secret -n keycloak keycloak-admin-password -o jsonpath={.data.password} | base64 -d)
KEYCLOAK_ADMIN_TOKEN=$(curl -s --location "https://keycloak.admin.uds.dev/realms/master/protocol/openid-connect/token" \
--header "Content-Type: application/x-www-form-urlencoded" \
--data-urlencode "username=admin" \
--data-urlencode "password=${KEYCLOAK_ADMIN_PASSWORD}" \
--data-urlencode "client_id=admin-cli" \
--data-urlencode "grant_type=password" | uds zarf tools yq .access_token)
curl --location "https://keycloak.admin.uds.dev/admin/realms/uds/users" \
--header "Content-Type: application/json" \
--header "Authorization: Bearer ${KEYCLOAK_ADMIN_TOKEN}" \
--data-raw '{
  "username": "doug",
  "firstName": "Doug",
  "lastName": "Unicorn",
  "email": "doug@uds.dev",
  "attributes": {
    "mattermostid": "1"
  },
  "emailVerified": true,
  "enabled": true,
  "requiredActions": [],
  "credentials": [
    {
      "type": "password",
      "value": "unicorn123!@#UN",
      "temporary": false
    }
  ]
}'
CONDITIONAL_OTP_ID=$(curl --location "https://keycloak.admin.uds.dev/admin/realms/uds/authentication/flows/Authentication/executions" \
--header "Authorization: Bearer ${KEYCLOAK_ADMIN_TOKEN}" | uds zarf tools yq '.[] | select(.displayName == "Conditional OTP") | .id')
curl --location --request PUT "https://keycloak.admin.uds.dev/admin/realms/uds/authentication/flows/Authentication/executions" \
--header "Content-Type: application/json" \
--header "Authorization: Bearer ${KEYCLOAK_ADMIN_TOKEN}" \
--data "{
\"id\": \"${CONDITIONAL_OTP_ID}\",
\"requirement\": \"DISABLED\"
}"
USER=$(curl --location "https://keycloak.admin.uds.dev/admin/realms/uds/users?user=doug" \
--header "Content-Type: application/json" \
--header "Authorization: Bearer ${KEYCLOAK_ADMIN_TOKEN}" \
)
echo "User: $USER"