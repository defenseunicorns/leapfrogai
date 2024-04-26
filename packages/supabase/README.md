Create a client for your application in keycloak
Create a secret called 'supabase-keycloak-secret' that contains the key 'secret' which has a value equal to the Keycloak client secret tied to the applications's client in keycloak
``` bash
kubectl create secret generic supabase-keycloak-secret --from-literal=secret='my-saved-keycloak-secret' -n leapfrogai
```

If it is the first time the package is being deployed to the cluster, set the Zarf var 'EXISTING_POSTGRES_SECRET' to "". If not, then leave it as the default.

The keycloak client that is configured needs to have these urls in both the valid redirect urls and web origins
http://supabase-kong.uds.dev/auth/v1/callback
https://lfaiui.uds.dev/

If you get an error about the client id or secret, 401 unauthorized that may be an indication that the secret supabase-keycloak-secret needs to be updated. So check your current value for client-id and client-secret in Supabase.