import pytest
from openai.types.beta import Thread, Assistant
from openai.types.beta.thread import ToolResources
from openai.types.beta.threads import Message, TextContentBlock, Text
from fastapi.responses import StreamingResponse

from tests.mocks.mock_crud import mock_crud_base
from tests.mocks.mock_session import mock_session
from tests.utils.crud_utils import execute_response_format

from leapfrogai_api.routers.openai.threads import create_thread, create_run
from leapfrogai_api.routers.openai.requests.create_thread_request import CreateThreadRequest
from leapfrogai_api.routers.openai.requests.run_create_params_request import RunCreateParamsRequestBaseRequest

mock_thread = Thread(
    id="",  # Leave blank to have Postgres generate a UUID
    created_at=0,  # Leave blank to have Postgres generate a timestamp
    object="thread"
)

mock_message = Message(
    id="",
    thread_id="",
    created_at=0,
    object="thread.message",
    status="in_progress",
    role="assistant",
    content=[TextContentBlock(text=Text(value="mock-data", annotations=[]), type="text")],
)

@pytest.mark.asyncio
@pytest.mark.parametrize("mock_messages, expected_result", [
    ([mock_message], mock_thread),
    ([mock_message, mock_message], mock_thread)
])
async def test_create_thread(mock_session, mock_crud_base, mock_messages, expected_result):
    mock_tools = ToolResources(code_interpreter=None, file_search=None)
    mock_metadata = None
    mock_data = CreateThreadRequest(
        messages=mock_messages, 
        tool_resources=mock_tools,
        metadata = mock_metadata
    )

    mock_session.table().insert().execute.return_value = execute_response_format(mock_thread.model_dump())

    result = await create_thread(
        request=mock_data, 
        session=mock_session
    )

    assert isinstance(result, Thread)
    assert result == expected_result
    #mock_session.table.assert_called_once_with("table")


@pytest.mark.asyncio
@pytest.mark.parametrize("mock_messages, expected_result", [
    ([mock_message], mock_thread)
])
async def test_create_run(mock_session, mock_crud_base, mock_messages, expected_result):
    mock_thread_id = "1"
    mock_request = RunCreateParamsRequestBaseRequest(
        assistant_id="0"
    )
    mock_assistant = Assistant(
        id = "0",
        created_at = 0,
        model = "mock-data",
        object = "assistant",
        tools = []
    )
    mock_session.table().select().execute.return_value = execute_response_format(mock_assistant.model_dump())

    result = await create_run(
        session=mock_session, 
        thread_id=mock_thread_id,
        request=mock_request
    )

    assert isinstance(result, StreamingResponse)