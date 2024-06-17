import pytest
from openai.types.beta import Thread, ThreadDeleted
from openai.types.beta.thread import ToolResources

from tests.mocks.mock_tables import mock_message, mock_thread
from tests.utils.crud_utils import execute_response_format

from leapfrogai_api.routers.openai.requests.create_thread_request import (
    CreateThreadRequest,
)
from leapfrogai_api.backend.types import ModifyThreadRequest

from leapfrogai_api.routers.openai.threads import (
    create_thread,
    retrieve_thread,
    modify_thread,
    delete_thread,
)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "mock_messages, expected_result",
    [([mock_message], mock_thread), ([mock_message, mock_message], mock_thread)],
)
async def test_create_thread(mock_session, mock_messages, expected_result):
    mock_tools = ToolResources(code_interpreter=None, file_search=None)
    mock_metadata = None
    mock_data = CreateThreadRequest(
        messages=mock_messages, tool_resources=mock_tools, metadata=mock_metadata
    )

    mock_session.table().insert().execute.return_value = execute_response_format(
        mock_thread.model_dump()
    )

    result = await create_thread(request=mock_data, session=mock_session)

    assert isinstance(result, Thread)
    assert result == expected_result
    # mock_session.table.assert_called_once_with("table")


@pytest.mark.asyncio
async def test_retrieve_thread(mock_session):
    mock_session.table().select().execute.return_value = execute_response_format(
        mock_thread.model_dump()
    )

    result = await retrieve_thread(thread_id="0", session=mock_session)

    assert isinstance(result, Thread)
    assert mock_session.table.called_with("thread")


@pytest.mark.asyncio
async def test_modify_thread(mock_session):
    mock_session.table().select().execute.return_value = execute_response_format(
        mock_thread.model_dump()
    )
    mock_session.table().update().execute.return_value = execute_response_format(
        mock_thread.model_dump()
    )

    mock_request = ModifyThreadRequest(
        tool_resources=None, metadata=dict(new_data="mock-data")
    )
    result = await modify_thread(
        thread_id="0", request=mock_request, session=mock_session
    )

    assert isinstance(result, Thread)


@pytest.mark.asyncio
async def test_delete_thread(mock_session):
    mock_session.table().delete().execute.return_value = execute_response_format(
        mock_thread.model_dump()
    )

    result = await delete_thread(thread_id="0", session=mock_session)

    assert isinstance(result, ThreadDeleted)
    assert result == ThreadDeleted(id="0", deleted=True, object="thread.deleted")
