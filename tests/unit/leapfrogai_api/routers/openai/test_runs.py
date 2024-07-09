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
    RunCreateParamsRequestBaseRequest,
)
from tests.mocks.mock_tables import mock_run, mock_thread, mock_assistant, mock_message


@pytest.mark.asyncio
@patch("leapfrogai_api.routers.openai.chat.chat_completion")
# @patch('leapfrogai_api.routers.openai.chat.stream_chat_completion')
# @patch('leapfrogai_api.routers.openai.chat.stream_chat_completion_raw')
@patch.object(CRUDMessage, "list")
@patch.object(CRUDAssistant, "get")
@patch.object(CRUDRun, "create")
@patch.object(CRUDThread, "get")
async def test_create_run(
    mock_thread_get,
    mock_run_create,
    mock_assistant_get,
    mock_message_list,
    # mock_stream_chat_completion_raw,
    # mock_stream_chat_completion,
    mock_chat_completion,
    mock_session,
):
    # to test: tools, tool_choice
    # mock: QueryService.query_rag : SingleAPIResponse[RAGResponse]
    # grpc.aio.insecure_channel(model.backend): grpc.Channel
    # grpc.aio.UnaryStreamCall.wait_for_connection()
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

    request = RunCreateParamsRequestBaseRequest()

    # Test valid run creation
    response = await create_run("thread_id", mock_session, request)

    # Assertions
    assert response == mock_run
    mock_thread_get.assert_called_once_with(filters={"id": "thread_id"})
    mock_run_create.assert_called_once()
    mock_chat_completion.assert_called_once()


@pytest.mark.asyncio
# @patch("leapfrogai_api.routers.openai.chat.chat_completion")
# @patch('leapfrogai_api.routers.openai.chat.stream_chat_completion')
@patch("leapfrogai_api.routers.openai.chat.stream_chat_completion_raw")
@patch.object(CRUDMessage, "list")
@patch.object(CRUDAssistant, "get")
@patch.object(CRUDRun, "create")
@patch.object(CRUDThread, "get")
async def test_create_run_stream(
    mock_thread_get,
    mock_run_create,
    mock_assistant_get,
    mock_message_list,
    # mock_stream_chat_completion_raw,
    mock_stream_chat_completion,
    # mock_chat_completion,
    mock_session,
):
    mock_thread_get.return_value = mock_thread
    mock_run_create.return_value = mock_run
    mock_assistant_get.return_value = mock_assistant
    mock_message_list.return_value = [mock_message]

    request = RunCreateParamsRequestBaseRequest(stream=True)

    # mock_stream_response = StreamingResponse(content=b"mock-data")
    # mock_stream_chat_completion.return_value = mock_stream_response

    # Test valid run creation
    response = await create_run("thread_id", mock_session, request)

    response_data = []
    async for chunk in response.iter_chunks():
        response_data.append(chunk)

    # Assertions
    assert isinstance(response, StreamingResponse)
    mock_thread_get.assert_called_once_with(filters={"id": "thread_id"})
    mock_run_create.assert_called_once()
    mock_stream_chat_completion.assert_called_once()
    # mock_chat_completion.assert_not_called()
