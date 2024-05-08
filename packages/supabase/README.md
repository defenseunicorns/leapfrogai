# Setting up Supabase locally

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

# Troubleshooting

* If you cannot reach `https://supabase-kong.uds.dev`, check if the `Packages` CRDs and `VirtualServices` contain `supabase-kong.uds.dev`. If they do not, try restarting the `pepr-uds-core-watcher` pod.
* If logging in to the UI through keycloak returns a `500`, check and see if the `sql` migrations have been run in Supabase.
  * You can find those in `leapfrogai/src/leapfrogai_ui/supabase/migrations`. They can be run in the studios SQL Editor.

By following these steps, you'll have successfully set up Keycloak for your application, allowing secure authentication and authorization for your users.