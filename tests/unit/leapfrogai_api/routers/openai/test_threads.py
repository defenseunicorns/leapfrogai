import pytest
from unittest.mock import patch
import copy
from fastapi import HTTPException, status

from openai.types.beta.thread import (
    ToolResources,
    ToolResourcesCodeInterpreter,
    ToolResourcesFileSearch,
)

from leapfrogai_api.typedef.threads import ModifyThreadRequest, CreateThreadRequest
from leapfrogai_api.data.crud_thread import CRUDThread
from leapfrogai_api.data.crud_message import CRUDMessage
from leapfrogai_api.routers.openai.threads import (
    create_thread,
    retrieve_thread,
    modify_thread,
    delete_thread,
)

from tests.mocks.mock_tables import mock_message, mock_thread


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "mock_message_payload", [[], [mock_message], [mock_message, mock_message]]
)
@patch.object(CRUDThread, "create")
@patch.object(CRUDMessage, "create")
async def test_create_thread(
    mock_create_messages, mock_create_thread, mock_message_payload, mock_session
):
    # Prep mock data
    mock_create_thread.return_value = mock_thread
    mock_create_messages.return_value = mock_message

    mock_metadata = dict(mockfield="mock-data")

    request = CreateThreadRequest(messages=mock_message_payload, metadata=mock_metadata)

    # Make the test call
    response = await create_thread(request, mock_session)

    # Verify response
    assert response.id == "1"
    assert response.object == "thread"

    # Check if CRUDThread.create was called with our mock-data passed through
    mock_create_thread.assert_called_once()
    _, kwargs = mock_create_thread.call_args
    assert kwargs["object_"].metadata["mockfield"] == "mock-data"

    # Check if CRUDMessage.create was called N times
    assert mock_create_messages.call_count == len(mock_message_payload)

    # Verify each call to CRUDMessage.create was with the expected message
    for idx, call in enumerate(mock_create_messages.call_args_list):
        _, kwargs = call
        # assert kwargs["object_"] == mock_message_payload[idx]
        assert kwargs["object_"].metadata == mock_metadata
        assert kwargs["object_"].content == mock_message_payload[idx].content


@pytest.mark.asyncio
@patch.object(CRUDThread, "get")
async def test_retrieve_thread(mock_get, mock_session):
    # prep mock data
    mock_get.return_value = mock_thread

    # make test call
    response = await retrieve_thread(mock_thread.id, mock_session)

    # verify response
    assert response == mock_thread

    mock_get.assert_called_once_with(filters={"id": mock_thread.id})


mock_resource_code_interpreter = ToolResourcesCodeInterpreter(file_ids=["mock-data"])
mock_resource_file_search = ToolResourcesFileSearch(vector_store_ids=["mock-data"])


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "mock_tool_resource",
    [
        None,
        ToolResources(),
        ToolResources(code_interpreter=None, file_search=mock_resource_file_search),
    ],
)
@patch.object(CRUDThread, "get")
@patch.object(CRUDThread, "update")
async def test_modify_thread(
    mock_thread_update, mock_thread_get, mock_tool_resource, mock_session
):
    mock_thread_get.return_value = mock_thread

    mock_thread_update_return = copy.deepcopy(mock_thread)
    mock_thread_update.return_value = mock_thread_update_return

    mock_metadata = dict(mockfield="mock-data")
    request = ModifyThreadRequest()
    request.metadata = mock_thread_update_return.metadata = mock_metadata
    request.tool_resources = mock_thread_update_return.tool_resources = (
        mock_tool_resource
    )

    response = await modify_thread(mock_thread.id, request, mock_session)

    assert response == mock_thread_update_return

    mock_thread_get.assert_called_once_with(filters={"id": mock_thread.id})
    mock_thread_update.assert_called_once()
    _, kwargs = mock_thread_update.call_args
    assert kwargs["object_"].metadata == mock_metadata
    assert kwargs["object_"].tool_resources == mock_tool_resource


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "mock_tool_resource, mock_get_response, mock_update_response, expected_status_code",
    [
        # invalid tool resource
        (
            ToolResources(code_interpreter=mock_resource_code_interpreter),
            None,
            None,
            status.HTTP_400_BAD_REQUEST,
        ),
        # invalid tool resource
        (
            ToolResources(code_interpreter=dict(mock="data")),
            None,
            None,
            status.HTTP_400_BAD_REQUEST,
        ),
        # no CRUDThread.get response
        (
            ToolResources(),
            None,
            None,
            status.HTTP_404_NOT_FOUND,
        ),
        # no CRUDThread.update response
        (
            ToolResources(),
            mock_thread,
            None,
            status.HTTP_500_INTERNAL_SERVER_ERROR,
        ),
    ],
)
@patch.object(CRUDThread, "update")
@patch.object(CRUDThread, "get")
async def test_modify_thread_fail(
    mock_thread_get,
    mock_thread_update,
    mock_tool_resource,
    mock_get_response,
    mock_update_response,
    expected_status_code,
    mock_session,
):
    mock_thread_get.return_value = mock_get_response
    mock_thread_update.return_value = mock_update_response

    request = ModifyThreadRequest()
    request.tool_resources = mock_tool_resource

    with pytest.raises(HTTPException) as exc_info:
        await modify_thread(mock_thread.id, request, mock_session)

    assert exc_info.value.status_code == expected_status_code


@pytest.mark.asyncio
@patch.object(CRUDThread, "delete")
async def test_delete_thread(mock_thread_delete, mock_session):
    mock_thread_delete.return_value = True

    response = await delete_thread("1", mock_session)

    assert response.id == "1"
    assert response.object == "thread.deleted"
    assert response.deleted
