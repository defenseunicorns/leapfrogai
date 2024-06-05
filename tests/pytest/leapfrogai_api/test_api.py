import json
import os
import shutil
import time
from typing import Optional

import pytest
from fastapi.applications import BaseHTTPMiddleware
from fastapi.security import HTTPBearer
from fastapi.testclient import TestClient
from starlette.middleware.base import _CachedRequest
from supabase_py_async.lib.client_options import ClientOptions
import leapfrogai_api.backend.types as lfai_types
from leapfrogai_api.main import app
from leapfrogai_api.routers.supabase_session import init_supabase_client

security = HTTPBearer()

# Set environment variables that the TestClient will use
LFAI_CONFIG_FILENAME = os.environ["LFAI_CONFIG_FILENAME"] = "repeater-test-config.yaml"
LFAI_CONFIG_PATH = os.environ["LFAI_CONFIG_PATH"] = os.path.join(
    os.path.dirname(__file__), "fixtures"
)
LFAI_CONFIG_FILEPATH = os.path.join(LFAI_CONFIG_PATH, LFAI_CONFIG_FILENAME)


#########################
#########################


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


@pytest.fixture
def dummy_auth_middleware():
    app.dependency_overrides[init_supabase_client] = mock_init_supabase_client
    app.user_middleware.clear()
    app.middleware_stack = None
    app.add_middleware(BaseHTTPMiddleware, dispatch=pack_dummy_bearer_token)
    app.middleware_stack = app.build_middleware_stack()


def test_config_load():
    """Test that the config is loaded correctly."""
    with TestClient(app) as client:
        response = client.get("/models")

        assert response.status_code == 200
        assert response.json() == {
            "config_sources": {"repeater-test-config.yaml": ["repeater"]},
            "models": {"repeater": {"backend": "localhost:50051", "name": "repeater"}},
        }


def test_config_delete(tmp_path):
    """Test that the config is deleted correctly."""
    # move repeater-test-config.yaml to temp dir so that we can remove it at a later step
    tmp_config_filepath = shutil.copyfile(
        LFAI_CONFIG_FILEPATH, os.path.join(tmp_path, LFAI_CONFIG_FILENAME)
    )
    os.environ["LFAI_CONFIG_PATH"] = str(tmp_path)

    with TestClient(app) as client:
        # ensure the API loads the temp config
        response = client.get("/models")
        assert response.status_code == 200

        assert response.json() == {
            "config_sources": {"repeater-test-config.yaml": ["repeater"]},
            "models": {"repeater": {"backend": "localhost:50051", "name": "repeater"}},
        }
        # delete source config from temp dir
        os.remove(tmp_config_filepath)

        # wait for the api to be able to detect the change
        time.sleep(0.5)
        # assert response is now empty
        response = client.get("/models")
        assert response.status_code == 200
        assert response.json() == {"config_sources": {}, "models": {}}

    os.environ["LFAI_CONFIG_PATH"] = os.path.join(os.path.dirname(__file__), "fixtures")


def test_routes():
    """Test that the expected routes are present."""
    expected_routes = {
        "/docs": ["GET", "HEAD"],
        "/healthz": ["GET"],
        "/models": ["GET"],
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
    ]

    actual_routes = app.routes
    for route in actual_routes:
        if hasattr(route, "path") and route.path in expected_routes:
            assert route.methods == set(expected_routes[route.path])
            del expected_routes[route.path]

    for route, name, methods in openai_routes:
        found = False
        for actual_route in actual_routes:
            if (
                hasattr(actual_route, "path")
                and actual_route.path == route
                and actual_route.name == name
            ):
                assert actual_route.methods == set(methods)
                found = True
                break
        assert found, f"Missing route: {route}, {name}, {methods}"

    assert len(expected_routes) == 0


def test_healthz():
    """Test the healthz endpoint."""
    with TestClient(app) as client:
        response = client.get("/healthz")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


@pytest.mark.skipif(
    os.environ.get("LFAI_RUN_REPEATER_TESTS") != "true",
    reason="LFAI_RUN_REPEATER_TESTS envvar was not set to true",
)
def test_embedding(dummy_auth_middleware):
    """Test the embedding endpoint."""
    expected_embedding = [0.0 for _ in range(10)]

    with TestClient(app) as client:
        # Send request to client
        embedding_request = lfai_types.CreateEmbeddingRequest(
            model="repeater",
            input="This is the embedding input text.",
        )
        response = client.post(
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


@pytest.mark.skipif(
    os.environ.get("LFAI_RUN_REPEATER_TESTS") != "true",
    reason="LFAI_RUN_REPEATER_TESTS envvar was not set to true",
)
def test_chat_completion(dummy_auth_middleware):
    """Test the chat completion endpoint."""
    with TestClient(app) as client:
        input_content = "this is the chat completion input."
        chat_completion_request = lfai_types.ChatCompletionRequest(
            model="repeater",
            messages=[lfai_types.ChatMessage(role="user", content=input_content)],
        )
        response = client.post(
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


@pytest.mark.skipif(
    os.environ.get("LFAI_RUN_REPEATER_TESTS") != "true",
    reason="LFAI_RUN_REPEATER_TESTS envvar was not set to true",
)
def test_stream_chat_completion(dummy_auth_middleware):
    """Test the stream chat completion endpoint."""
    with TestClient(app) as client:
        input_content = "this is the stream chat completion input."

        chat_completion_request = lfai_types.ChatCompletionRequest(
            model="repeater",
            messages=[lfai_types.ChatMessage(role="user", content=input_content)],
            stream=True,
        )

        response = client.post(
            "/openai/v1/chat/completions", json=chat_completion_request.model_dump()
        )
        assert response.status_code == 200
        assert (
            response.headers.get("content-type") == "text/event-stream; charset=utf-8"
        )

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
