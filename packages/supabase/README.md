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

**NOTE:** The `uds.dev` domain is only used for locally deployed LeapfrogAI packages, so this domain will be unreachable without first manually deploying the UDS bundle.

## Local Supabase Troubleshooting

* If you cannot reach `https://supabase-kong.uds.dev`, check if the `Packages` CRDs and `VirtualServices` contain `supabase-kong.uds.dev`. If they do not, try restarting the `pepr-uds-core-watcher` pod.
* If logging in to the UI through keycloak returns a `500`, check and see if the `sql` migrations have been run in Supabase.
  * You can find those in `leapfrogai/src/leapfrogai_ui/supabase/migrations`. They can be run in the studios SQL Editor.
* To obtain a jwt token for testing, create a test user and run the following:
```
curl -X POST 'https://supabase-kong.uds.dev/auth/v1/token?grant_type=password' \-H "apikey: <anon-key>" \-H "Content-Type: application/json" \-d '{ "email": "<test-email>", "password": "<test-password>"}'
```

By following these steps, you'll have successfully set up Keycloak for your application, allowing secure authentication and authorization for your users.


# Supabase Migrations

## Motivation

A database migration is the process of modifying a database's schema in a controlled and versioned way. Migrations are used to modify the functionality of a database as its supported applications evolves over time. As time goes on, an application may require new tables, or tables may need new columns/indexes. Migrations allow for smooth changes to be applied to deployed databases, regardless of the current version the application is on.

Migrations catalog a history of the database and provide an inherit form of database documentation, as each migration is stored in the Git repository chronologically (and by release). Migrations are automated on new deployments of LeapfrogAI such that all of the migrations (i.e database changes) are applied in order to ensure that the database has the most up to date schema. Migrations can also be run anytime a new version of LeapfrogAI is released, regardless of which version of LeapfrogAI is being updated from.

## Approach

Migrations are handled using the [Supabase CLI](https://supabase.com/docs/guides/cli/getting-started?queryGroups=platform&platform=linux). The Supabase CLI automatically handles new migrations and keeps track of which migrations have already been run, regardless whether the database instance is brand new or pre-existing.

Migrations are intended to be tracked by the package that needs them, so for example, migrations for API-specific needs are tracked within the [API package migrations](/packages/api/supabase/migrations/) and migrations needed by the UI are tracked within the [UI migrations](/src/leapfrogai_ui/supabase/migrations/).

In order to submit migrations at deploy time, [K8s jobs](https://kubernetes.io/docs/concepts/workloads/controllers/job/) are used to run the Supabase CLI commands. These migration K8s jobs are built off of [small Docker Containers](/packages/api/supabase/Dockerfile) that solely run the Supabase CLI commands for their associated migrations. The Dockerfiles for these jobs must be colocated with the directory that contains its associated migrations, so for example, the migrations and Dockerfile for the API migrations live within the [API package's supabase directory](/packages/api/supabase).

The K8s jobs themselves simply pull any existing migrations from the remote database within the same cluster, then push up the local migrations. Due to the [schema migrations table](https://supabase.com/docs/reference/cli/usage#supabase-db-push), any migrations that have already been run on the remote database will be skipped, ensuring migrations are not repeated. Since each package's migrations should be separate, a different template is used for each job.

## Managing Migrations

Keep the following in mind when adding new migrations:

- Do not update previous migrations. If the schema for a table is to be changed for example, create a new migration that handles the schema updates. This new migration will automatically be applied during the K8s migration job.
- Migrations should only update tables that have to do with their associated package. For example, the UI should not have associated migrations that affect the vector database, so no migration files doing so should be in the UI's supabase migrations directory. This keeps package migrations separable from one another.
- When adding new migrations for a package that does not yet have migrations, remember to do the following to add a new K8s migration job
  - add a `migration-job.yaml` in the package's template directory
  - add a `Dockerfile` to build the image that contains the Supabase CLI and migrations
  - update the package's `zarf.yaml` to include the new image
  - update the `Makefile` to build the new migrations image
  - add the new migrations image to the `release.yaml` pipeline
