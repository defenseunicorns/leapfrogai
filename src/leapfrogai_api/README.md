# LeapfrogAI API

> [!IMPORTANT]
> See the [API package documentation](../../packages/api/README.md) for general pre-requisites, dependent components, and package deployment instructions

This document is only applicable for spinning up the API in a local Python development environment.

## Local Development Setup

> [!IMPORTANT]
> Execute the following commands from this sub-directory

### Running

1. Install dependencies

    ```bash
    make install-api
    ```

2. Create a config.yaml using the config.example.yaml as a template.

3. Run the FastAPI application

    ```bash
    make dev-run-api
    ```

4. Create a local Supabase user

    ```bash
    make user
    ```

5. Create an API (JWT) token

    ```bash
    make jwt
    source .env
    ```

    This will copy the JWT token to your clipboard.

6. Make calls to the api swagger endpoint at `http://localhost:8080/docs` using your JWT token as the `HTTPBearer` token.
   * Hit `Authorize` on the swagger page to enter your JWT token

### Integration Tests

The integration tests serve to verify API functionality and compatibility with other existing components:

* Check all API routes
* Validate Request/Response objects
* Database CRUD operations
* Schema mismatches

#### Running the tests

After obtaining the JWT token, run the following:

```bash
make test-integration
```
