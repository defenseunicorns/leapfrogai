# LeapfrogAI Repeater Backend

A LeapfrogAI API-compatible repeater backend that simply parrots the input it is provided back to the user. This is primarily used for quick-testing the API.

The repeater backend is used to verify that the API is able to both load configs for and send inputs to a very simple backend. The repeater backend fulfills this role by returning the input it recieves as output.

## Usage

### Pre-Requisites

See the LeapfrogAI documentation website for [system requirements](https://docs.leapfrog.ai/docs/local-deploy-guide/requirements/) and [dependencies](https://docs.leapfrog.ai/docs/local-deploy-guide/dependencies/).

#### Dependent Components

- Have the LeapfrogAI API deployed, running, and accessible in order to provide a fully RESTful application

### Deployment

To build and deploy the repeater backend Zarf package into an existing [UDS Kubernetes cluster](../k3d-gpu/README.md):

> [!IMPORTANT]
> Execute the following Make targets from the root of the LeapfrogAI repository

```bash
make build-repeater LOCAL_VERSION=dev
uds zarf package deploy packages/repeater/zarf-package-repeater-*-dev.tar.zst --confirm
```

### Local Development

To run the repeater backend locally:

> [!IMPORTANT]
> Execute the following commands from this sub-directory

```bash
# Setup Virtual Environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies and start the model backend
make dev
```

Now the basic API tests can be run in full with the following commands.

> [!IMPORTANT]
> Execute the following commands from from the root of the LeapfrogAI repository

```bash
export LFAI_RUN_REPEATER_TESTS=true    # this is needed to run the tests that require the repeater model, otherwise they get skipped
pytest tests/pytest/test_api_auth.py
```
