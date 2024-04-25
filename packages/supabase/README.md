Create a client for your application in keycloak
Create a secret called 'supabase-keycloak-secret' that contains the key 'secret' which has a value equal to the Keycloak client secret tied to the applications's client in keycloak
``` bash
kubectl create secret generic supabase-keycloak-secret --from-literal=secret='my-saved-keycloak-secret' -n leapfrogai
```

If it is the first time the package is being deployed to the cluster, set the Zarf var 'EXISTING_POSTGRES_SECRET' to "". If not, then leave it as the default.