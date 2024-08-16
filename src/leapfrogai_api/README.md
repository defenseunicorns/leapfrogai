# LeapfrogAI API

> [!IMPORTANT]
> See the [API package documentation](../../packages/api/README.md) for general pre-requisites, dependent components, and package deployment instructions

This document is only applicable for spinning up the API in a local Python development environment.

## Local Development Setup

> [!IMPORTANT]
> Execute the following commands from this sub-directory

### Running

> [!IMPORTANT]
> The following steps assume that you already have a deployed and accessible UDS Kubernetes cluster and LeapfrogAI. Please follow the steps within the [DEVELOPMENT.md](../../docs/DEVELOPMENT.md) for details.

1. Install dependencies

    ```bash
    make install
    ```

2. Create a config.yaml using the config.example.yaml as a template.

3. Run the FastAPI application

    ```bash
    make dev API_PORT=3000
    ```

4. Create an API key with test user "leapfrogai@defenseunicorns.com" and test password "password", lasting 30 days from creation time

    ```bash
    # If the in-cluster API is up, and not testing the API workflow
    make api-key API_BASE_URL=https://leapfrogai-api.uds.dev
    ```

    To create a new 30-day API key, use the following:

    ```bash
    # If the in-cluster API is up, and not testing the API workflow
    make new-api-key API_BASE_URL=https://leapfrogai-api.uds.dev
    ```

    The newest API key will be printed to a `.env` file located within this directory.

5. Make calls to the API Swagger endpoint at `http://localhost:8080/docs` using your API token as the `HTTPBearer` token.

    - Hit `Authorize` on the Swagger page to enter your API key

### Access

See the ["Access" section of the DEVELOPMENT.md](../../docs/DEVELOPMENT.md#access) for different ways to connect the API to a model backend or Supabase.

### Tests

See the [tests directory documentation](../../tests/README.md) for more details.
