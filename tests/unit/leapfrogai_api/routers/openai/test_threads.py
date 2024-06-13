import pytest
from unittest.mock import MagicMock, AsyncMock
from openai.types.beta import Thread
from openai.types.beta.thread import ToolResources
from openai.types.beta.threads import Message, TextContentBlock, Text

from tests.mocks.mock_crud import mock_crud_base
from tests.mocks.mock_session import mock_session
from tests.utils.crud_utils import MockModel, execute_response_format

from leapfrogai_api.routers.openai.threads import create_thread
from leapfrogai_api.routers.openai.requests.create_thread_request import CreateThreadRequest


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
    ([mock_message], mock_thread)
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

    result = await create_thread(mock_data, mock_session)

    assert isinstance(result, Thread)
    assert result == expected_result
