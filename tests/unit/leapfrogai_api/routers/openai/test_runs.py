import pytest
from unittest.mock import patch

from starlette.responses import StreamingResponse

from leapfrogai_api.routers.openai.runs import (
    create_run,
    # create_thread_and_run,
    # list_runs,
    # retrieve_run,
    # modify_run,
)
from leapfrogai_api.backend.types import ChatCompletionResponse, ChatChoice, ChatMessage
from leapfrogai_api.data.crud_run import CRUDRun
from leapfrogai_api.data.crud_thread import CRUDThread
from leapfrogai_api.data.crud_assistant import CRUDAssistant
from leapfrogai_api.data.crud_message import CRUDMessage
from leapfrogai_api.routers.openai.requests.run_create_params_request import (
    RunCreateParamsRequest,
)
from tests.mocks.mock_tables import mock_run, mock_thread, mock_assistant, mock_message


@pytest.mark.asyncio
@patch("leapfrogai_api.routers.openai.chat.chat_completion")
@patch.object(CRUDMessage, "list")
@patch.object(CRUDAssistant, "get")
@patch.object(CRUDRun, "create")
@patch.object(CRUDThread, "get")
async def test_create_run(
    mock_thread_get,
    mock_run_create,
    mock_assistant_get,
    mock_message_list,
    mock_chat_completion,
    mock_session,
):
    # Setup
    mock_thread_get.return_value = mock_thread
    mock_run_create.return_value = mock_run
    mock_assistant_get.return_value = mock_assistant
    mock_message_list.return_value = [mock_message]

    mock_complete_data = ChatChoice(
        message=ChatMessage(role="user", content="mock-data")
    )
    mock_chat_completion.return_value = ChatCompletionResponse(
        choices=[mock_complete_data]
    )

    request = RunCreateParamsRequest()

    # Test valid run creation
    response = await create_run("thread_id", mock_session, request)

    # Assertions
    assert response == mock_run
    mock_thread_get.assert_called_once_with(filters={"id": "thread_id"})
    mock_run_create.assert_called_once()
    mock_chat_completion.assert_called_once()


@pytest.mark.asyncio
@patch("leapfrogai_api.routers.openai.chat.stream_chat_completion_raw")
@patch.object(CRUDMessage, "update")
@patch.object(CRUDMessage, "list")
@patch.object(CRUDAssistant, "get")
@patch.object(CRUDRun, "create")
@patch.object(CRUDThread, "get")
async def test_create_run_stream(
    mock_thread_get,
    mock_run_create,
    mock_assistant_get,
    mock_message_list,
    mock_message_update,
    mock_stream_chat_completion,
    mock_session,
):
    mock_thread_get.return_value = mock_thread
    mock_run_create.return_value = mock_run
    mock_assistant_get.return_value = mock_assistant
    mock_message_list.return_value = [mock_message]
    mock_message_update.return_value = mock_message

    request = RunCreateParamsRequest(stream=True)

    response = await create_run("thread_id", mock_session, request)
    assert isinstance(response, StreamingResponse)

    results = []

    async def mock_receive():
        return {"type": "http.disconnect"}

    async def mock_send(message):
        if message["type"] == "http.response.body":
            results.append(message["body"])

    # Simulate the ASGI call
    try:
        await response(scope={"type": "http"}, receive=mock_receive, send=mock_send)
    except ConnectionResetError:
        # Expected when all data has been sent
        pass

    mock_thread_get.assert_called_once_with(filters={"id": "thread_id"})
    mock_run_create.assert_called_once()
    mock_stream_chat_completion.assert_called_once()

    # TODD: Figure out which aspects of return message to test for
    assert len(results) == 16
