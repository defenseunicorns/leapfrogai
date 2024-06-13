import pytest
from unittest.mock import MagicMock, AsyncMock
from tests.utils.crud_utils import MockModel, execute_response_format

@pytest.fixture
def mock_session():
    session = AsyncMock()

    mock_user = MagicMock()
    mock_user.user = MagicMock()
    mock_user.user.id = "0"
    mock_auth = MagicMock()
    mock_auth.get_user = AsyncMock(return_value=mock_user)
    
    session.auth = mock_auth

    mock_table = MagicMock()
    session.table = MagicMock(return_value=mock_table)

    mock_data = dict(id=1, name="mock-data")

    mock_insert = AsyncMock()
    mock_insert.execute.return_value = execute_response_format(mock_data)
    mock_table.insert.return_value = mock_insert

    mock_select = AsyncMock()
    mock_select.execute.return_value = execute_response_format(mock_data)
    mock_select.eq = MagicMock(return_value = mock_select)
    mock_table.select.return_value = mock_select

    mock_update = AsyncMock()
    mock_update.execute.return_value = execute_response_format(mock_data)
    mock_update.eq = MagicMock(return_value = mock_update)
    mock_table.update.return_value = mock_update

    mock_delete = AsyncMock()
    mock_delete.execute.return_value = execute_response_format(True)
    mock_delete.eq = MagicMock(return_value = mock_delete)
    mock_table.delete.return_value = mock_delete

    return session