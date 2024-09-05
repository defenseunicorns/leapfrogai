from openai import OpenAI
import os
from pathlib import Path


LEAPFROGAI_MODEL = "llama-cpp-python"
OPENAI_MODEL = "gpt-4o-mini"


def text_file_path():
    return Path(os.path.dirname(__file__) + "/../data/test_with_data.txt")


def openai_client():
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def leapfrogai_client():
    return OpenAI(
        base_url=os.getenv("LEAPFROGAI_API_URL"),
        api_key=os.getenv("SUPABASE_USER_JWT"),
    )


class ClientConfig:
    client: OpenAI
    model: str

    def __init__(self, client: OpenAI, model: str):
        self.client = client
        self.model = model


def client_config_factory(client_name) -> ClientConfig:
    if client_name == "openai":
        return ClientConfig(client=openai_client(), model=OPENAI_MODEL)
    elif client_name == "leapfrogai":
        return ClientConfig(client=leapfrogai_client(), model=LEAPFROGAI_MODEL)
    else:
        raise ValueError(f"Unknown client name: {client_name}")
