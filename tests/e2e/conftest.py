import os
import warnings
import pytest

from openai import OpenAI

from .utils import create_test_user

DEFAULT_LEAPFROGAI_MODEL = "llama-cpp-python"


@pytest.fixture(scope="module")
def client():
    return OpenAI(
        base_url="https://leapfrogai-api.uds.dev/openai/v1", api_key=create_test_user()
    )


def get_model_name():
    model_name = os.getenv("LEAPFROGAI_MODEL")
    if model_name is None:
        warnings.warn(
            f"LEAPFROGAI_MODEL environment variable not set. Defaulting to '{DEFAULT_LEAPFROGAI_MODEL}'.\n"
            "Consider setting LEAPFROGAI_MODEL explicitly. Examples: 'vllm', 'repeater', 'llama-cpp-python'."
        )
        model_name = DEFAULT_LEAPFROGAI_MODEL
    return model_name


@pytest.fixture(scope="module")
def model_name():
    return get_model_name()
