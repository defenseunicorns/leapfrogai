import asyncio
import json
import logging


import os
import shutil
import httpx

from typing import Any, Callable, Optional, TYPE_CHECKING

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
            backend="localhost:50051",
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
# @pytest_asyncio.fixture
# async def app_with_lifespan():
#     @asynccontextmanager
#     async def lifespan(app):
#         print("Starting up")
#         yield
#         print("Shutting down")

#     async def home(request):
#         return PlainTextResponse("Hello, world!")

#     async with LifespanManager(app) as manager:
#         logging.debug("Lifespan manager created and running")
#         yield manager.app


@pytest_asyncio.fixture
async def test_client():
    app = create_app(testing=True)
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        logging.debug("Test client created and running")
        yield client


class AsyncClient:
    """Supabase client class."""

    def __init__(
        self,
        supabase_url: str,
        supabase_key: str,
        access_token: Optional[str] = None,
        options: ClientOptions = ClientOptions(),
    ):
        self.supabase_url = supabase_url
        self.supabase_key = supabase_key
        self.access_token = access_token
        self.options = options


async def mock_init_supabase_client() -> AsyncClient:
    return AsyncClient("", "", "", ClientOptions())


async def pack_dummy_bearer_token(request: _CachedRequest, call_next):
    request.headers._list.append(
        (
            "authorization".encode(),
            "Bearer dummy".encode(),
        )
    )
    return await call_next(request)


async def wait_for_condition(
    condition: Callable[[], bool], timeout: float = 5.0, interval: float = 0.1
) -> bool:
    start_time = asyncio.get_event_loop().time()
    while asyncio.get_event_loop().time() - start_time < timeout:
        if condition():
            return True
        await asyncio.sleep(interval)
    return False


@pytest.fixture
def auth_client():
    app = create_app(testing=True)
    """Fixture for creating a TestClient instance with dummy auth middleware."""
    # Save the original state of the app
    original_dependency_overrides = app.dependency_overrides.copy()
    original_middleware = app.user_middleware.copy()
    original_middleware_stack = app.middleware_stack

    # Modify the app for the test
    app.dependency_overrides[init_supabase_client] = mock_init_supabase_client
    app.user_middleware.clear()
    app.middleware_stack = None
    app.add_middleware(BaseHTTPMiddleware, dispatch=pack_dummy_bearer_token)
    app.middleware_stack = app.build_middleware_stack()

    try:
        with TestClient(app) as client:
            yield client
    finally:
        # Restore the original state of the app
        app.dependency_overrides = original_dependency_overrides
        app.user_middleware = original_middleware
        app.middleware_stack = original_middleware_stack


@pytest.fixture(scope="function")
def client():
    """Fixture for creating a TestClient instance without additional middleware."""
    app = create_app(testing=True)
    with TestClient(app) as client:
        yield client


@pytest_asyncio.fixture
async def test_app_factory(monkeypatch):
    """Factory fixture for creating an app and config."""

    # NOTE: This primarily existst to make it easy to override env vars / lifespan
    async def _create_app(
        config_path: str | None = None,
        config_filename: str | None = None,
    ) -> tuple["FastAPI", "Config"]:
        config_path = config_path or os.environ.get("LFAI_CONFIG_PATH")
        config_filename = config_filename or os.environ.get("LFAI_CONFIG_FILENAME")
        monkeypatch.setenv("LFAI_CONFIG_PATH", config_path)
        monkeypatch.setenv("LFAI_CONFIG_FILENAME", config_filename)
        config = await Config.create(testing=True)

        lifespan_func = None
        app = create_app(testing=True, lifespan=lifespan_func)
        return app, config

    try:
        yield _create_app
    finally:
        pass


@pytest.mark.anyio
# @pytest.mark.timeout(5, method="thread")
async def test_config_load(test_app_factory):
    """Test that the config is loaded correctly."""
    config_filename = LFAI_CONFIG_FILENAME
    config_path = LFAI_CONFIG_PATH
    model_name = "repeater"

    app, config = await test_app_factory(
        config_path=config_path,
        config_filename=config_filename,
    )
    app.state.config = config

    with TestClient(app=app) as client:
        logger.debug("Created AsyncClient")

        response = client.get(REQUEST_URI)
        logger.debug(f"Received response: {response}")

        result = response.json()
        assert response.status_code == 200

        expected_response: dict[str, dict[str, Any]] = dict(
            config_sources={config_filename: [model_name]},
            **NO_MODEL_METADATA,
        )
        assert (
            expected_response == result
        ), f"Assertions failed due to {expected_response} != {result}"
        logger.debug("Assertions passed")

    logger.debug("AsyncClient context exited")


@pytest.mark.anyio
@pytest.mark.timeout(5, method="thread")
async def test_config_delete(test_app_factory, tmp_path):
    """Test that the config is deleted correctly."""
    config_filename = LFAI_CONFIG_FILENAME
    config_path = tmp_path
    model_name = "repeater"

    # Step 1: Copy the config file to the temporary directory
    tmp_config_filepath = shutil.copyfile(
        LFAI_CONFIG_FILEPATH, tmp_path / config_filename
    )

    app, config = await test_app_factory(str(config_path), config_filename)
    app.state.config = config

    with TestClient(app=app) as client:
        logger.debug("Created AsyncClient")

        # Step 2: Ensure the API loads the temp config
        response = client.get(REQUEST_URI)
        logger.debug(f"Received response: {response}")

        expected_response = {
            "config_sources": {config_filename: [model_name]},
            "models": {
                model_name: {
                    "backend": "localhost:50051",
                    "name": model_name,
                    "metadata": None,
                }
            },
        }
        result = response.json()
        assert response.status_code == 200
        assert (
            expected_response == result
        ), f"Assertions failed due to {expected_response} != {result}"
        logger.debug("Config loaded and assertions passed")

        # Step 3: Delete the source config file from temp dir
        os.remove(tmp_config_filepath)
        logger.debug(f"Deleted config file: {tmp_config_filepath}")

        # Step 4: Wait for the API to detect the change
        await asyncio.sleep(1.0)  # Adjust the sleep time as necessary

        # Step 5: Assert response is now empty
        response = client.get(REQUEST_URI)
        logger.debug(f"Received response after deletion: {response}")
        assert response.status_code == 200
        assert response.json() == {"config_sources": {}, "models": {}}
        logger.debug("Config deletion detected and assertions passed")

    logger.debug("AsyncClient context exited")


@pytest.mark.anyio
async def test_routes(test_app_factory):
    """Test that the expected routes are present."""
    app, config = await test_app_factory()
    app.state.config = config
    app = create_app()
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

        # if path_name is not None and path_name in expected_routes:
        #     assert route.methods == set(expected_routes[path_name])
        #     del expected_routes[path_name]
        # # if hasattr(route, "path") and route.path in expected_routes:
        # #    assert route.methods == set(expected_routes[route.path])
        # #    del expected_routes[route.path]

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


@pytest.mark.anyio
@pytest.mark.asyncio
async def test_healthz(test_client):
    """Test the healthz endpoint."""
    response = await test_client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@SKIP_IF_NO_REPEATER_ENV_VAR
def test_embedding(auth_client):
    """Test the embedding endpoint."""
    expected_embedding = [0.0 for _ in range(10)]

    # Send request to client
    embedding_request = lfai_types.CreateEmbeddingRequest(
        model="repeater",
        input="This is the embedding input text.",
    )
    response = auth_client.post(
        "/openai/v1/embeddings", json=embedding_request.model_dump()
    )
    assert response.status_code == 200

    # parse through the response
    response_obj = response.json()
    assert "data" in response_obj
    assert len(response_obj.get("data")) == 1

    # validate the expected response
    data_obj = response_obj.get("data")[0]
    assert "embedding" in data_obj
    assert data_obj.get("embedding") == expected_embedding


@SKIP_IF_NO_REPEATER_ENV_VAR
def test_chat_completion(auth_client):
    """Test the chat completion endpoint."""
    input_content = "this is the chat completion input."
    chat_completion_request = lfai_types.ChatCompletionRequest(
        model="repeater",
        messages=[lfai_types.ChatMessage(role="user", content=input_content)],
    )
    response = auth_client.post(
        "/openai/v1/chat/completions", json=chat_completion_request.model_dump()
    )
    assert response.status_code == 200

    assert response

    # parse through the chat completion response
    response_obj = response.json()
    assert "choices" in response_obj

    # parse the choices from the response
    response_choices = response_obj.get("choices")
    assert len(response_choices) == 1
    assert "message" in response_choices[0]
    assert "content" in response_choices[0].get("message")

    # parse finish reason
    assert "finish_reason" in response_choices[0]
    assert "stop" == response_choices[0].get("finish_reason")

    # parse usage data
    response_usage = response_obj.get("usage")
    prompt_tokens = response_usage.get("prompt_tokens")
    completion_tokens = response_usage.get("completion_tokens")
    total_tokens = response_usage.get("total_tokens")
    assert prompt_tokens == len(input_content)
    assert completion_tokens == len(input_content)
    assert total_tokens == len(input_content) * 2

    # validate that the repeater repeated
    assert response_choices[0].get("message").get("content") == input_content


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
        "/openai/v1/chat/completions", json=chat_completion_request.model_dump()
    )
    assert response.status_code == 200
    assert response.headers.get("content-type") == "text/event-stream; charset=utf-8"

    # parse through the streamed response
    iter_length = 0
    iter_lines = response.iter_lines()
    for line in iter_lines:
        # skip the empty, and non-data lines
        if ": " in line:
            strings = line.split(": ", 1)

            # Process all the data responses that is not the sig_stop signal
            if strings[0] == "data" and strings[1] != "[DONE]":
                stream_response = json.loads(strings[1])
                assert "choices" in stream_response
                choices = stream_response.get("choices")
                assert len(choices) == 1
                assert "delta" in choices[0]
                assert "content" in choices[0].get("delta")
                assert choices[0].get("delta").get("content") == input_content
                iter_length += 1
                # parse finish reason
                assert "finish_reason" in choices[0]
                assert "stop" == choices[0].get("finish_reason")
                # parse usage data
                response_usage = stream_response.get("usage")
                prompt_tokens = response_usage.get("prompt_tokens")
                completion_tokens = response_usage.get("completion_tokens")
                total_tokens = response_usage.get("total_tokens")
                assert prompt_tokens == len(input_content)
                assert completion_tokens == len(input_content)
                assert total_tokens == len(input_content) * 2

    # The repeater only response with 5 messages
    assert iter_length == 5
