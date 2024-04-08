# LeapfrogAI End-To-End Tests

This directory holds our e2e tests that we use to verify LFAI-API + various model backend functionality in an environment that replicates a live setting. The tests in this directory are automatically run against a [UDS Core](https://github.com/defenseunicorns/uds-core) cluster whenever a PR is opened or updated.


## Running Tests Locally
The tests in this directory are also able to be run locally! We are currently opinionated towards running on a cluster that is configured with UDS, as we mature out tests & documentations we'll potentially lose some of that opinionation.


### Dependencies
1. Python >= 3.11.6
2. k3d >= v5.6.0
3. uds >= v0.7.0


### Actually Running The Test
There are several ways you can setup and run these tests. Here is one such way:

```bash
# Setup the UDS cluster
# NOTE: This stands up a k3d cluster and installs istio & pepr
# NOTE: Be sure to use the latest released version at the time you're reading this!
uds deploy oci://ghcr.io/defenseunicorns/packages/uds/bundles/k3d-core-slim-dev:0.18.0 --confirm

# Build and Deploy the LFAI API
make build-api
uds zarf package deploy zarf-package-leapfrogai-api-*.tar.zst

# Build and Deploy the model backend you want to test.
# NOTE: In this case we are showing llama-cpp-python
make build-llama-cpp-python
uds zarf package deploy zarf-package-llama-cpp-python-*.tar.zst

# Install the python dependencies
python -m pip install ".[e2e-test]"

# Run the tests!
# NOTE: Each model backend has its own e2e test files
python -m pytest tests/e2e/test_llama.py -v

# Cleanup after yourself
k3d cluster delete
```
