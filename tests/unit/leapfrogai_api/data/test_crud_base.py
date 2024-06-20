import pytest
from pydantic import BaseModel
from tests.utils.crud_utils import execute_response_format
from tests.mocks.mock_tables import mock_data_model, MockModel

from src.leapfrogai_api.data.crud_base import CRUDBase


class MockModelNoID(BaseModel):
    name: str


class MockModelStrID(BaseModel):
    id: str
    name: str


class MockModelFields(BaseModel):
    id: int
    name: str
    created_at: int | str = None
    field_name: str = None


mock_data_dict = dict(id=1, name="mock-data")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "mock_data_object, mock_response, expected_result, expected_call",
    [
        (mock_data_model, mock_data_dict, mock_data_model, mock_data_dict),
        (
            MockModelNoID(name="mock-data"),
            mock_data_dict,
            mock_data_model,
            dict(name="mock-data"),
        ),
        (
            MockModelStrID(id="", name="mock-data"),
            mock_data_dict,
            mock_data_model,
            dict(name="mock-data"),
        ),
        (
            MockModelFields(id=1, name="mock-data", created_at=0),
            mock_data_dict,
            mock_data_model,
            dict(id=1, name="mock-data", field_name=None),
        ),
        (
            MockModelFields(id=1, name="mock-data", created_at="mock-data"),
            mock_data_dict,
            mock_data_model,
            dict(id=1, name="mock-data", field_name=None),
        ),
        (
            MockModelFields(id=1, name="mock-data"),
            mock_data_dict,
            mock_data_model,
            dict(id=1, name="mock-data"),
        ),
        (
            MockModelFields(
                id=1, name="mock-data", created_at=0, field_name="mock-data"
            ),
            mock_data_dict,
            mock_data_model,
            dict(id=1, name="mock-data", field_name="mock-data"),
        ),
    ],
)
async def test_create(
    mock_session, mock_data_object, mock_response, expected_result, expected_call
):
    mock_crud_base = CRUDBase(
        db=mock_session, model=MockModel, table_name="dummy_table"
    )
    mock_table = mock_session.table(mock_crud_base.table_name)
    mock_table.insert().execute.return_value = execute_response_format(mock_response)

    result = await mock_crud_base.create(mock_data_object)

    assert result == expected_result
    mock_session.table.assert_called_with(mock_crud_base.table_name)
    if expected_call:
        mock_table.insert.assert_called_with(expected_call)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "mock_data_object, mock_response",
    [(mock_data_model, {}), (mock_data_model, []), (mock_data_model, None)],
)
async def test_create_fail(mock_session, mock_data_object, mock_response):
    mock_crud_base = CRUDBase(
        db=mock_session, model=MockModel, table_name="dummy_table"
    )
    mock_table = mock_session.table(mock_crud_base.table_name)
    mock_table.insert().execute.return_value = execute_response_format(mock_response)

    with pytest.raises(RuntimeError):
        await mock_crud_base.create(mock_data_object)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "filters, mock_response, expected_result",
    [({"id": 1}, dict(id=1, name="mock-data"), MockModel(id=1, name="mock-data"))],
)
async def test_get(mock_session, filters, mock_response, expected_result):
    mock_crud_base = CRUDBase(
        db=mock_session, model=MockModel, table_name="dummy_table"
    )
    mock_table = mock_session.table(mock_crud_base.table_name)
    mock_table.select().execute.return_value = execute_response_format(mock_response)

    result = await mock_crud_base.get(filters)

    if expected_result:
        assert result == expected_result
    else:
        assert result is None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "filters, mock_response",
    [({"id": 1}, []), ({"id": 1}, {}), ({"id": 1}, None), ({}, None), (None, None)],
)
async def test_get_fail(mock_session, filters, mock_response):
    mock_crud_base = CRUDBase(
        db=mock_session, model=MockModel, table_name="dummy_table"
    )
    mock_table = mock_session.table(mock_crud_base.table_name)
    mock_table.select().execute.return_value = execute_response_format(mock_response)

    with pytest.raises(RuntimeError):
        await mock_crud_base.get(filters)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "filters, mock_response, expected_result",
    [
        ({"id": 1}, dict(id=1, name="mock-data"), [MockModel(id=1, name="mock-data")]),
        (
            {"id": 1},
            [dict(id=1, name="mock-data"), dict(id=2, name="mock-data")],
            [MockModel(id=1, name="mock-data"), MockModel(id=2, name="mock-data")],
        ),
        ({"id": 1}, [], None),
    ],
)
async def test_list(mock_session, filters, mock_response, expected_result):
    mock_crud_base = CRUDBase(
        db=mock_session, model=MockModel, table_name="dummy_table"
    )
    mock_table = mock_session.table(mock_crud_base.table_name)
    mock_table.select().execute.return_value = execute_response_format(mock_response)

    result = await mock_crud_base.list(filters)

    assert result == expected_result


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "filters, mock_response",
    [({"id": 1}, {}), ({"id": 1}, None), ({}, None), (None, None)],
)
async def test_list_fail(mock_session, filters, mock_response):
    mock_crud_base = CRUDBase(
        db=mock_session, model=MockModel, table_name="dummy_table"
    )
    mock_table = mock_session.table(mock_crud_base.table_name)
    mock_table.select().execute.return_value = execute_response_format(mock_response)

    with pytest.raises(RuntimeError):
        await mock_crud_base.get(filters)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "mock_response, expected_result", [(mock_data_model, mock_data_model)]
)
async def test_update(mock_session, mock_response, expected_result):
    mock_crud_base = CRUDBase(
        db=mock_session, model=MockModel, table_name="dummy_table"
    )
    mock_table = mock_session.table(mock_crud_base.table_name)
    mock_table.update().execute.return_value = execute_response_format(
        mock_response.model_dump()
    )

    result = await mock_crud_base.update("1", mock_data_model)

    assert result == expected_result


@pytest.mark.asyncio
@pytest.mark.parametrize("mock_response", [({}), ([]), (None)])
async def test_update_fail(mock_session, mock_response):
    mock_crud_base = CRUDBase(
        db=mock_session, model=MockModel, table_name="dummy_table"
    )
    mock_table = mock_session.table(mock_crud_base.table_name)
    mock_table.update().execute.return_value = execute_response_format(mock_response)

    with pytest.raises(RuntimeError):
        await mock_crud_base.update("1", mock_data_model)


@pytest.mark.asyncio
async def test_delete(mock_session):
    mock_crud_base = CRUDBase(
        db=mock_session, model=MockModel, table_name="dummy_table"
    )

    result = await mock_crud_base.delete({"id": 1})

    assert result is True


@pytest.mark.asyncio
@pytest.mark.parametrize("mock_response", [({}), ([]), (None)])
async def test_delete_fail(mock_session, mock_response):
    mock_crud_base = CRUDBase(
        db=mock_session, model=MockModel, table_name="dummy_table"
    )
    mock_table = mock_session.table(mock_crud_base.table_name)
    mock_table.delete().execute.return_value = execute_response_format(mock_response)

    with pytest.raises(RuntimeError):
        await mock_crud_base.update("1", mock_data_model)