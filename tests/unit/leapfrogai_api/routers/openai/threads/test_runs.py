import pytest
from openai.types.beta import Assistant
from fastapi.responses import StreamingResponse

from leapfrogai_api.routers.openai.requests.run_create_params_request import RunCreateParamsRequestBaseRequest
from leapfrogai_api.routers.openai.threads import create_run

from tests.mocks.mock_crud import mock_crud_base
from tests.mocks.mock_session import mock_session
from tests.utils.crud_utils import execute_response_format

from .conftest import mock_message, mock_thread


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



async def test_list_runs():
    pass

async def test_retrieve_run():
    pass

async def test_modify_run():
    pass

async def test_cancel_run():
    pass

async def test_submit_tool_outputs():
    pass