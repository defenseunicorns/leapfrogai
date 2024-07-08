import pytest
from unittest.mock import patch

from leapfrogai_api.routers.openai.runs import (
    create_run,
    # create_thread_and_run,
    # list_runs,
    # retrieve_run,
    # modify_run,
)
from leapfrogai_api.data.crud_run import CRUDRun
from leapfrogai_api.data.crud_thread import CRUDThread
from leapfrogai_api.data.crud_assistant import CRUDAssistant
from leapfrogai_api.data.crud_message import CRUDMessage

from leapfrogai_api.routers.openai.requests.run_create_params_request import (
    RunCreateParamsRequestBaseRequest,
)
from tests.mocks.mock_tables import mock_run, mock_thread, mock_assistant, mock_message


@pytest.mark.asyncio
@patch.object(CRUDMessage, "list")
@patch.object(CRUDAssistant, "get")
@patch.object(CRUDRun, "create")
@patch.object(CRUDThread, "get")
async def test_create_run(
    mock_thread_get,
    mock_run_create,
    mock_assistant_get,
    mock_message_list,
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

    request = RunCreateParamsRequestBaseRequest(
        assistant_id="mock-assistant-id", instructions="mock-data"
    )

    # Test valid run creation
    response = await create_run("thread_id", mock_session, request)

    # Assertions
    assert response == mock_run
    mock_thread_get.assert_called_once_with(filters={"id": "thread_id"})
    mock_run_create.assert_called_once()


# Additional test cases can be added here

# Run the tests
pytest.main()
