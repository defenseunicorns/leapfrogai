# LeapfrogAI Repeater Backend

A LeapfrogAI API-compatible repeater model that simply parrots the input it is provided back to the user. This is primarily used for quick-testing the API.


# Usage

The repeater model is used to verify that the API is able to both load configs for and send inputs to a very simple model. The repeater model fulfills this role by returning the input it recieves as output.

## Local Usage

Here is how to run the repeater model locally to test the API:

It's easiest to set up a virtual environment to keep things clean:
```
python -m venv .venv
source .venv/bin/activate
```

First install the lfai-repeater project and dependencies. From the root of the project repository:
```
pip install src/leapfrogai_sdk
cd packages/repeater
pip install .
```

Next, launch the repeater model:
```
python repeater.py
```

Now the basic API tests can be run in full. In a new terminal, starting from the root of the project repository:
```
export LFAI_RUN_REPEATER_TESTS=true    # this is needed to run the tests that require the repeater model, otherwise they get skipped
pytest tests/pytest/test_api.py
```
