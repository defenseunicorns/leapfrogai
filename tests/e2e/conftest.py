import pytest

from openai import OpenAI

from .utils import create_test_user


@pytest.fixture(scope="module")
def client():
    return OpenAI(
        base_url="https://leapfrogai-api.uds.dev/openai/v1", api_key=create_test_user()
    )


def pytest_addoption(parser):
    parser.addoption(
        "--model_name",
        action="append",
        help="Model name(s) to test, e.g., vllm or llama-cpp-python (required)",
    )


@pytest.fixture
def model_name(request):
    model_names = request.config.getoption("--model_name")

    if not model_names:
        pytest.exit(
            "Error: --model_name is required. Please provide at least one model name."
        )

    # If a single model name is provided, return it directly
    if len(model_names) == 1:
        return model_names[0]

    # If multiple model names are provided, return the list (for future use if needed)
    return model_names
