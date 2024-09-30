from urllib.parse import urljoin
from openai import OpenAI
import os
import requests
from requests import Response


def get_leapfrogai_model() -> str:
    """Get the model to use for LeapfrogAI.

    Returns:
        str: The model to use for LeapfrogAI. (default: "vllm")
    """

    return os.getenv("LEAPFROGAI_MODEL", "vllm")


def get_openai_key() -> str:
    """Get the API key for OpenAI.

    Returns:
        str: The API key for OpenAI.

    Raises:
        ValueError: If OPENAI_API_KEY is not set.
    """

    api_key = os.getenv("OPENAI_API_KEY")
    if api_key is None:
        raise ValueError("OPENAI_API_KEY not set")

    return api_key


def get_openai_model() -> str:
    """Get the model to use for OpenAI.

    Returns:
        str: The model to use for OpenAI. (default: "gpt-4o-mini")
    """

    return os.getenv("OPENAI_MODEL", "gpt-4o-mini")


def get_leapfrogai_api_key() -> str:
    """Get the API key for the LeapfrogAI API.

    Set via the LEAPFROGAI_API_KEY environment variable or the SUPABASE_USER_JWT environment variable in that order.

    Returns:
        str: The API key for the LeapfrogAI API.
    Raises:
        ValueError: If LEAPFROGAI_API_KEY or SUPABASE_USER_JWT is not set.
    """

    api_key = os.getenv("LEAPFROGAI_API_KEY") or os.getenv("SUPABASE_USER_JWT")

    if api_key is None:
        raise ValueError("LEAPFROGAI_API_KEY or SUPABASE_USER_JWT not set")

    return api_key


def get_leapfrogai_api_url() -> str:
    """Get the URL for the LeapfrogAI API.

    Returns:
        str: The URL for the LeapfrogAI API. (default: "https://leapfrogai-api.uds.dev/openai/v1")
    """

    return os.getenv("LEAPFROGAI_API_URL", "https://leapfrogai-api.uds.dev/openai/v1")


def get_leapfrogai_api_url_base() -> str:
    """Get the base URL for the LeapfrogAI API.

    Set via the LEAPFRAGAI_API_URL environment variable.

    If LEAPFRAGAI_API_URL is set to "https://leapfrogai-api.uds.dev/openai/v1", this will trim off the "/openai/v1" part.

    Returns:
        str: The base URL for the LeapfrogAI API. (default: "https://leapfrogai-api.uds.dev")
    """

    url = os.getenv("LEAPFROGAI_API_URL", "https://leapfrogai-api.uds.dev")
    if url.endswith("/openai/v1"):
        return url[:-9]
    return url


def openai_client() -> OpenAI:
    """Create an OpenAI client using the OPENAI_API_KEY.

    returns:
        OpenAI: An OpenAI client.
    """
    return OpenAI(api_key=get_openai_key())


def leapfrogai_client() -> OpenAI:
    """Create an OpenAI client using the LEAPFROGAI_API_URL and LEAPFROGAI_API_KEY or SUPABASE_USER_JWT.

    returns:
        OpenAI: An OpenAI client.
    """
    return OpenAI(
        base_url=get_leapfrogai_api_url(),
        api_key=get_leapfrogai_api_key(),
    )


class ClientConfig:
    """Configuration for a client that is OpenAI compliant."""

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
    """Client for handling queries in the LeapfrogAI namespace that are not handled by the OpenAI SDK.

    Wraps the requests library to make HTTP requests to the LeapfrogAI API.

    Raises:
        requests.HTTPError: If the response status code is not a 2xx status code.
    """

    def __init__(self, base_url: str | None = None, api_key: str | None = None):
        self.base_url = base_url or get_leapfrogai_api_url_base()
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
