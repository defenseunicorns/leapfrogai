# Testing

This document outlines tests related to the LeapfrogAI API and backends.

Please see the [documentation in the LeapfrogAI UI sub-directory](../src/leapfrogai_ui/README.md) for Svelte UI Playwright tests.

## API Tests

For the unit and integration tests within this directory, the following components must be running and accessible:

- [LeapfrogAI API](../src/leapfrogai_api/README.md)
- [Repeater](../packages/repeater/README.md)
- [Supabase](../packages/supabase/README.md)

Please see the [Makefile](./Makefile) for more details. Below is a quick synopsis of the available Make targets:

```bash
# create a test user for the tests
make test-user SUPABASE_URL=https://supabase-kong.uds.dev

# setup the environment variables for the tests
make test-env SUPABASE_URL=https://supabase-kong.uds.dev

# run the unit tests
make test-api-unit SUPABASE_URL=https://supabase-kong.uds.dev

# run the integration tests
make test-api-integration SUPABASE_URL=https://supabase-kong.uds.dev
```

## Load Tests

Please see the [Load Test documentation](./load/README.md) and directory for more details.

## End-To-End Tests

End-to-End (E2E) tests are located in the `e2e/` sub-directory. Each E2E test runs independently based on the model backend that we are trying to test.

### Running Tests

Run the tests on an existing [UDS Kubernetes cluster](../k3d-gpu/README.md) with the applicable backend deployed to the cluster.

For example, the following sequence of commands runs test on the llama-cpp-python backend:

```bash
# Build and Deploy the LFAI API
make build-api
uds zarf package deploy packages/api/zarf-package-leapfrogai-api-*.tar.zst

# Build and Deploy the model backend you want to test.
# NOTE: In this case we are showing llama-cpp-python
make build-llama-cpp-python
uds zarf package deploy packages/llama-cpp-python/zarf-package-llama-cpp-python-*.tar.zst

# Install the python dependencies
python -m pip install ".[dev]"

# Run the tests!
# NOTE: Each model backend has its own e2e test files
python -m pytest tests/e2e/test_llama.py -v

# Cleanup after yourself
k3d cluster delete uds
```