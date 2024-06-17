import pytest
from unittest.mock import AsyncMock, patch


@pytest.fixture
async def mock_crud_base():
    with patch(
        "leapfrogai_api.data.crud_message.CRUDBase", autospec=True
    ) as mock_crud_base:
        mock_crud_base.create = AsyncMock()
        mock_crud_base.get = AsyncMock()
        mock_crud_base.list = AsyncMock()
        mock_crud_base.update = AsyncMock()
        mock_crud_base.delete = AsyncMock()

        mock_db = AsyncMock()
        mock_db.auth.return_value.get_user = dict(user=dict(id=0))
        mock_crud_base.db = mock_db

        yield mock_crud_base
