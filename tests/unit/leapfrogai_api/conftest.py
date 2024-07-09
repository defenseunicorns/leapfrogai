import pytest
from unittest.mock import patch, MagicMock

# This imports the Session mock into the running test
# Exposes the imports to all test files in this directory and lower
from tests.mocks.mock_session import mock_session  # noqa: F401


# This mocks the model Config class
@pytest.fixture(scope="session", autouse=True)
def mock_config():
    with patch("leapfrogai_api.utils.Config") as mock:
        # Configure the mock as needed
        mock_model_obj = dict(name="mock_model_name", backend="mock_backend")
        mock.return_value.models.return_value = mock_model_obj

        mock_model = MagicMock()
        mock_model.name = "mock_model_name"
        mock_model.backend = "mock_backend"
        mock.return_value.get_model_backend.return_value = mock_model

        yield mock
