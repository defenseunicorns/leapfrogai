# Setting up Supabase locally

Setup keycloak for the frontend so that you can use auth

## Step 1: Create a Zarf package

From `leapfrogai/packages/supabase` run `zarf package create`

## Step 2: Create the uds bundle

From `leapfrogai/uds-bundles/dev/<cpu|gpu>/` run `uds create`


## Step 3: Deploy the UDS bundle or deploy the Zarf package

To deploy only Supabase for UDS bundle run the following from `leapfrogai/uds-bundles/dev/<cpu|gpu>/`:
* `uds deploy -p supabase uds-bundle-leapfrogai-*.tar.zst`

To deploy the Zarf package run the following from `leapfrogai/packages/supabase`:
* `uds zarf package deploy zarf-package-supabase-*.tar.zst`

## Step 4: Accessing Supabase

Go to `https://supabase-kong.uds.dev`. The login is `supabase-admin` the password is randomly generated in a cluster secret named `supabase-dashboard-secret`

# Setting Up Keycloak integration for Your Application

Setup keycloak for the frontend so that you can use auth

## Step 1: Create a Client in Keycloak

In the Keycloak management console, navigate to the "Clients" section and create a new client with a client ID of `leapfrogai`. Make sure to note down the client secret, as you'll need them later.

## Step 2: Create a Kubernetes Secret

Create a Kubernetes secret named `supabase-keycloak-secret` that contains the client secret from the previous step. Use the following command:

```bash
kubectl create secret generic supabase-keycloak-secret --from-literal=secret='YOUR_KEYCLOAK_CLIENT_SECRET' -n leapfrogai
```

Replace `YOUR_KEYCLOAK_CLIENT_SECRET` with the actual client secret from Keycloak.

## Step 3: Configure Keycloak Client URLs

In the Keycloak client settings, ensure that the following URLs are added to both the "Valid Redirect URIs" and "Web Origins" sections:

- `http://supabase-kong.uds.dev/auth/v1/callback`

# Troubleshooting

* If you encounter a 401 Unauthorized error, it might indicate that the `supabase-keycloak-secret` secret needs to be updated with the correct client ID and client secret. Double-check the values in Supabase and update the secret accordingly.
* If you cannot reach `https://supabase-kong.uds.dev`, check if the `Packages` CRDs and `VirtualServices` contain `supabase-kong.uds.dev`. If they do not, try restarting the `pepr-uds-core-watcher` pod.

By following these steps, you'll have successfully set up Keycloak for your application, allowing secure authentication and authorization for your users.