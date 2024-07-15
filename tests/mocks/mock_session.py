import pytest
from unittest.mock import MagicMock, AsyncMock

from tests.utils.crud_utils import execute_response_format
from .mock_tables import (
    mock_assistant,
    mock_thread,
    mock_run,
    mock_message,
    mock_data_model,
    mock_api_key,
)

_mocks_cache = {}


@pytest.fixture
def mock_session():
    session = AsyncMock()

    mock_user = MagicMock()
    mock_user.user = MagicMock()
    mock_user.user.id = "0"
    mock_auth = MagicMock()
    mock_auth.get_user = AsyncMock(return_value=mock_user)
    session.auth = mock_auth

    session.table = MagicMock(side_effect=mock_table)

    return session


def mock_table(table_name=None):
    if table_name in _mocks_cache:
        return _mocks_cache[table_name]

    mock_table = MagicMock()

    mock_data = mock_execute_data(table_name)

    mock_insert = AsyncMock()
    mock_insert.execute.return_value = execute_response_format(mock_data.model_dump())
    mock_table.insert.return_value = mock_insert

    mock_select = AsyncMock()
    mock_select.execute.return_value = execute_response_format([mock_data.model_dump()])
    mock_select.eq = MagicMock(return_value=mock_select)
    mock_table.select.return_value = mock_select

    mock_update = AsyncMock()
    mock_update.execute.return_value = execute_response_format(mock_data.model_dump())
    mock_update.eq = MagicMock(return_value=mock_update)
    mock_table.update.return_value = mock_update

    mock_delete = AsyncMock()
    mock_delete.execute.return_value = execute_response_format(True)
    mock_delete.eq = MagicMock(return_value=mock_delete)
    mock_table.delete.return_value = mock_delete

    _mocks_cache[table_name] = mock_table
    return mock_table


def mock_execute_data(table_name):
    mock_map = dict(
        thread=mock_thread,
        run=mock_run,
        assistant=mock_assistant,
        message=mock_message,
        dummy_table=mock_data_model,
        api_keys=mock_api_key,
    )
    if table_name:
        return mock_map[table_name]
    else:
        return mock_data_model
