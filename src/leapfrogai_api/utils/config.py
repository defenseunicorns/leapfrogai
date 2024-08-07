from __future__ import annotations
import fnmatch
import logging
import os
from typing import Any, Literal, Self
from pathlib import Path

import toml
import yaml
from watchfiles import Change, awatch
from dataclasses import dataclass, asdict

logging.basicConfig(level=logging.INFO)

DEFAULT_CONFIG_FILE: str = "config.yaml"


@dataclass
class ModelMetadata:
    """
    Initializes a ModelMetadata object with the specified model type, dimensions, and precision.

    Parameters:
        capabilities (list[str], optional): The capabilities of the model e.g. ('embeddings' or 'chat').
        dimensions (Optional[int], optional): Embedding dimensions (for embeddings models). Defaults to None.
        precision (str, optional): Model precision (e.g., 'float16', 'float32'). Defaults to 'float32'.
        type (Literal["embeddings", "llm"], optional): The type of the model e.g  ('embeddings' or 'llm').
    """

    capabilities: list[str] | None = None
    dimensions: int | None = None
    precision: str | None = None
    type: Literal["embeddings", "llm"] | None = None

    def has_values(self) -> bool:
        """
        Returns True if any of the attributes 'type', 'dimensions', or 'precision' of the object are not None,
        and False otherwise.

        :return: bool
        """
        # returns true if any public attribute is not None
        return any(value is not None for value in asdict(self).values())


@dataclass
class Model:
    """Represents a model in the LeapFrogAI API."""

    name: str
    backend: str
    metadata: ModelMetadata | None = None


class Config:
    models: dict[str, Model] = {}
    config_sources: dict[str, list] = {}

    def __init__(
        self,
        models: dict[str, Model] | None = None,
        config_sources: dict[str, list] | None = None,
    ):
        # both values default to empty dict if not provided
        self.models = models or {}
        self.config_sources = config_sources or {}

    def __str__(self) -> str:
        return f"Models: {self.models}"

    def __repr__(self) -> str:
        return f"Config(models={self.models}, config_sources={self.config_sources})"

    def initialize_config(
        self,
        directory: str = ".",
        filename: str = DEFAULT_CONFIG_FILE,
    ) -> tuple[str, str]:
        """
        Initialize the configuration by loading all configs from the specified directory and filename.

        Args:
            directory (str): The directory to load the configs from. Defaults to ".".
            filename (str): The filename of the config file. Defaults to DEFAULT_CONFIG_FILE.

        Returns:
            tuple[str, str]: A tuple containing the directory and filename used to load the configs.
        """
        # Get the config directory and filename from the environment variables if provided
        directory = os.environ.get("LFAI_CONFIG_PATH", directory)
        filename = os.environ.get("LFAI_CONFIG_FILENAME", filename)

        # Process all the configs that were already in the directory
        self.load_all_configs(
            directory=directory,
            filename=filename,
        )
        return (directory, filename)

    def _process_changes(
        self,
        changes: list[tuple[Change, str]],
    ) -> tuple[set[str], set[str]]:
        """
        Process the changes detected by awatch and return sets of new and deleted files.

        Args:
            changes (list[tuple[Change, str]]): A list of tuples containing the type of change and the file path.

        Returns:
            tuple[set[str], set[str]]: A tuple containing two sets: one for the new files and one for the deleted files.
        """
        unique_new_files = set()
        unique_deleted_files = set()
        for change in changes:
            if change[0] == Change.deleted:
                unique_deleted_files.add(os.path.basename(change[1]))
            else:
                unique_new_files.add(os.path.basename(change[1]))
        return unique_new_files, unique_deleted_files

    def _load_updated_configs(
        self,
        directory: str,
        matches: list[str],
    ) -> None:
        """
        Load updated config files.

        Args:
            directory (str): The directory containing the config files.
            matches (list[str]): The list of config file names to load.

        Returns:
            None
        """
        for match in matches:
            try:
                self.load_config_file(directory, match)
            except Exception as e:
                logging.error(f"Failed to load config file {match}: {e}")

    def _remove_deleted_configs(self, matches: list[str]) -> None:
        """
        Remove models corresponding to deleted config files.

        Args:
            matches (list[str]): A list of file paths of deleted config files.

        Returns:
            None: This function does not return anything.

        Raises:
            Exception: If there is an error removing a config file. The error message will include the file path.

        """
        for match in matches:
            try:
                self.remove_model_by_config(config_file=match)
            except Exception as e:
                logging.error(f"Failed to remove config for file {match}: {e}")

    def _handle_config_file_changes(
        self,
        changes: list[tuple[Change, str]],
        directory: str,
        filename: str,
    ) -> None:
        """
        Handle changes detected in configuration files, including processing changes,
        filtering relevant files, and loading or removing configs as necessary.

        Args:
            changes (list[tuple[Change, str]]): A list of changes detected by awatch.
            directory (str): The directory being watched.
            filename (str): The filename pattern to match.

        Returns:
            None
        """
        logging.info(f"Config changes detected: {changes}")
        # TODO: Anything with I/O below is going to be synchronous and blocking
        unique_new_files, unique_deleted_files = self._process_changes(changes)
        filtered_new_matches = fnmatch.filter(unique_new_files, filename)
        filtered_deleted_matches = fnmatch.filter(unique_deleted_files, filename)

        self._load_updated_configs(directory, filtered_new_matches)
        self._remove_deleted_configs(filtered_deleted_matches)

    async def watch_and_load_configs(
        self,
        directory: str = ".",
        filename: str = DEFAULT_CONFIG_FILE,
        recursive: bool = False,
        step: int = 50,
    ) -> None:
        """
        Asynchronously watches a directory for changes to configuration files and loads/removes models based on the changes.

        Args:
            directory (str, optional): The directory to watch for changes. Defaults to ".".
            filename (str, optional): The name of the configuration file to watch for. Defaults to DEFAULT_CONFIG_FILE.
            recursive (bool, optional): Whether to watch the directory recursively. Defaults to False.
            step (int, optional): The time in milliseconds between each check for changes. Defaults to 50.

        Returns:
            None: This function does not return anything.
        """
        # Load and process all the configs that were already in the directory
        directory, filename = self.initialize_config(
            directory=directory,
            filename=filename,
        )

        # Watch the directory for changes indefinitely
        while True:
            watcher = awatch(directory, recursive=recursive, step=step)
            async for changes in watcher:
                self._handle_config_file_changes(changes, directory, filename)
            logging.info("Finished watching for config changes")

    async def clear_all_models(self) -> Self:
        # reset the model config on shutdown (so old model configs don't get cached)
        self.models = {}
        self.config_sources = {}
        logging.info("All models have been removed")
        return self

    def load_config_file(
        self,
        directory: str,
        config_file: str,
    ) -> None:
        """
        Load a configuration file from the specified directory and parse its contents into the config object.

        Args:
            directory (str): The directory where the configuration file is located.
            config_file (str): The name of the configuration file.

        Returns:
            None: This function does not return anything.

        Raises:
            None: This function does not raise any exceptions.

        Side Effects:
            - The configuration file is loaded and its contents are parsed into the config object.
            - The function logs the path of the loaded configuration file.

        """
        logging.info("Loading config file: {}/{}".format(directory, config_file))

        # load the config file into the config object
        config_path = os.path.join(directory, config_file)
        with open(config_path) as c:
            # Load the file into a python object
            loaded_artifact: dict[str, Any] = {}
            if config_path.endswith(".toml"):
                loaded_artifact = toml.load(c)
            elif config_path.endswith(".yaml"):
                loaded_artifact = yaml.safe_load(c)
            else:
                # TODO: Return an error ???
                logging.error(f"Unsupported file type: {config_path}")
                return

            # parse the object into our config object
            self.parse_models(loaded_artifact, config_file)

        logging.info("loaded artifact at {}".format(config_path))

        return

    def load_all_configs(
        self,
        directory: str = "",
        filename: str = DEFAULT_CONFIG_FILE,
    ) -> list[Path] | str:
        """
        Load all config files in the specified directory that match the given filename.

        Args:
            directory (str): The directory where the config files are located. Defaults to an empty string.
            filename (str): The filename pattern to match. Defaults to the value of DEFAULT_CONFIG_FILE.

        Returns:
            list[str] | str:
            If the specified directory does not exist, returns the error message "THE CONFIG DIRECTORY DOES NOT EXIST".

        Raises:
            None

        """
        logging.info(
            "Loading all configs in {} that match the name '{}'".format(
                directory, filename
            )
        )

        if not (directory_path := Path(directory)).exists():
            logging.error("The config directory ({}) does not exist".format(directory))
            return "THE CONFIG DIRECTORY DOES NOT EXIST"

        # Get all config files with valid extensions
        valid_extensions: list[str] = [".yaml", ".yml", ".toml"]
        config_files: list[str] = [
            p for p in directory_path.glob(filename) if p.suffix in valid_extensions
        ]

        # load the config files into the config object
        for config_path in config_files:
            self.load_config_file(
                directory=str(config_path.parent),
                config_file=config_path.name,
            )

        # Return the list of config Paths, if any
        return config_files

    def get_model_backend(self, model: str) -> Model | None:
        if model in self.models:
            return self.models[model]
        return None

    def _get_model(
        self,
        model: dict[str, Any],
    ) -> Model:
        """
        Creates and returns a `Model` object based on the given `model` dictionary.

        Args:
            model (dict[str, Any]): A dictionary containing the information to create a `Model` object.
                The dictionary should have the following keys:
                    - "name" (str): The name of the model.
                    - "backend" (str): The backend of the model.
                    - "type" (str, optional): The type of the model.
                    - "dimensions" (int, optional): The dimensions of the model.
                    - "precision" (int, optional): The precision of the model.

        Returns:
            Model: The created `Model` object.

        Raises:
            KeyError: If the required keys are not present in the `model` dictionary.
        """
        metadata: ModelMetadata | None = ModelMetadata(
            type=model.get("type"),
            dimensions=model.get("dimensions"),
            precision=model.get("precision"),
            capabilities=model.get("capabilities"),
        )
        # default to None if no non-None attributes exist in class
        if not metadata.has_values():
            metadata = None

        return Model(
            name=model["name"],
            backend=model["backend"],
            metadata=metadata,
        )

    def parse_models(
        self,
        loaded_artifact: dict[str, Any],
        config_file: str,
    ) -> None:
        """
        Parses the models from the loaded artifact and updates the internal model configuration.

        Args:
            loaded_artifact (dict[str, Any]): A dictionary containing the loaded artifact information.
                It should have a key "models" which is a list of dictionaries representing the models.
                Each dictionary should have a key "name" representing the name of the model.
            config_file (str): The name of the configuration file.

        Returns:
            None: This function does not return anything.

        Raises:
            KeyError: If the required keys are not present in the loaded_artifact dictionary.

        Side Effects:
            - Updates the internal `models` dictionary with the parsed models.
            - Updates the `config_sources` dictionary with the parsed model names.
            - Logs a message indicating the added model to the model config.
        """
        for m in loaded_artifact["models"]:
            model_config = self._get_model(model=m)

            self.models[m["name"]] = model_config
            try:
                self.config_sources[config_file].append(m["name"])
            except KeyError:
                self.config_sources[config_file] = [m["name"]]
            logging.info("added {} to model config".format(m["name"]))

    def remove_model_by_config(self, config_file: str) -> None:
        """
        Remove models based on the specified config file.

        Args:
            config_file (str): The file path of the config file to remove models from.

        Returns:
            None: This function does not return anything.
        """
        for model_name in self.config_sources[config_file]:
            self.models.pop(model_name)
            logging.info("removed {} from model config".format(model_name))

        # clear config once all corresponding models are deleted
        self.config_sources.pop(config_file)
