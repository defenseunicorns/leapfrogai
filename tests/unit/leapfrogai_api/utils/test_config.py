from __future__ import annotations
import pytest
from pathlib import Path
import logging

from unittest.mock import patch, MagicMock

from src.leapfrogai_api.utils.config import (
    Config,
    Model,
    ModelMetadata,
    DEFAULT_CONFIG_FILE,
)
from watchfiles import Change

# Both of these are relative to the tests directory
TOML_CONFIG_FILE: str = "test_config.toml"
YAML_CONFIG_FILE: str = "test_config.yaml"
INVALID_CONFIG_FILE: str = "invalid_config.fake"
NON_EXISTENT_DIR: str = "/path/to/non/existent/directory"


@pytest.fixture
def test_dir():
    """Fixture to return the path to the tests directory."""
    return Path(__file__).resolve().parent


@pytest.fixture
def config_files(test_dir: Path) -> list[Path]:
    """Fixture to represent the list of config files in the tests directory."""
    return [
        test_dir / YAML_CONFIG_FILE,
        test_dir / TOML_CONFIG_FILE,
        test_dir / INVALID_CONFIG_FILE,
    ]


@pytest.fixture(scope="function")
def config() -> Config:
    """Fixture to represent a Config object."""
    return Config()


@pytest.mark.parametrize(
    "metadata, expected",
    [
        (ModelMetadata(), False),
        (ModelMetadata(type="embeddings"), True),
        (ModelMetadata(dimensions=768), True),
        (ModelMetadata(precision="float32"), True),
        (ModelMetadata(capabilities=["chat"]), True),
    ],
)
def test_model_metadata_has_values(metadata, expected):
    # No values should be False, otherwise any non-None value should be True
    assert metadata.has_values() == expected


class TestConfig:
    def test_init(self, config: Config) -> None:
        """Test the initialization of Config."""
        assert config.models is not None and config.models == {}
        assert config.config_sources is not None and config.config_sources == {}

    def test_str(self, config: Config) -> None:
        """Test the string representation of Config."""
        assert str(config) == "Models: {}"

    def test_repr(self, config: Config) -> None:
        """Test the repr representation of Config."""
        assert repr(config) == "Config(models={}, config_sources={})"

    def test_get_model_backend(self, config: Config) -> None:
        """Test retrieving model backend."""
        model = Model(name="test_model", backend="test_backend")
        config.models["test_model"] = model
        assert config.get_model_backend("test_model") == model
        assert config.get_model_backend("non_existent_model") is None

    @pytest.mark.parametrize(
        "config_file",
        [
            YAML_CONFIG_FILE,
            TOML_CONFIG_FILE,
        ],
    )
    def test_load_config_file(
        self, config: Config, test_dir: str, config_file: str
    ) -> None:
        """Test loading a single config file."""
        config.load_config_file(
            directory=test_dir,
            config_file=config_file,
        )

        assert len(config.models) == 2
        assert "model1" in config.models
        assert "model2" in config.models

        model1 = config.models["model1"]
        assert model1.name == "model1"
        assert model1.backend == "backend1"
        assert model1.metadata is not None
        assert model1.metadata.type == "type1"
        assert model1.metadata.dimensions == 768
        assert model1.metadata.precision == 32

        model2 = config.models["model2"]
        assert model2.name == "model2"
        assert model2.backend == "backend2"
        assert model2.metadata is None

        assert config_file in config.config_sources
        config_files = set(config.config_sources[config_file])
        assert config_files == set(["model1", "model2"])

    @patch.object(Config, "parse_models")
    def test_load_config_file_raises(self, mock_parse_models, test_dir: str) -> None:
        """Test loading a config with an invalid extension results in None."""
        config = Config()
        result = config.load_config_file(
            directory=test_dir,
            config_file=INVALID_CONFIG_FILE,
        )
        assert result is None

    def test_load_all_configs(self, config: Config, test_dir: str) -> None:
        """Test loading all config files in a directory."""
        config.load_all_configs(
            directory=test_dir,
            filename="test_config.*",
        )

        assert len(config.config_sources) == 2
        for file_name in [YAML_CONFIG_FILE, TOML_CONFIG_FILE]:
            assert file_name in config.config_sources

        assert (
            len(config.models) == 2
        )  # Both files have the same models, so only 2 unique models
        assert "model1" in config.models
        assert "model2" in config.models

    def test_load_all_configs_directory_not_exists(self, config: Config) -> None:
        """Test loading configs from a non-existent directory."""
        non_existent_dir = NON_EXISTENT_DIR
        result = config.load_all_configs(non_existent_dir, "test_config.*")
        assert result == "THE CONFIG DIRECTORY DOES NOT EXIST"
        assert len(config.models) == 0
        assert len(config.config_sources) == 0

    def test_process_changes(self, config):
        changes = [
            (Change.added, "/path/to/new_file1.txt"),
            (Change.modified, "/path/to/new_file2.txt"),
            (Change.deleted, "/path/to/deleted_file1.txt"),
            (Change.deleted, "/path/to/deleted_file2.txt"),
        ]

        new_files, deleted_files = config._process_changes(changes)

        assert new_files == {"new_file1.txt", "new_file2.txt"}
        assert deleted_files == {"deleted_file1.txt", "deleted_file2.txt"}

    def test_load_updated_configs(self, config: Config, test_dir: str, caplog) -> None:
        """Test loading updated config files."""
        config.load_config_file = MagicMock(
            side_effect=[
                None,
                Exception("Mocked Exception"),
            ]
        )

        matches = [YAML_CONFIG_FILE, TOML_CONFIG_FILE]
        with caplog.at_level(logging.ERROR):
            config._load_updated_configs(test_dir, matches)

        config.load_config_file.assert_any_call(test_dir, YAML_CONFIG_FILE)
        config.load_config_file.assert_any_call(test_dir, TOML_CONFIG_FILE)
        assert config.load_config_file.call_count == 2
        # Check the correct log message
        expected_log = (
            f"Failed to load config file {TOML_CONFIG_FILE}: Mocked Exception"
        )
        assert expected_log in caplog.text

    def test_remove_deleted_configs(self, config: Config, caplog) -> None:
        """Test removing models corresponding to deleted config files."""
        config.remove_model_by_config = MagicMock(
            side_effect=[
                None,
                Exception("Mocked Exception"),
            ]
        )

        matches = ["deleted_config.yaml", "other_config.yaml"]
        with caplog.at_level(logging.ERROR):
            config._remove_deleted_configs(matches)

        config.remove_model_by_config.assert_any_call(config_file="deleted_config.yaml")
        config.remove_model_by_config.assert_any_call(config_file="other_config.yaml")
        assert config.remove_model_by_config.call_count == 2

        # Check the correct log message
        expected_log = (
            f"Failed to remove config for file {matches[1]}: Mocked Exception"
        )
        assert expected_log in caplog.text

    def test_remove_model_by_config(self, config: Config) -> None:
        """Test removing models by config file."""
        config.models = {
            "model1": Model(name="model1", backend="backend1"),
            "model2": Model(name="model2", backend="backend2"),
        }
        config.config_sources = {YAML_CONFIG_FILE: ["model1", "model2"]}

        config.remove_model_by_config(YAML_CONFIG_FILE)

        assert len(config.models) == 0
        assert YAML_CONFIG_FILE not in config.config_sources

    @pytest.mark.asyncio
    async def test_clear_all_models(self, config: Config) -> None:
        """Test clearing all models."""
        config.models = {
            "model1": Model(name="model1", backend="backend1"),
            "model2": Model(name="model2", backend="backend2"),
        }
        config.config_sources = {YAML_CONFIG_FILE: ["model1", "model2"]}

        await config.clear_all_models()

        assert len(config.models) == 0
        assert len(config.config_sources) == 0

    def test_handle_config_file_changes(self, config):
        # Mock the internal methods
        config._process_changes = MagicMock(
            return_value=(set(["new_file.yaml"]), set(["deleted_file.yaml"]))
        )
        config._load_updated_configs = MagicMock()
        config._remove_deleted_configs = MagicMock()

        # Create a sample list of changes
        changes = [
            (Change.added, "path/to/new_file.yaml"),
            (Change.deleted, "path/to/deleted_file.yaml"),
        ]

        # Call the method we're testing
        with patch("src.leapfrogai_api.utils.config.fnmatch.filter") as mock_filter:
            mock_filter.side_effect = [["new_file.yaml"], ["deleted_file.yaml"]]
            config._handle_config_file_changes(changes, "/path/to", "*.yaml")

        # Assert that _process_changes was called with the correct arguments
        config._process_changes.assert_called_once_with(changes)

        # Assert that fnmatch.filter was called twice with the correct arguments
        assert mock_filter.call_count == 2
        mock_filter.assert_any_call({"new_file.yaml"}, "*.yaml")
        mock_filter.assert_any_call({"deleted_file.yaml"}, "*.yaml")

        # Assert that _load_updated_configs was called with the correct arguments
        config._load_updated_configs.assert_called_once_with(
            "/path/to", ["new_file.yaml"]
        )

        # Assert that _remove_deleted_configs was called with the correct arguments
        config._remove_deleted_configs.assert_called_once_with(["deleted_file.yaml"])

        # Optional: Test logging (if you want to ensure the log message is correct)
        with patch("src.leapfrogai_api.utils.config.logging.info") as mock_logging:
            config._handle_config_file_changes(changes, "/path/to", "*.yaml")
            mock_logging.assert_called_with(f"Config changes detected: {changes}")

    def test_initialize_config(self, config):
        # Test default behavior
        with patch.object(Config, "load_all_configs") as mock_load_all_configs:
            result = config.initialize_config()
            mock_load_all_configs.assert_called_once_with(
                directory=".", filename=DEFAULT_CONFIG_FILE
            )
            assert result == (".", DEFAULT_CONFIG_FILE)

        # Test with custom parameters
        with patch.object(Config, "load_all_configs") as mock_load_all_configs:
            result = config.initialize_config(
                directory="/custom/dir", filename="custom.yaml"
            )
            mock_load_all_configs.assert_called_once_with(
                directory="/custom/dir", filename="custom.yaml"
            )
            assert result == ("/custom/dir", "custom.yaml")

        # Test with environment variables
        env_vars = {"LFAI_CONFIG_PATH": "/env/dir", "LFAI_CONFIG_FILENAME": "env.yaml"}
        with (
            patch.dict("os.environ", env_vars),
            patch.object(Config, "load_all_configs") as mock_load_all_configs,
        ):
            result = config.initialize_config()
            mock_load_all_configs.assert_called_once_with(
                directory="/env/dir", filename="env.yaml"
            )
            assert result == ("/env/dir", "env.yaml")

        # Test with environment variables overriding custom parameters
        with (
            patch.dict("os.environ", env_vars),
            patch.object(Config, "load_all_configs") as mock_load_all_configs,
        ):
            result = config.initialize_config(
                directory="/custom/dir", filename="custom.yaml"
            )
            mock_load_all_configs.assert_called_once_with(
                directory="/env/dir", filename="env.yaml"
            )
            assert result == ("/env/dir", "env.yaml")
