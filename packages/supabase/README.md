Create a client for your application in keycloak
Create a secret called 'supabase-keycloak-secret' that contains the key 'secret' which has a value equal to the Keycloak client secret tied to the applications's client in keycloak
``` bash
kubectl create secret generic supabase-keycloak-secret --from-literal=secret='my-saved-keycloak-secret' -n leapfrogai
```