import pytest
from unittest.mock import MagicMock, AsyncMock
from pydantic import BaseModel
from tests.utils.crud_utils import MockModel, execute_response_format
from tests.mocks.mock_crud_base import mock_crud_base


class MockModelNoID(BaseModel):
    name: str

class MockModelStrID(BaseModel):
    id: str
    name: str

class MockModelFields(BaseModel):
    id: int
    name: str
    created_at: str = None
    field_name: str = None

mock_data_dict = dict(id=1, name="mock-data")
mock_data_model = MockModel(id=1, name="mock-data")


@pytest.mark.asyncio
@pytest.mark.parametrize("mock_data_object, mock_response, expected_result, expected_call", [
    (mock_data_model, mock_data_dict, mock_data_model, mock_data_dict),
    (MockModelNoID(name="mock-data"), mock_data_dict, mock_data_model, dict(name="mock-data")),
    (MockModelStrID(id="", name="mock-data"), mock_data_dict, mock_data_model, dict(name="mock-data")),
    (MockModelFields(id=1, name="mock-data", created_at="mock-data"), mock_data_dict, mock_data_model, dict(id=1, name="mock-data", field_name=None)),
    (MockModelFields(id=1, name="mock-data", field_name="mock-data"), mock_data_dict, mock_data_model, dict(id=1, name="mock-data", field_name="mock-data")),
    (mock_data_model, None, None, mock_data_dict),
    ({}, None, None, None),
    (None, None, None, None)
])
async def test_create(mock_crud_base, mock_data_object, mock_response, expected_result, expected_call):
    mock_crud_base.db.table().insert().execute.return_value = execute_response_format(mock_response)

    result = await mock_crud_base.create(mock_data_object)

    assert result == expected_result

    if expected_call:
        mock_crud_base.db.table.return_value.insert.assert_called_with(expected_call)


@pytest.mark.asyncio
@pytest.mark.parametrize("filters, mock_response, expected_result", [
    ({"id": 1}, dict(id=1,name="mock-data"), MockModel(id=1,name="mock-data")),
    ({"id": 1}, [], None),
    ({"id": 1}, {}, None),
    ({"id": 1}, None, None),
    ({}, None, None),
    (None, None, None)
])
async def test_get(mock_crud_base, filters, mock_response, expected_result):
    mock_crud_base.db.table().select().execute.return_value = execute_response_format(mock_response)

    result = await mock_crud_base.get(filters)

    if expected_result:
        assert result == expected_result
    else:
        assert result is None


@pytest.mark.asyncio
async def test_list(mock_crud_base):
    Mock_list = await mock_crud_base.list({})
    assert len(Mock_list) == 1
    assert Mock_list[0].id == 1
    assert Mock_list[0].name == "mock-data"

@pytest.mark.asyncio
async def test_update(mock_crud_base):
    Mock_model_instance = MockModel(id=1, name="updated-data")
    mock_crud_base.db.table().update().execute.return_value = execute_response_format(Mock_model_instance.model_dump())
    updated_Mock = await mock_crud_base.update("1", Mock_model_instance)
    assert updated_Mock == Mock_model_instance

@pytest.mark.asyncio
async def test_delete(mock_crud_base):
    result = await mock_crud_base.delete({"id": 1})
    assert result is True