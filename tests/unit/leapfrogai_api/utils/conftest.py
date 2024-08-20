import os
import pytest
import pytest_asyncio
from anyio import Path
from typing import AsyncGenerator, TypeAlias, Callable
from leapfrogai_api.utils.config import Config

TOML_CONFIG_FILE: str = "test_config.toml"
YAML_CONFIG_FILE: str = "test_config.yaml"
INVALID_CONFIG_FILE: str = "invalid_config.fake"
NON_EXISTENT_DIR: str = "/path/to/non/existent/directory"

ConfigMaker: TypeAlias = Callable[[str, str], Config]


@pytest_asyncio.fixture(scope="function")
async def config_files() -> dict[str, Path]:
    """Fixture to return the path to the tests directory."""
    # NOTE: this is an async `anyio.Path` object that is _mostly_ comptatible with `pathlib.Path`
    test_dir = await Path(str(__file__)).resolve()
    dir_name = Path(
        os.path.dirname(test_dir)
    )  # dir the file lives in e.g `/tests/unit/leapfrogai_api/utils`
    return {
        YAML_CONFIG_FILE: await (dir_name / YAML_CONFIG_FILE).resolve(),
        TOML_CONFIG_FILE: await (dir_name / TOML_CONFIG_FILE).resolve(),
        INVALID_CONFIG_FILE: await (dir_name / INVALID_CONFIG_FILE).resolve(),
    }


@pytest_asyncio.fixture
async def config_factory(monkeypatch) -> AsyncGenerator[ConfigMaker, None]:
    """Used to instantiate a Config object while overriding the initial env vars that dictate the folders / files to use"""

    async def _create_config(
        config_path: str | None = None,
        config_filename: str | None = None,
    ) -> Config:
        # Check for either arguments or env vars
        config_path = config_path or os.environ.get("LFAI_CONFIG_PATH")
        config_filename = config_filename or os.environ.get("LFAI_CONFIG_FILENAME")

        # if either are set, patch the env vars
        if config_path is not None:
            monkeypatch.setenv("LFAI_CONFIG_PATH", config_path)
        if config_filename is not None:
            monkeypatch.setenv("LFAI_CONFIG_FILENAME", config_filename)
        # Instatiate the config now that we have patched our environment variables
        config = await Config.create(testing=True)
        return config

    yield _create_config


@pytest.fixture(autouse=True)
def anyio_backend():
    """This is necessary to prevent `watchfiles` from keeping an open thread with anyio"""
    return "asyncio"


@pytest_asyncio.fixture
def parent_dir():
    """Return the parent directory of the current file."""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
