import json
import os
import shutil
import time

import leapfrogai_api.backends.openai.types as lfai_types
import pytest
from fastapi.testclient import TestClient
from leapfrogai_api.main import app

# Set environment variables that the TestClient will use
LFAI_CONFIG_FILENAME = os.environ["LFAI_CONFIG_FILENAME"] = "repeater-test-config.yaml"
LFAI_CONFIG_PATH = os.environ["LFAI_CONFIG_PATH"] = os.path.join(
    os.path.dirname(__file__), "fixtures"
)
LFAI_CONFIG_FILEPATH = os.path.join(LFAI_CONFIG_PATH, LFAI_CONFIG_FILENAME)


#########################
#########################


def test_config_load():
    with TestClient(app) as client:
        response = client.get("/models")

        assert response.status_code == 200
        assert response.json() == {
            "config_sources": {"repeater-test-config.yaml": ["repeater"]},
            "models": {"repeater": {"backend": "localhost:50051", "name": "repeater"}},
        }


def test_config_delete(tmp_path):
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
    expected_routes = {
        "/docs": ["GET", "HEAD"],
        "/healthz": ["GET"],
        "/models": ["GET"],
        "/openai/v1/completions": ["POST"],
        "/openai/v1/chat/completions": ["POST"],
        "/openai/v1/models": ["GET"],
        "/openai/v1/embeddings": ["POST"],
        "/openai/v1/audio/transcriptions": ["POST"],
    }

    actual_routes = app.routes
    for route in actual_routes:
        if hasattr(route, "path") and route.path in expected_routes:
            assert route.methods == set(expected_routes[route.path])
            del expected_routes[route.path]

    assert len(expected_routes) == 0


def test_healthz():
    with TestClient(app) as client:
        response = client.get("/healthz")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


@pytest.mark.skipif(
    os.environ.get("LFAI_RUN_REPEATER_TESTS") != "true",
    reason="LFAI_RUN_REPEATER_TESTS envvar was not set to true",
)
def test_completion():
    with TestClient(app) as client:
        # Send request to client
        input_text = "This is the completion input text."
        completion_request = lfai_types.CompletionRequest(
            model="repeater",
            prompt=input_text,
        )
        response = client.post(
            "/openai/v1/completions", json=completion_request.model_dump()
        )
        assert response.status_code == 200

        # parse through the response
        response_obj = response.json()
        assert "choices" in response_obj

        # parse the choices from the response
        response_choices = response_obj.get("choices")
        assert len(response_choices) == 1
        assert "text" in response_choices[0]

        # validate that the repeater repeated
        assert response_choices[0].get("text") == input_text


@pytest.mark.skipif(
    os.environ.get("LFAI_RUN_REPEATER_TESTS") != "true",
    reason="LFAI_RUN_REPEATER_TESTS envvar was not set to true",
)
def test_embedding():
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
def test_stream_completion():
    with TestClient(app) as client:
        # Send request to client
        input_text = "This is the completion input text."
        stream_completion_request = lfai_types.CompletionRequest(
            model="repeater",
            prompt=input_text,
            stream=True,
        )
        response = client.post(
            "/openai/v1/completions", json=stream_completion_request.model_dump()
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
                    assert "text" in choices[0]
                    assert choices[0].get("text") == input_text
                    iter_length += 1

        # The repeater only response with 5 messages
        assert iter_length == 5


@pytest.mark.skipif(
    os.environ.get("LFAI_RUN_REPEATER_TESTS") != "true",
    reason="LFAI_RUN_REPEATER_TESTS envvar was not set to true",
)
def test_chat_completion():
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

        # validate that the repeater repeated
        assert response_choices[0].get("message").get("content") == input_content


@pytest.mark.skipif(
    os.environ.get("LFAI_RUN_REPEATER_TESTS") != "true",
    reason="LFAI_RUN_REPEATER_TESTS envvar was not set to true",
)
def test_stream_chat_completion():
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

        # The repeater only response with 5 messages
        assert iter_length == 5
