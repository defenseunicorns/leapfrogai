from pydantic import BaseModel


class MockModel(BaseModel):
    id: int
    name: str


def execute_response_format(data):
    if isinstance(data, list):
        return ((None, data), len(data))
    elif data:
        return ((None, [data]), 1)
    else:
        return None

