# Supabase

A comprehensive relational and vector database operator and multi-functional API layer. See the [Supabase documentation](https://supabase.com/docs) and the [Bitnami package](https://bitnami.com/stack/supabase) for more details.

## Usage

### Pre-Requisites

See the LeapfrogAI documentation website for [system requirements](https://docs.leapfrog.ai/docs/local-deploy-guide/requirements/) and [dependencies](https://docs.leapfrog.ai/docs/local-deploy-guide/dependencies/).

#### Dependent Components

- [UDS Kubernetes cluster bootstrapped with UDS Core Slim Dev](../k3d-gpu/README.md) for local KeyCloak authentication, Istio Service Mesh, and MetalLB advertisement
- [LeapfrogAI API](../api/README.md) for RESTful interaction
- [Text Embeddings](../text-embeddings/README.md) for vector generation
- [LeapfrogAI UI](../ui/README.md) for a Supabase and API compatible frontend

### Deployment

To build and deploy the Supabase Zarf package into an existing [UDS Kubernetes cluster](../k3d-gpu/README.md):

> [!IMPORTANT]
> Execute the following commands from the root of the LeapfrogAI repository

```bash
make build-supabase LOCAL_VERSION=dev
uds zarf package deploy packages/supabase/zarf-package-supabase-*-dev.tar.zst --confirm
```

### Accessing Supabase

Go to `https://supabase-kong.uds.dev`. The login is `supabase-admin` the password is randomly generated in a cluster secret named `supabase-dashboard-secret`

**NOTE:** The `uds.dev` domain is only used for locally deployed LeapfrogAI packages, so this domain will be unreachable without first manually deploying the UDS bundle.

## Troubleshooting

- If you cannot reach `https://supabase-kong.uds.dev`, check if the `Packages` CRDs and `VirtualServices` contain `supabase-kong.uds.dev`. If they do not, try restarting the `pepr-uds-core-watcher` pod.
- If logging in to the UI through keycloak returns a `500`, check and see if the `sql` migrations have been run in Supabase.
  - You can find those in `leapfrogai/src/leapfrogai_ui/supabase/migrations` - Migrations can be run in the Supabase studio SQL editor
- To obtain a 1-hour JWT for testing run the following:

  ```bash
  # Replace <email>, <password>, and <confirmPassword> with your desired credentials
  # Grab the Supabase Anon Key from the JWT Secret in the UDS Kubernetes cluster and use it with xargs
  uds zarf tools kubectl get secret -n leapfrogai supabase-bootstrap-jwt -o json | uds zarf tools yq '.data.anon-key' | base64 -d | xargs -I {} curl -X POST 'https://supabase-kong.uds.dev/auth/v1/signup' \
    -H "apikey: {}" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer {}" \
    -d '{ "email": "<email>", "password": "<password>", "confirmPassword": "<confirmPassword>"}'
  ```

- Longer term API tokens (30, 60, or 90 days) can be created from the API key workflow within the LeapfrogAI UI
- Longer term API tokens (30 days) can also be created using the [API documentation](../../src/leapfrogai_api/README.md)

## Supabase Migrations

### Motivation

A database migration is the process of modifying a database's schema in a controlled and versioned way. Migrations are used to modify the functionality of a database as its supported applications evolves over time. As time goes on, an application may require new tables, or tables may need new columns/indexes. Migrations allow for smooth changes to be applied to deployed databases, regardless of the current version the application is on.

Migrations catalog a history of the database and provide an inherit form of database documentation, as each migration is stored in the Git repository chronologically (and by release). Migrations are automated on new deployments of LeapfrogAI such that all of the migrations (i.e database changes) are applied in order to ensure that the database has the most up to date schema. Migrations can also be run anytime a new version of LeapfrogAI is released, regardless of which version of LeapfrogAI is being updated from.

### Approach

Migrations are handled using the [Supabase CLI](https://supabase.com/docs/guides/cli/getting-started?queryGroups=platform&platform=linux). The Supabase CLI automatically handles new migrations and keeps track of which migrations have already been run, regardless whether the database instance is brand new or pre-existing.

Migrations are intended to be tracked by the package that needs them, so for example, migrations for API-specific needs are tracked within the [API package migrations](/packages/api/supabase/migrations/) and migrations needed by the UI are tracked within the [UI migrations](/src/leapfrogai_ui/supabase/migrations/).

In order to submit migrations at deploy time, [K8s jobs](https://kubernetes.io/docs/concepts/workloads/controllers/job/) are used to run the Supabase CLI commands. These migration K8s jobs are built off of a small [Docker container](/Dockerfile.migrations) that runs the Supabase CLI commands for each packages associated migrations. The primary Dockerfile for these jobs is located at the root of the repository.

The K8s jobs themselves simply pull any existing migrations from the remote database within the same cluster, then push up the local migrations. Due to the [schema migrations table](https://supabase.com/docs/reference/cli/usage#supabase-db-push), any migrations that have already been run on the remote database will be skipped, ensuring migrations are not repeated. Since each package's migrations should be separate, a different template is used for each job.

### Managing Migrations

Keep the following in mind when adding new migrations:

- Do not update previous migrations. If the schema for a table is to be changed for example, create a new migration that handles the schema updates. This new migration will automatically be applied during the K8s migration job.
- Migrations should only update tables that have to do with their associated package. For example, the UI should not have associated migrations that affect the vector database, so no migration files doing so should be in the UI's supabase migrations directory. This keeps package migrations separable from one another.
- When adding new migrations for a package that does not yet have migrations, remember to do the following to add a new K8s migration job
  - add a `migration-job.yaml` in the package's template directory
  - update the package's `zarf.yaml` to include the new image
  - update the `Makefile` to build the new migrations image
  - add the new migrations image to the `release.yaml` pipeline
