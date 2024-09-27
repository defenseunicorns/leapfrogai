from urllib.parse import urljoin
from openai import OpenAI
import os
from requests import Response

import requests


def get_leapfrogai_model():
    try:
        return os.getenv("LEAPFROGAI_MODEL", "vllm")
    except KeyError:
        raise ValueError("LEAPFROGAI_MODEL not set")


def get_openai_model():
    try:
        return os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    except KeyError:
        raise ValueError("OPENAI_MODEL not set")


def get_leapfrogai_api_key():
    try:
        return os.getenv("LEAPFROGAI_API_KEY") or os.getenv("SUPABASE_USER_JWT")
    except KeyError:
        raise ValueError("LEAPFROGAI_API_KEY or SUPABASE_USER_JWT not set")


def get_leapfrogai_api_url():
    try:
        return os.getenv(
            "LEAPFROGAI_API_URL", "https://leapfrogai-api.uds.dev/openai/v1"
        )
    except KeyError:
        raise ValueError("LEAPFROGAI_API_URL not set")


def get_leapfrogai_api_url_other():
    try:
        return os.getenv("LEAPFROGAI_API_URL_OTHER", "https://leapfrogai-api.uds.dev")
    except KeyError:
        raise ValueError("LEAPFROGAI_API_URL_OTHER not set")


def openai_client():
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def leapfrogai_client():
    return OpenAI(
        base_url=get_leapfrogai_api_url(),
        api_key=get_leapfrogai_api_key(),
    )


class ClientConfig:
    client: OpenAI
    model: str

    def __init__(self, client: OpenAI, model: str):
        self.client = client
        self.model = model


def client_config_factory(client_name: str) -> ClientConfig:
    """Factory function for creating a client configuration that is OpenAI compliant."""
    if client_name == "openai":
        return ClientConfig(client=openai_client(), model=get_openai_model())
    elif client_name == "leapfrogai":
        return ClientConfig(client=leapfrogai_client(), model=get_leapfrogai_model())
    else:
        raise ValueError(f"Unknown client name: {client_name}")


class LeapfrogAIClient:
    """Client for handling queries in the LeapfrogAI namespace that are not handled by the OpenAI SDK."""

    def __init__(self, base_url: str | None = None, api_key: str | None = None):
        self.base_url = base_url or get_leapfrogai_api_url_other()
        self.api_key = api_key or get_leapfrogai_api_key()
        self.headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

    def get(self, endpoint, **kwargs) -> Response | None:
        url = urljoin(self.base_url, endpoint)
        response = requests.get(url, headers=self.headers, **kwargs)
        return self._handle_response(response)

    def post(self, endpoint, **kwargs) -> Response | None:
        url = urljoin(self.base_url, endpoint)
        response = requests.post(url, headers=self.headers, **kwargs)
        return self._handle_response(response)

    def put(self, endpoint, **kwargs) -> Response | None:
        url = urljoin(self.base_url, endpoint)
        response = requests.put(url, headers=self.headers, **kwargs)
        return self._handle_response(response)

    def delete(self, endpoint, **kwargs) -> Response | None:
        url = urljoin(self.base_url, endpoint)
        response = requests.delete(url, headers=self.headers, **kwargs)
        return self._handle_response(response)

    def _handle_response(self, response) -> Response | None:
        response.raise_for_status()
        if response.content:
            return response
        return None
