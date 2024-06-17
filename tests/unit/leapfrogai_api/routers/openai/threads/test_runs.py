import pytest
from unittest.mock import AsyncMock

from openai.types.beta.threads import Run
from fastapi.responses import StreamingResponse

from tests.mocks.mock_tables import mock_thread, mock_assistant, mock_run
from tests.utils.crud_utils import execute_response_format

from leapfrogai_api.routers.openai.requests.thread_run_create_params_request import ThreadRunCreateParamsRequestBaseRequest
from leapfrogai_api.routers.openai.runs import create_run, create_thread_and_run, list_runs


@pytest.mark.asyncio
async def test_create_run(mock_session):
    # Create run
    #     await self.update_with_assistant_data(session)
    #           assistant: Assistant | None = await crud_assistant.get(
    #     await self.create_additional_messages(session, thread_id)
    # thread.get
    # request.generate_response


    mock_thread_id = "1"
    mock_request = AsyncMock()
    mock_request.tools = False
    mock_request.generate_response = AsyncMock(return_value=mock_run)

    #TODO: mock with side_effect
    mock_session.table().select().execute.return_value = execute_response_format(mock_assistant.model_dump())
    mock_session.table().select().execute.return_value = execute_response_format(mock_thread.model_dump())
    mock_session.table().insert().execute.return_value = execute_response_format(mock_run.model_dump())

    result = await create_run(
        session=mock_session, 
        thread_id=mock_thread_id,
        request=mock_request
    )

    assert isinstance(result, StreamingResponse)


@pytest.mark.asyncio
async def test_create_thread_and_run(mock_session):
    #mock_data = Thread(messages=[mock_message])
    mock_request = ThreadRunCreateParamsRequestBaseRequest()

    mock_session.table().select().execute.return_value = execute_response_format(mock_assistant.model_dump())
    mock_session.table().insert().execute.return_value = execute_response_format(mock_thread.model_dump())
    

    result = await create_thread_and_run(
        session = mock_session,
        request = mock_request
    )

    assert isinstance(result, Run)


@pytest.mark.asyncio
async def test_list_runs(mock_session):
    
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