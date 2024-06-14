import pytest

from openai.types.beta.thread_create_and_run_params import Thread as ThreadCreateAndRunsThread
from openai.types.beta.threads import Run
from fastapi.responses import StreamingResponse

from .conftest import mock_message, mock_thread, mock_assistant, mock_run
from tests.mocks.mock_crud import mock_crud_base
from tests.mocks.mock_session import mock_session
from tests.utils.crud_utils import execute_response_format

from leapfrogai_api.routers.openai.requests.thread_run_create_params_request import ThreadRunCreateParamsRequestBaseRequest
from leapfrogai_api.routers.openai.requests.run_create_params_request import RunCreateParamsRequestBaseRequest

from leapfrogai_api.routers.openai.threads import create_run, create_thread_and_run, list_runs


@pytest.mark.asyncio
@pytest.mark.parametrize("mock_messages, expected_result", [
    ([mock_message], mock_thread)
])
async def test_create_run(mock_session, mock_crud_base, mock_messages, expected_result):
    mock_thread_id = "1"
    mock_request = RunCreateParamsRequestBaseRequest(
        assistant_id="0"
    )
    
    mock_session.table().select().execute.return_value = execute_response_format(mock_assistant.model_dump())

    result = await create_run(
        session=mock_session, 
        thread_id=mock_thread_id,
        request=mock_request
    )

    assert isinstance(result, StreamingResponse)


@pytest.mark.asyncio
async def test_create_thread_and_run(mock_session, mock_crud_base):
    #mock_data = ThreadCreateAndRunsThread(messages=[mock_message])
    mock_request = ThreadRunCreateParamsRequestBaseRequest()

    mock_session.table().select().execute.return_value = execute_response_format(mock_assistant.model_dump())
    mock_session.table().insert().execute.return_value = execute_response_format(mock_thread.model_dump())
    

    result = await create_thread_and_run(
        session = mock_session,
        request = mock_request
    )

    assert isinstance(result, Run)


@pytest.mark.asyncio
async def test_list_runs(mock_session, mock_crud_base):
    
    mock_session.table().select().execute.return_value = execute_response_format(mock_run.model_dump())

    result = await list_runs(
        session = mock_session,
        thread_id = "mock-data"
    )

    assert isinstance(result, list)


async def test_retrieve_run():
    pass


async def test_modify_run():
    pass


async def test_cancel_run():
    pass


async def test_submit_tool_outputs():
    pass