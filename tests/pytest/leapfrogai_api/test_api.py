import asyncio
from dataclasses import dataclass, field
import json
import logging

import os
import shutil

from typing import Any, TYPE_CHECKING

from leapfrogai_api.utils.config import Config

import pytest
import pytest_asyncio

from fastapi.applications import BaseHTTPMiddleware
from fastapi.security import HTTPBearer
from fastapi.testclient import TestClient
from starlette.middleware.base import _CachedRequest
from supabase import ClientOptions
import leapfrogai_api.backend.types as lfai_types

from leapfrogai_api.main import create_app
from leapfrogai_api.routers.supabase_session import init_supabase_client

if TYPE_CHECKING:
    from fastapi import FastAPI

security = HTTPBearer()
logger = logging.getLogger(__name__)

# Set environment variables that the TestClient will use
LFAI_CONFIG_FILENAME = os.environ["LFAI_CONFIG_FILENAME"] = "repeater-test-config.yaml"
LFAI_CONFIG_PATH = os.environ["LFAI_CONFIG_PATH"] = os.path.join(
    os.path.dirname(__file__), "fixtures"
)
LFAI_CONFIG_FILEPATH = os.path.join(LFAI_CONFIG_PATH, LFAI_CONFIG_FILENAME)
# Set reusable variables for test runs
NO_MODEL_METADATA: dict[str, Any] = dict(
    models=dict(
        repeater=dict(
            backend="0.0.0.0:50051",
            name="repeater",
            metadata=None,
        )
    )
)
EMPTY_CONFIG: dict[str, Any] = dict(
    config_sources={},
    models={},
)
REQUEST_URI = "/leapfrogai/v1/models"

# Set pytest markers / fixtures etc.
SKIP_IF_NO_REPEATER_ENV_VAR = pytest.mark.skipif(
    os.environ.get("LFAI_RUN_REPEATER_TESTS") != "true",
    reason="LFAI_RUN_REPEATER_TESTS envvar was not set to true",
)


@pytest.fixture(autouse=True)
def anyio_backend():
    """This is necessary to prevent `watchfiles` from keeping an open thread with anyio"""
    return "asyncio"


#########################
#########################


async def mock_init_supabase_client():
    """Returns a mocked supabase client"""

    @dataclass
    class AsyncClient:
        """Supabase client class."""

        supabase_url: str = ""
        supabase_key: str = ""
        access_token: str | None = None
        options: ClientOptions = field(default_factory=ClientOptions)

    return AsyncClient()


async def pack_dummy_bearer_token(request: _CachedRequest, call_next):
    """Creates a callable that adds a dummy bearer token to the request header"""
    request.headers._list.append(
        (
            "authorization".encode(),
            "Bearer dummy".encode(),
        )
    )
    return await call_next(request)


@pytest.fixture
def auth_client():
    """Creates a client with dummy auth middleware configured"""
    app = create_app(testing=True)
    app.dependency_overrides[init_supabase_client] = mock_init_supabase_client
    app.user_middleware.clear()
    app.middleware_stack = None
    app.add_middleware(BaseHTTPMiddleware, dispatch=pack_dummy_bearer_token)
    app.middleware_stack = app.build_middleware_stack()
    with TestClient(app) as client:
        yield client


@pytest_asyncio.fixture(scope="function")
async def test_app_factory(monkeypatch):
    """Factory fixture for creating an app and config."""

    # NOTE: This primarily existst to make it easy to override env vars / lifespan
    async def _create_app(
        config_path: str | None = None,
        config_filename: str | None = None,
    ) -> tuple["FastAPI", "Config"]:
        if config_path is None:
            config_path = os.environ.get("LFAI_CONFIG_PATH", LFAI_CONFIG_PATH)
        if config_filename is None:
            config_filename = os.environ.get(
                "LFAI_CONFIG_FILENAME", LFAI_CONFIG_FILENAME
            )
        monkeypatch.setenv("LFAI_CONFIG_PATH", config_path)
        monkeypatch.setenv("LFAI_CONFIG_FILENAME", config_filename)
        config = await Config.create(testing=True)
        app = create_app(testing=True, lifespan=None)
        return app, config

    try:
        yield _create_app
    finally:
        pass


@pytest.mark.anyio
async def test_config_load(test_app_factory):
    """Test that the config is loaded correctly."""
    config_path = LFAI_CONFIG_PATH
    model_name = "repeater"

    app, _ = await test_app_factory(
        config_path=config_path,
        config_filename=LFAI_CONFIG_FILENAME,
    )

    with TestClient(app=app) as client:
        response = client.get(REQUEST_URI)

        result = response.json()
        assert response.status_code == 200, response.json()

        expected_response: dict[str, dict[str, Any]] = dict(
            config_sources={LFAI_CONFIG_FILENAME: [model_name]},
            **NO_MODEL_METADATA,
        )
        assert (
            expected_response == result
        ), f"Assertions failed due to {expected_response} != {result}"


@pytest.mark.anyio
async def test_config_delete(test_app_factory, tmp_path):
    """Test that the config is deleted correctly."""

    # Step 1: Copy the config file to the temporary directory
    tmp_config_filepath = shutil.copyfile(
        LFAI_CONFIG_FILEPATH,
        tmp_path / LFAI_CONFIG_FILENAME,
    )
    app, _ = await test_app_factory(
        config_path=str(tmp_path),
        config_filename=LFAI_CONFIG_FILENAME,
    )
    model_name = "repeater"
    expected_response = {
        "config_sources": {LFAI_CONFIG_FILENAME: [model_name]},
        "models": {
            model_name: {
                "backend": "0.0.0.0:50051",
                "name": model_name,
                "metadata": None,
            }
        },
    }

    with TestClient(app=app) as client:
        # Step 2: Ensure the API loads the temp config
        response = client.get(REQUEST_URI)
        result = response.json()
        assert response.status_code == 200, response.json()
        assert (
            expected_response == result
        ), f"Assertions failed due to {expected_response} != {result}"

        # Step 3: Delete the source config file from temp dir
        os.remove(tmp_config_filepath)
        logger.debug(f"Deleted config file: {tmp_config_filepath}")

        # Step 4: Await a context switch to allow the API to detect the change.
        await asyncio.sleep(0.1)

        # Step 5: Make another request that should have no models loaded
        response = client.get(REQUEST_URI)
        logger.debug(f"Received response after deletion: {response}")
        assert response.status_code == 200, response.json()

        assert response.json() == dict(
            config_sources={},
            models={},
        )


@pytest.mark.anyio
async def test_routes(test_app_factory):
    """Test that the expected routes are present."""
    app, _ = await test_app_factory()

    expected_routes = {
        "/docs": ["GET", "HEAD"],
        "/healthz": ["GET"],
        "/leapfrogai/v1/models": ["GET"],
        "/openai/v1/models": ["GET"],
        "/openai/v1/chat/completions": ["POST"],
        "/openai/v1/embeddings": ["POST"],
        "/openai/v1/audio/transcriptions": ["POST"],
        "/openai/v1/files": ["POST"],
        "/openai/v1/assistants": ["POST"],
    }

    openai_routes = [
        ("/openai/v1/files", "upload_file", ["POST"]),
        ("/openai/v1/files", "list_files", ["GET"]),
        ("/openai/v1/files/{file_id}", "retrieve_file", ["GET"]),
        ("/openai/v1/files/{file_id}", "delete_file", ["DELETE"]),
        ("/openai/v1/files/{file_id}/content", "retrieve_file_content", ["GET"]),
        ("/openai/v1/assistants", "create_assistant", ["POST"]),
        ("/openai/v1/assistants", "list_assistants", ["GET"]),
        ("/openai/v1/assistants/{assistant_id}", "retrieve_assistant", ["GET"]),
        ("/openai/v1/assistants/{assistant_id}", "modify_assistant", ["POST"]),
        ("/openai/v1/assistants/{assistant_id}", "delete_assistant", ["DELETE"]),
        ("/openai/v1/vector_stores", "create_vector_store", ["POST"]),
        ("/openai/v1/vector_stores", "list_vector_stores", ["GET"]),
        (
            "/openai/v1/vector_stores/{vector_store_id}",
            "retrieve_vector_store",
            ["GET"],
        ),
        ("/openai/v1/vector_stores/{vector_store_id}", "modify_vector_store", ["POST"]),
        (
            "/openai/v1/vector_stores/{vector_store_id}",
            "delete_vector_store",
            ["DELETE"],
        ),
        (
            "/openai/v1/vector_stores/{vector_store_id}/files",
            "create_vector_store_file",
            ["POST"],
        ),
        (
            "/openai/v1/vector_stores/{vector_store_id}/files",
            "list_vector_store_files",
            ["GET"],
        ),
        (
            "/openai/v1/vector_stores/{vector_store_id}/files/{file_id}",
            "retrieve_vector_store_file",
            ["GET"],
        ),
        (
            "/openai/v1/vector_stores/{vector_store_id}/files/{file_id}",
            "delete_vector_store_file",
            ["DELETE"],
        ),
    ]
    # test the expected routes
    for path, methods in expected_routes.items():
        route = next(  # iterate through the routes to find the route with the expected path, if any
            (r for r in app.routes if getattr(r, "path", None) == path),
            None,
        )
        assert route is not None, f"Route {path} not found."
        assert route.methods == set(methods), f"Methods for {path} do not match."

    for path, name, methods in openai_routes:
        route = next(
            (
                r
                for r in app.routes
                if getattr(r, "path", None) == path and r.name == name
            ),
            None,
        )
        assert route is not None, f"Route {path} with name {name} not found."
        assert route.methods == set(
            methods
        ), f"Methods for {path} with name {name} do not match."


def test_healthz():
    """Test the healthz endpoint."""

    app = create_app(testing=True)
    with TestClient(app) as client:
        response = client.get("/healthz")
    assert response.status_code == 200, response.json()

    assert response.json() == {"status": "ok"}


@SKIP_IF_NO_REPEATER_ENV_VAR
def test_embedding(auth_client):
    """Test the embedding endpoint."""

    # Send request to client
    embedding_request = lfai_types.CreateEmbeddingRequest(
        model="repeater",
        input="This is the embedding input text.",
    )
    response = auth_client.post(
        "/openai/v1/embeddings",
        json=embedding_request.model_dump(),
    )
    response_obj = response.json()
    assert response.status_code == 200, response_obj

    # parse through the response
    assert (data := response_obj.get("data")) is not None, response_obj
    assert len(data) == 1

    # validate the expected response
    data_obj = data[0]  # type: ignore
    assert "embedding" in data_obj
    assert data_obj.get("embedding") == ([0.0] * 10)  # list of 10 floats


@SKIP_IF_NO_REPEATER_ENV_VAR
def test_chat_completion(auth_client):
    """Test the chat completion endpoint."""
    input_content = "this is the chat completion input."
    chat_completion_request = lfai_types.ChatCompletionRequest(
        model="repeater",
        messages=[lfai_types.ChatMessage(role="user", content=input_content)],
    )
    response = auth_client.post(
        "/openai/v1/chat/completions",
        json=chat_completion_request.model_dump(),
    )
    response_obj = response.json()
    assert response.status_code == 200, response_obj

    # parse through the chat completion response
    response_choices: list[dict[str, Any]] = response_obj.get("choices")
    assert response_choices is not None, response_obj
    assert len(response_choices) == 1
    first_choice = response_choices[0]

    assert (response_message := first_choice.get("message")) is not None
    assert (response_content := response_message.get("content")) is not None
    assert first_choice.get("finish_reason") == "stop", first_choice

    # parse usage data
    response_usage = response_obj.get("usage")
    prompt_tokens = response_usage.get("prompt_tokens")
    completion_tokens = response_usage.get("completion_tokens")
    total_tokens = response_usage.get("total_tokens")
    assert prompt_tokens == len(input_content)
    assert completion_tokens == len(input_content)
    assert total_tokens == len(input_content) * 2

    # validate that the repeater repeated
    assert response_content == input_content


@SKIP_IF_NO_REPEATER_ENV_VAR
def test_stream_chat_completion(auth_client):
    """Test the stream chat completion endpoint."""
    input_content = "this is the stream chat completion input."

    chat_completion_request = lfai_types.ChatCompletionRequest(
        model="repeater",
        messages=[lfai_types.ChatMessage(role="user", content=input_content)],
        stream=True,
    )

    response = auth_client.post(
        "/openai/v1/chat/completions",
        json=chat_completion_request.model_dump(),
    )
    assert response.status_code == 200, response.json()

    assert response.headers.get("content-type") == "text/event-stream; charset=utf-8"

    # parse through the streamed response
    iter_length = 0
    iter_lines = response.iter_lines()
    for line in iter_lines:
        # skip the empty, and non-data lines
        if ": " in line:
            # parse through the streamed response
            key, content = line.split(": ", 1)
            # Process all the data responses that is not the sig_stop signal
            if key == "data" and content != "[DONE]":
                # Check the content of the response
                stream_response = json.loads(content)
                assert (choices := stream_response.get("choices")) is not None
                assert len(choices) == 1
                first_choice = choices[0]
                response_usage = stream_response.get("usage")

                # Check the content of the "first choice"
                assert first_choice.get("delta", {}).get("content") == input_content
                iter_length += 1

                # parse finish reason
                assert "stop" == first_choice.get("finish_reason", None), first_choice
                assert response_usage.get("prompt_tokens", 0) == len(input_content)
                assert response_usage.get("completion_tokens", 0) == len(input_content)
                assert response_usage.get("total_tokens", 0) == (len(input_content) * 2)

    # The repeater only response with 5 messages
    assert iter_length == 5
