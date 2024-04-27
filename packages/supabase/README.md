# Setting Up Keycloak for Your Application

Setup keycloak for the frontend so that you can use auth

## Step 1: Create a Client in Keycloak

In the Keycloak management console, navigate to the "Clients" section and create a new client for the frontend (lfaiui). Make sure to note down the client ID and client secret, as you'll need them later.

## Step 2: Create a Kubernetes Secret

Create a Kubernetes secret named `supabase-keycloak-secret` that contains the client secret from the previous step. Use the following command:

```bash
kubectl create secret generic supabase-keycloak-secret --from-literal=secret='YOUR_KEYCLOAK_CLIENT_SECRET' -n leapfrogai
```

Replace `YOUR_KEYCLOAK_CLIENT_SECRET` with the actual client secret from Keycloak.

## Step 3: Configure Keycloak Client URLs

In the Keycloak client settings, ensure that the following URLs are added to both the "Valid Redirect URIs" and "Web Origins" sections:

- `http://supabase-kong.uds.dev/auth/v1/callback`
- `https://lfaiui.uds.dev/`

## Step 4: Troubleshooting

If you encounter a 401 Unauthorized error, it might indicate that the `supabase-keycloak-secret` secret needs to be updated with the correct client ID and client secret. Double-check the values in Supabase and update the secret accordingly.

By following these steps, you'll have successfully set up Keycloak for your application, allowing secure authentication and authorization for your users.