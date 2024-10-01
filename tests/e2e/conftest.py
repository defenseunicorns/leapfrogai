from openai import OpenAI
import pytest

from tests.utils.client import leapfrogai_client, get_leapfrogai_model


@pytest.fixture(scope="module")
def client() -> OpenAI:
    return leapfrogai_client()


@pytest.fixture(scope="module")
def model_name() -> str:
    return get_leapfrogai_model()
