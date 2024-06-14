import pytest
from openai.types.beta import Thread
from openai.types.beta.thread import ToolResources

from tests.mocks.mock_crud import mock_crud_base
from tests.mocks.mock_session import mock_session
from tests.utils.crud_utils import execute_response_format

from leapfrogai_api.routers.openai.threads import create_thread
from leapfrogai_api.routers.openai.requests.create_thread_request import CreateThreadRequest

from .conftest import mock_message, mock_thread

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


async def test_create_thread_and_run():
    pass


async def test_retrieve_thread():
    pass

async def test_modify_thread():
    pass

async def test_delete_thread():
    pass

