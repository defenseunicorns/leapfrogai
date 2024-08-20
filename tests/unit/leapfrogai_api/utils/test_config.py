from typing import AsyncGenerator, TypeAlias, Callable
import pytest
import asyncio

from anyio import Path
import pytest_asyncio
from unittest.mock import patch, AsyncMock, MagicMock
import toml
from watchfiles import Change

from leapfrogai_api.utils.config import (
    Config,
    ConfigFile,
    Model,
)

# This is just to make the IDE happy about what the factory does
ConfigFileMaker: TypeAlias = Callable[[str], ConfigFile]


TOML_CONFIG_FILE: str = "test_config.toml"
YAML_CONFIG_FILE: str = "test_config.yaml"
INVALID_CONFIG_FILE: str = "invalid_config.fake"
NON_EXISTENT_DIR: str = "/path/to/non/existent/directory"


@pytest.fixture
def config_file():
    return ConfigFile(Path(YAML_CONFIG_FILE))


@pytest_asyncio.fixture
async def config_file_factory(monkeypatch) -> AsyncGenerator[ConfigFile, None]:
    async def _create_config_file(path: str, mock_load: bool = False) -> ConfigFile:
        config_file = ConfigFile(path=Path(path))

        if mock_load:
            # Mock the aload method
            config_file.aload = AsyncMock()

            # Optionally mock the behavior to simulate file loading
            config_file.aload.return_value = None  # or whatever behavior you expect
            config_file.models = {
                "test_model": Model(name="test_model", backend="test_backend")
            }

        return config_file

    yield _create_config_file


@pytest.mark.anyio
async def test_config_singleton():
    """Test that Config is a singleton"""
    config1 = await Config.create()
    config2 = await Config.create()
    assert config1 is config2
    await Config.cleanup()


@pytest.mark.anyio
async def test_initialize_from_env(config_factory):
    """Test that this will run from the env vars we specify and won't error just cause it's a fake path"""
    config_path = "/test/path"
    config_filename = "test*.yaml"

    # Set env variables to existing values if not provided, and create the config object
    config = await config_factory(
        config_path=config_path,
        config_filename=config_filename,
    )
    assert config._config_dir == "/test/path"
    assert config._config_filename == "test*.yaml"
    await config.cleanup()


@pytest.mark.anyio
async def test_config_load_config_file(config_factory, config_file_factory):
    """Test that this will run from the env vars we specify and won't error just cause it's a fake path"""
    config_filename = "test_config.yaml"
    config: Config = await config_factory(
        config_path="/test/path",
        config_filename="test_config.yaml",
    )
    # Create a real ConfigFile instance with a mocked __await__ method
    config_file: ConfigFile = await config_file_factory(
        path=config_filename, mock_load=True
    )

    with patch(
        "leapfrogai_api.utils.config.ConfigFile",  # Patching the class constructor to return our instance
        return_value=config_file,
    ):
        await config._load_config_file(path=Path(config_filename))

    # Verify that the config file was loaded into the config object
    test_config = config.config_files.get(config_filename, None)
    assert test_config is not None, f"{config_filename} not loaded: {test_config}"

    # Verify that the model was loaded into the config's models
    test_model = config.models.get("test_model", None)
    assert test_model is not None, f"test_model not loaded: {test_model}"
    assert test_model.name == "test_model"
    assert test_model.backend == "test_backend"


@pytest.mark.anyio
async def test_load_all_configs(config_factory, parent_dir):
    config = await config_factory()

    mock_glob = MagicMock()
    mock_glob.__aiter__.return_value = iter(
        [
            await (Path(parent_dir) / "test-config.yaml").resolve(),
            await (Path(parent_dir) / "test-config.toml").resolve(),
        ]
    )

    with patch("leapfrogai_api.utils.config.Path.glob", return_value=mock_glob):
        await config.load_all_configs()

    assert mock_glob.__aiter__.called


@pytest.mark.anyio
async def test_watch_for_changes(config_factory, parent_dir):
    config = await config_factory(config_path=parent_dir, config_filename="*.yaml")

    # Create an async generator for mocking awatch
    awatch_response = [(Change.added, "test-config.yaml")]

    async def mock_awatch_generator():
        yield awatch_response
        # Add a small delay to allow other coroutines to run
        await asyncio.sleep(0.1)

    with (
        patch(
            "leapfrogai_api.utils.config.awatch",
            return_value=mock_awatch_generator(),
        ),
        patch.object(config, "initialize", new_callable=AsyncMock) as mock_initialize,
        patch.object(
            config, "_handle_config_changes", new_callable=AsyncMock
        ) as mock_handle_config_changes,
    ):
        # Start watching in a separate task
        watch_task = asyncio.create_task(config.start_watching())

        # Wait a short time to allow the watch task to start and process the mock changes
        await asyncio.sleep(0.2)

        # Stop the watching
        await config.stop_watching()

        # Wait for the watch task to complete
        await watch_task

    mock_initialize.assert_called_once()
    mock_handle_config_changes.assert_called_once_with(awatch_response)

    # config.initialize.assert_called_once()
    # config._handle_config_changes.assert_called_once_with([
    #     (Change.added, "new_config.yaml")
    # ])


@pytest.mark.anyio
async def test_handle_config_changes(config_factory):
    config = await config_factory()
    mock_load_config = AsyncMock()
    changes = [
        (Change.added, "new_config.yaml"),
        (Change.modified, "existing_config.yaml"),
        (Change.deleted, "old_config.yaml"),
        (Change.added, "not_a_config.txt"),
    ]

    config.config_files = {"old_config.yaml": AsyncMock()}

    with patch.object(config, "_load_config_file", mock_load_config):
        await config._handle_config_changes(changes)

    assert mock_load_config.call_count == 2  # for added and modified
    assert "old_config.yaml" not in config.config_files


@pytest.mark.anyio
async def test_get_model_backend(config_factory):
    config = await config_factory()

    config.models = {"test_model": Model(name="test_model", backend="test_backend")}
    assert config.get_model_backend("test_model").backend == "test_backend"
    assert config.get_model_backend("non_existent_model") is None


@pytest.mark.anyio
async def test_clear_all_models(config_factory, parent_dir):
    config = await config_factory(config_path=parent_dir)

    mock_config_file = AsyncMock(spec=ConfigFile)
    mock_config_file.filename = "test_config.yaml"  # Mock the filename attribute
    config.config_files = {"test_config.yaml": mock_config_file}
    config.models = {"test_model": Model(name="test_model", backend="test_backend")}

    await config.clear_all_models()

    assert len(config.models) == 0
    assert len(config.config_files) == 0
    mock_config_file.aunload.assert_called_once()


@pytest.mark.anyio
async def test_to_dict(config_factory):
    config = await config_factory()
    config.models = {
        "model1": Model(name="model1", backend="backend1"),
        "model2": Model(name="model2", backend="backend2"),
    }
    config.config_files = {
        "config1.yaml": MagicMock(
            spec=ConfigFile, filename="config1.yaml", models={"model1": None}
        ),
        "config2.yaml": MagicMock(
            spec=ConfigFile, filename="config2.yaml", models={"model2": None}
        ),
    }

    result = config.to_dict()

    assert "config_sources" in result
    assert "models" in result
    assert len(result["models"]) == 2
    assert result["config_sources"]["config1.yaml"] == ["model1"]
    assert result["config_sources"]["config2.yaml"] == ["model2"]


@pytest.mark.asyncio
async def test_parse_models(config_files):
    config_path: Path = config_files.get(YAML_CONFIG_FILE, None)
    assert config_path is not None, f"Could not find config file: {YAML_CONFIG_FILE}"
    config = ConfigFile(
        path=Path(config_path),
    )
    await config.aload()
    test_data = {
        "models": [
            {"name": "model1", "backend": "backend1"},
            {"name": "model2", "backend": "backend2"},
        ]
    }

    config.parse_models(test_data)

    assert len(config.models) == 2
    # Model 1 tests
    model1 = config.models["model1"]
    assert model1.name == "model1"
    assert model1.backend == "backend1"

    # Model 2 tests
    model2 = config.models["model2"]

    assert model2.name == "model2"
    assert model2.backend == "backend2"

    assert config._loaded is True


@pytest.mark.asyncio
async def test_load_from_file_yaml(config_files):
    config_path: Path = config_files.get(YAML_CONFIG_FILE, None)
    assert config_path is not None, f"Could not find config file: {YAML_CONFIG_FILE}"
    config_path = await config_path.resolve()

    config = ConfigFile(path=config_path)
    # result = await config._load_from_file
    result = await config._load_from_file(config_path)

    print(f"Debug: result = {result}")

    expected_data = {
        "models": [
            {
                "name": "model1",
                "backend": "backend1",
                "type": "type1",
                "dimensions": 768,
                "precision": 32,
                "capabilities": ["embeddings"],
            },
            {"name": "model2", "backend": "backend2"},
        ]
    }

    assert result == expected_data


@pytest.mark.asyncio
async def test_load_from_file_toml(config_files):
    config_path: Path = config_files.get(TOML_CONFIG_FILE, None)
    assert config_path is not None, f"Could not find config file: {TOML_CONFIG_FILE}"
    config_path = await config_path.resolve()

    print(f"Debug: config_path = {config_path}")
    print(f"Debug: config_path.exists() = {await config_path.exists()}")
    print(f"Debug: config_path.is_file() = {await config_path.is_file()}")

    config = ConfigFile(path=config_path)
    result = await config._load_from_file(config_path)

    print(f"Debug: result = {result}")

    # Load the TOML file directly for comparison
    with open(config_path, "r") as f:
        expected_data = toml.load(f)

    print(f"Debug: expected_data = {expected_data}")

    assert result == expected_data


@pytest.mark.asyncio
async def test_load_from_file_unsupported():
    config = ConfigFile(Path("test_config.txt"))

    with patch("pathlib.Path.open") as mock_open:
        mock_file = MagicMock()
        mock_file.read.return_value = "dummy_content"
        mock_open.return_value.__aenter__.return_value = mock_file

        result = await config._load_from_file(Path("test_config.txt"))

        assert result == {}


@pytest.mark.asyncio
async def test_load_config_file():
    config = ConfigFile(path=await Path(YAML_CONFIG_FILE).resolve())
    test_data = {"models": [{"name": "test_model", "backend": "test_backend"}]}

    with (
        patch.object(config, "_load_from_file") as mock_load,
        patch.object(config, "parse_models") as mock_parse,
    ):
        mock_load.return_value = test_data

        await config.load_config_file()

        mock_load.assert_called_once_with(path=config.path)
        mock_parse.assert_called_once_with(test_data)


@pytest.mark.asyncio
async def test_aload():
    config = ConfigFile(Path(YAML_CONFIG_FILE))

    with (
        patch("pathlib.Path.exists") as mock_exists,
        patch.object(config, "load_config_file") as mock_load,
    ):
        mock_exists.return_value = True

        await config.aload()

        mock_exists.assert_called_once()
        mock_load.assert_called_once()


@pytest.mark.asyncio
async def test_aunload():
    config = ConfigFile(Path(YAML_CONFIG_FILE))
    config.models = {"model1": Model(name="model1", backend="backend1")}
    config._loaded = True

    await config.aunload()

    assert len(config.models) == 0
    assert config._loaded is False, f"config._loaded = {config._loaded}"


def test_str_representation(config_file):
    assert str(config_file) == f"Path: {config_file.path}, Models: {{}}"


def test_repr_representation(config_file):
    assert repr(config_file) == f"ConfigFile(path={config_file.path}, models={{}})"
