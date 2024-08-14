# LeapfrogAI API

A mostly OpenAI compliant API surface.

## Zarf Package Deployment

To build and deploy just the API Zarf package (from the root of the repository):

> Deploy a [UDS cluster](../../README.md#uds) if one isn't deployed already

```bash
make build-api LOCAL_VERSION=dev
uds zarf package deploy packages/api/zarf-package-leapfrogai-api-*-dev.tar.zst --confirm
```

## Local Development Setup

1. Install dependencies

    ```bash
    make install
    ```

2. Create a config.yaml using the config.example.yaml as a template.

3. Run the FastAPI application

    ``` bash
    make dev-run-api
    ```

4. Create a local Supabase instance (requires [Supabase CLI](https://supabase.com/docs/guides/cli/getting-started)):

    ```bash
    brew install supabase/tap/supabase

    supabase start # from this directory

    supabase stop --project-id leapfrogai # stop api containers

    supabase db reset # clears all data and re-initializes migrations

    supabase status # to check status and see your keys
    ```

5. Create a local API user

    ```bash
    make user
    ```

6. Create a JWT token

    ```bash
    make jwt
    source .env
    ```

    This will copy the JWT token to your clipboard.

7. Make calls to the api swagger endpoint at `http://localhost:8080/docs` using your JWT token as the `HTTPBearer` token.
   * Hit `Authorize` on the swagger page to enter your JWT token

## Integration Tests

The integration tests serve to identify any mismatches between components:

* Check all API routes
* Validate Request/Response types
* DB CRUD operations
* Schema mismatches

### Prerequisites

Integration tests require a Supabase instance and environment variables configured (see [Local Development](#local-development-setup)).

### Authentication

Tests require a JWT token environment variable `SUPABASE_USER_JWT`. See [Local Development](#local-development-setup) steps 3-5 to set this up.

### Running the tests

After obtaining the JWT token, run the following:

```bash
make test-integration
```

## Notes

* All API calls must be authenticated via a Supabase JWT token in the message's `Authorization` header, including swagger docs.
