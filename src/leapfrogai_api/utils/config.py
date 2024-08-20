# src/leapfrogai_api/utils/config.py
from __future__ import annotations
import asyncio
import logging
import os
import functools
import traceback
from typing import Any, Callable, ClassVar, Generator, Literal, Self
from anyio import Event

# from pathlib import Path
from anyio import Path

import anyio
import toml
import yaml
from watchfiles import Change, awatch

from dataclasses import dataclass, asdict
from leapfrogai_api.backend.types import Capability, Precision, Modality, Format

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


DEFAULT_CONFIG_FILE: str = "config.yaml"


def async_locked(method: Callable) -> Callable:
    @functools.wraps(method)
    async def wrapper(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        # Acquire the lock if it's not already held
        if getattr(self, "_lock", None) is None:
            self._lock = anyio.Lock()
        try:
            # Wrap the method with the lock.
            # NOTE: The lock must be released by the task that acquired it
            async with self._lock:
                return await method(self, *args, **kwargs)
        except asyncio.CancelledError:
            raise
        finally:
            # Release the lock regardless
            if getattr(self, "_lock", None) is not None:
                self._lock = None

    return wrapper


@dataclass
class ModelMetadata:
    """
    Initializes a ModelMetadata object with the specified model type, dimensions, and precision.

    Parameters:
        capabilities (list[Capability], optional): The capabilities of the model e.g. ('embeddings' or 'chat').
        dimensions (Optional[int], optional): Embedding dimensions (for embeddings models). Defaults to None.
        precision (str, optional): Model precision (e.g., 'float16', 'float32'). Defaults to 'float32'.
        type (Literal["embeddings", "llm"], optional): The type of the model e.g  ('embeddings' or 'llm').
    """

    capabilities: list[Capability] | None = None
    dimensions: int | None = None
    format: Format | None = None
    modalities: list[Modality] | None = None
    precision: Precision | None = None
    type: Literal["embeddings", "llm"] | None = None

    def has_values(self) -> bool:
        """
        Returns True if any of the attributes 'type', 'dimensions', or 'precision' of the object are not None,
        and False otherwise.

        :return: bool
        """
        # returns true if any public attribute is not None
        return any(value is not None for value in asdict(self).values())

    def __iter__(self) -> Generator[tuple[str, Any], None, None]:
        """Make it iterable / possible to use `dict(class_instance)"""
        yield from asdict(self).items()


@dataclass
class Model:
    """Represents a model in the LeapFrogAI API."""

    name: str
    backend: str
    metadata: ModelMetadata | None = None

    def __iter__(self) -> Generator[tuple[str, Any], None, None]:
        """Make it iterable / possible to use `dict(class_instance)"""
        yield from asdict(self).items()


class ConfigFile:
    def __init__(self, path: Path):
        self.path = path
        self.filename = str(path.name)
        self.models: dict[str, Model] = {}
        self._loaded = False
        # https://anyio.readthedocs.io/en/stable/synchronization.html#locks
        self._lock: anyio.Lock | None = None
        # methods used to parse models from a file
        self.parsers: dict[str, Callable] = {
            ".toml": toml.loads,
            ".yaml": yaml.safe_load,
            ".yml": yaml.safe_load,
        }

    def parse_models(self, loaded_artifact: dict[str, Any]) -> Self:
        # Step 1: Clear models to avoid duplicates for the given config file
        self.models.clear()

        # Step 2: Make sure that the config file contains models
        models_to_load = loaded_artifact.get("models", [])
        if not models_to_load:
            logger.error(f"Failed to load and parse config from {self.path}")
            return self

        # Step 3: Load and parse models
        for m in models_to_load:
            model_name = m["name"]
            model_config = Model(
                name=model_name,
                backend=m["backend"],
                metadata=ModelMetadata(**m["metadata"]) if m.get("metadata") else None,
            )
            self.models[model_name] = model_config
            logger.debug(f"Added {model_name} to model config")
        logger.debug(f"Successfully loaded and parsed config from {self.path}")
        self._loaded = True
        return self

    async def _load_from_file(self, path: Path) -> dict[str, Any]:
        """
        Asynchronously loads the content of a file from the given path and returns it as a dictionary.

        Args:
            path (Path): The path to the file to be loaded.

        Returns:
            dict[str, Any]: A dictionary containing the content of the file. If the file type is not supported or an error occurs during loading, an empty dictionary is returned.
        """

        try:
            async with await path.open("r") as contents:
                # If a known file type is found, use the corresponding parser
                if (parser := self.parsers.get(path.suffix)) is not None:
                    logger.debug(f"Loading config file: {path}")
                    loaded_artifact = parser(await contents.read())
                    logger.debug(f"Loaded artifact content: {loaded_artifact}")
                    return loaded_artifact

                # Else, return an empty dict if the file type is not supported
                logger.error(f"Unsupported file type: {path}")
                return {}

        except Exception as e:
            logger.error(f"Error loading config file {path}: {e}")
            return {}  # Return an empty dict if there's an error

    @async_locked
    async def load_config_file(self) -> None:
        logger.debug(f"Loading config file: {self.path}")
        try:
            if not (loaded_artifact := await self._load_from_file(path=self.path)):
                return
            self.parse_models(loaded_artifact)
        except Exception as e:
            logger.error(f"Error loading config file {self.path}: {e}")

    async def aload(self) -> None:
        # We make a new lock for each config file to avoid race conditions
        async with anyio.Lock():
            if not await self.path.exists():
                logger.error(f"Config file does not exist: {self.path}")
                return
            await self.load_config_file()
        return self

    @async_locked
    async def aunload(self) -> None:
        self.models.clear()
        logger.debug(f"Unloaded config file: {self.path}")
        self._loaded = False

    def __await__(self):
        # Load the config file on await
        return self.aload().__await__()

    def __str__(self) -> str:
        return f"Path: {self.path}, Models: {self.models}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(path={self.path}, models={self.models})"


class Config:
    """Configuration class for the Leapfrog AI API.

    This class is used to dynamically load and manage the configuration files for the Leapfrog AI API.
    """

    _instance: ClassVar["Config | None"] = None
    _watch_task: ClassVar[asyncio.Task | None] = None
    # https://anyio.readthedocs.io/en/latest/synchronization.html#events
    _stop_event: ClassVar[asyncio.Event] = Event()
    _testing: ClassVar[bool] = False

    def __new__(cls):
        """This method is used to ensure that only one instance of the Config class is created."""
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """Only one instance of the Config class can be created."""
        if not hasattr(self, "initialized"):
            self.config_files: dict[str, ConfigFile] = {}
            self.models: dict[str, Model] = {}
            self._config_dir = None
            self._config_filename = None
            self._lock = asyncio.Lock()
            self.initialized = True

    @classmethod
    async def create(cls, testing: bool = False) -> "Config":
        """
        Creates a new instance of the Config class.

        Args:
            testing (bool): A flag indicating if the Config instance is being created for testing purposes.
                Defaults to False.

        Returns:
            Config: The created instance of the Config class.
        """
        logger.debug("Entering Config.create")
        if cls._instance is None:
            cls._instance = cls()
        cls._testing = testing
        await cls._instance.initialize()
        return cls._instance

    async def initialize(self, testing: bool = False) -> Self:
        logger.debug("Initializing Config")
        try:
            self._initialize_from_env()
            await self.load_all_configs()
            await self.start_watching(testing)

            if not hasattr(self, "_initialized") or self._initialized is None:
                self._initialized = True
                logger.debug("Config initialized successfully")
            else:
                logger.debug("Existing Config found, skipping initialization")

        except Exception as e:
            logger.error(f"Error during Config initialization: {e}")
            raise
        return self

    def _initialize_from_env(self):
        """Updates the config directory and filename from environment variables.

        NOTE: At present this gets called as part of `initialize`. As such, it means that
        Any iterations of `watch_for_changes` will use the environment variables, even if they are updated
        AFTER the class has been instantiated. This behavior is intentional, but only for testing purposes.
        """
        logger.debug("Initializing from environment")
        self._config_dir = os.environ.get("LFAI_CONFIG_PATH", ".")
        self._config_filename = os.environ.get("LFAI_CONFIG_FILENAME", "*config.yaml")

    async def _load_config_file(self, path: Path) -> Self:
        config_file = ConfigFile(path=path)
        await config_file
        self.config_files[path.name] = config_file
        self.models.update(config_file.models)
        return self

    async def load_all_configs(self) -> None:
        logger.debug(
            f"Loading all configs in {self._config_dir} matching {self._config_filename}"
        )
        try:
            path = Path(self._config_dir)
            config_files = path.glob(self._config_filename)
            async for config_path in config_files:
                logger.debug(f"Loading config file: {config_path}")
                await self._load_config_file(path=config_path)
            logger.debug(f"Loaded configs: {list(self.config_files.keys())}")
            logger.debug(f"Current models: {list(self.models.keys())}")
        except Exception as e:
            logger.error(f"Error loading configs: {e}")
            raise e

    async def start_watching(self, testing: bool = False):
        if self._watch_task is not None:
            if self._watch_task.done():
                self._watch_task = None
            else:
                logger.warning("Watch task is already running")
                return self._watch_task

        logger.debug("Starting config watcher")
        self._watch_task = asyncio.create_task(
            self._watch_wrapper(testing=testing),
            name="Config Watcher Wrapper Worker",
        )
        logger.debug("Started watching for config changes")
        return self._watch_task

    @classmethod
    async def stop_watching(cls) -> None:
        """
        Stops the configuration watcher.

        This method stops the configuration watcher by setting the stop event and
        waiting for the watch task to finish. If the watch task does not finish within
        the specified timeout, a warning is logged. If the watch task is cancelled or
        an error occurs while stopping the watch task, an error is logged and the
        exception is re-raised.

        This method is idempotent. If the watcher is already stopped, it is ignored.

        Raises:
            Exception: If an error occurs while stopping the watch task.
        """
        if cls._watch_task is None:
            logger.warning("No watch task is running")
            return

        logger.info("Stopping config watcher")
        cls._stop_event.set()

        try:
            await asyncio.wait_for(cls._watch_task, timeout=5.0)
        except asyncio.TimeoutError:
            logger.warning("Timeout while waiting for watch task to finish")
        except asyncio.CancelledError:
            logger.debug("Watch task was cancelled")
        except Exception as e:
            logger.error(f"Error while stopping watch task: {e}")
            raise e
        finally:
            if cls._watch_task and not cls._watch_task.done():
                logger.debug("Force cancelling the watch task")
                cls._watch_task.cancel()
                try:
                    await cls._watch_task
                except asyncio.CancelledError:
                    pass

            cls._watch_task = None
            cls._stop_event.clear()
        logger.info("Stopped watching for config changes")

    async def _watch_wrapper(self, testing: bool) -> Self:
        """
        Executes the watch task for configuration changes.

        This function is responsible for running the watch task for configuration changes. It calls the `watch_for_changes` method with the provided `testing` flag. If the task is cancelled, it logs a message. If an exception occurs during the execution, it logs an error message and re-raises the exception. Finally, it ensures that the `cleanup` method is called after the task ends.

        Args:
            testing (bool): A flag indicating if the watch task is running in a testing environment.

        Returns:
            self: The instance of the class.

        Raises:
            Exception: If an error occurs during the watch task execution.
        """
        try:
            await self.watch_for_changes(testing=testing)
        except asyncio.CancelledError:
            logger.info("Watch task was cancelled")
        except Exception:
            logger.error(f"Error in watch task: {traceback.format_exc()}")
            raise
        finally:
            logger.debug("Cleaning up watch task")
            await self.cleanup()  # Ensure cleanup is called after the watch ends
            return self

    async def watch_for_changes(self, testing: bool = False) -> None:
        """
        Watches for changes in the configuration directory.

        Args:
            testing (bool): A flag indicating if the watch task is running in a testing environment. Defaults to False.

        Returns:
            None
        """
        if self._watch_task is None:
            logger.warning("No watch task is running")
            return

        logger.debug("Watching for changes")

        try:
            async for changes in awatch(
                self._config_dir,
                recursive=False,
                step=50,  # Normal interval
                stop_event=self.__class__._stop_event,
                debug=False,
            ):
                logger.debug(f"Detected changes: {changes}")
                await self.initialize()
                await self._handle_config_changes(changes)
        except asyncio.CancelledError as e:
            logger.warning("Watch for changes task was cancelled")
            raise e
        finally:
            logger.debug("Finished watch_for_changes")

    async def _handle_config_changes(
        self,
        changes: list[tuple[Change, str]],
    ) -> None:
        """
        Handles the detected changes in the configuration files.

        Args:
            changes (list[tuple[Change, str]]): A list of tuples representing the changes detected. Each tuple contains the type of change (Change.added, Change.modified, or Change.deleted) and the file path.

        Returns:
            None

        This function iterates over the list of changes and performs the necessary actions based on the type of change. If a change is detected in a configuration file, it updates or removes the corresponding config file and model from the internal state. If a change is detected in a non-configuration file, it is ignored.

        After handling the changes, the function logs the updated state of the config files and models.

        Note: This function assumes that the configuration files and models are stored in the `config_files` and `models` attributes of the object, respectively.
        """
        logger.info(f"Detected changes: {changes}")
        for change_type, file_path in changes:
            path = Path(file_path)
            if path.match(self._config_filename):
                if change_type in (Change.added, Change.modified):
                    logger.info(f"Adding or updating config file: {path}")
                    await self._load_config_file(path=path)
                elif change_type == Change.deleted:
                    logger.info(f"Removing config file from handler: {path}")
                    if config_file := self.config_files.pop(path.name, None):
                        for model_name in config_file.models:
                            self.models.pop(model_name, None)
            else:
                logger.debug(f"Ignoring change to non-config file: {path}")

        logger.debug(
            f"Updated state - Config files: {list(self.config_files.keys())}, Models: {list(self.models.keys())}"
        )

    @classmethod
    async def cleanup(cls):
        """
        Cleans up the Config instance by stopping the watch task and clearing all models.

        This method is a class method and is used to clean up the Config instance when it is no longer needed.

        Args:
            None

        Returns:
            None
        """
        await cls.stop_watching()
        if cls._instance:
            await cls._instance.clear_all_models()
            cls._instance = None
            logger.debug("Config instance cleanup complete")

    def get_model_backend(self, model: str) -> Model | None:
        """Get the backend for a model."""
        return self.models.get(model)

    async def clear_all_models(self) -> None:
        """Clear all models."""
        logger.debug("Clearing all models")
        self.models.clear()
        for config_file in list(self.config_files.values()):
            logger.debug(f"Removing config file: {config_file.filename}")
            await config_file.aunload()
        self.config_files.clear()
        logger.debug("All models have been removed")

    def to_dict(self) -> dict[str, Any]:
        """The method used to serialize the Config instance to a dictionary."""
        models_dict = {
            # TODO: Make this dynamically generated / structured
            name: {
                "name": name,
                "backend": model.backend,
                "metadata": model.metadata.dict() if model.metadata else None,
            }
            for name, model in self.models.items()
        }

        config_sources = {
            config_file.filename: list(config_file.models.keys())
            for config_file in self.config_files.values()
        }

        return {
            "config_sources": config_sources,
            "models": models_dict,
        }

    def __del__(self):
        if self.__class__._watch_task:
            self.__class__._watch_task.cancel()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.to_dict()})"
