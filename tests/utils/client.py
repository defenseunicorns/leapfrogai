from openai import OpenAI
import os

LEAPFROGAI_MODEL = os.getenv("LEAPFROGAI_MODEL", "llama-cpp-python")
OPENAI_MODEL = "gpt-4o-mini"
ROOT_URL = "https://leapfrogai-api.uds.dev"



def openai_client():
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def leapfrogai_client():
    return OpenAI(
        base_url=os.getenv(
            "LEAPFROGAI_API_URL", "https://leapfrogai-api.uds.dev/openai/v1"
        ),
        api_key=os.getenv("LEAPFROGAI_API_KEY") or os.getenv("SUPABASE_USER_JWT"),
    )


class ClientConfig:
    client: OpenAI
    model: str

    def __init__(self, client: OpenAI, model: str):
        self.client = client
        self.model = model


def client_config_factory(client_name: str) -> ClientConfig:
    if client_name == "openai":
        return ClientConfig(client=openai_client(), model=OPENAI_MODEL)
    elif client_name == "leapfrogai":
        return ClientConfig(client=leapfrogai_client(), model=LEAPFROGAI_MODEL)
    else:
        raise ValueError(f"Unknown client name: {client_name}")
