import pytest

from openai import OpenAI

from .utils import create_test_user


@pytest.fixture(scope="module")
def client():
    return OpenAI(
        base_url="https://leapfrogai-api.uds.dev/openai/v1", api_key=create_test_user()
    )
