# LeapfrogAI API

A mostly OpenAI compliant API surface.

## Local Development Setup

1. Install dependencies
    ```bash
    make install
    ```

2. Create a local Supabase instance (requires [Supabase CLI](https://supabase.com/docs/guides/cli/getting-started)):
    ```bash
    brew install supabase/tap/supabases

    supabase start # from this directory

    supabase stop --project-id leapfrogai # stop api containers

    supabase db reset # clears all data and reinitializes migrations

    supabase status # to check status and see your keys
    ```

### Session Authentication

3. Create a local api user
    ```bash
    make user
    ```

4. Create a JWT token
    ```bash
    make jwt
    source .env
    ```
    This will copy the JWT token to your clipboard.


5. Make calls to the api swagger endpoint at `http://localhost:8080/docs` using your JWT token as the `HTTPBearer` token.
   * Hit `Authorize` on the swagger page to enter your JWT token

## Integration Tests

The integration tests serve to identify any mismatches between components:

- Check all API routes
- Validate Request/Response types
- DB CRUD operations
- Schema mismatches

### Prerequisites

Integration tests require a Supabase instance and environment variables configured (see [Local Development](#local-development)).

### Authentication

Tests require a JWT token environment variable `SUPABASE_USER_JWT`. See [Session Authentication](#session-authentication) to set this up.

### Running the tests
After obtaining the JWT token, run the following:
```
make test-integration
```

## Notes

* All API calls must be authenticated via a Supabase JWT token in the message's `Authorization` header, including swagger docs.
