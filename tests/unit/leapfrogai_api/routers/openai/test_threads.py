import pytest
from unittest.mock import patch
from leapfrogai_api.routers.openai.threads import router
from leapfrogai_api.routers.openai.requests.create_thread_request import (
    CreateThreadRequest,
)
from leapfrogai_api.backend.types import ModifyThreadRequest
from leapfrogai_api.data.crud_thread import CRUDThread
from leapfrogai_api.data.crud_message import CRUDMessage
from openai.types.beta import Thread

from leapfrogai_api.routers.openai.threads import create_thread

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
    mock_create_thread.return_value = mock_thread
    mock_create_messages.return_value = mock_message

    mock_metadata = dict(mockfield="mock-data")

    request = CreateThreadRequest(messages=mock_message_payload, metadata=mock_metadata)
    response = await create_thread(request, mock_session)

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
async def test_retrieve_thread(mock_get, session):
    mock_get.return_value = Thread(id="1", object="thread", messages=[])

    response = await router.retrieve_thread("1", session)

    assert response.id == "1"
    assert response.object == "thread"
    assert response.messages == []


@pytest.mark.asyncio
@patch.object(CRUDThread, "get")
@patch.object(CRUDThread, "update")
async def test_modify_thread(mock_update, mock_get, session):
    mock_get.return_value = Thread(id="1", object="thread", messages=[])
    mock_update.return_value = Thread(id="1", object="thread", messages=[])

    request = ModifyThreadRequest()
    response = await router.modify_thread("1", request, session)

    assert response.id == "1"
    assert response.object == "thread"
    assert response.messages == []


@pytest.mark.asyncio
@patch.object(CRUDThread, "delete")
async def test_delete_thread(mock_delete, session):
    mock_delete.return_value = True

    response = await router.delete_thread("1", session)

    assert response.id == "1"
    assert response.object == "thread.deleted"
    assert response.deleted
