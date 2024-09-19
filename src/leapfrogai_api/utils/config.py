import asyncio
import fnmatch
import glob
import logging
import os
import toml
import yaml
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from leapfrogai_api.typedef.models import Model

logger = logging.getLogger(__name__)


class ConfigHandler(FileSystemEventHandler):
    def __init__(self, config):
        self.config = config
        super().__init__()

    def on_created(self, event):
        self.process(event)

    def on_modified(self, event):
        self.process(event)

    def on_deleted(self, event):
        self.process(event)

    def process(self, event):
        # Ignore directory events
        if event.is_directory:
            return

        filename = os.path.basename(event.src_path)

        # Check if the file matches the config filename or pattern
        if fnmatch.fnmatch(filename, self.config.filename):
            if event.event_type == "deleted":
                self.config.remove_model_by_config(filename)
            else:
                self.config.load_config_file(self.config.directory, filename)


class Config:
    models: dict[str, Model] = {}
    config_sources: dict[str, list] = {}

    def __init__(
        self, models: dict[str, Model] = {}, config_sources: dict[str, list] = {}
    ):
        self.models = models
        self.config_sources = config_sources
        self.directory = "."
        self.filename = "config.yaml"

    def __str__(self):
        return f"Models: {self.models}"

    async def watch_and_load_configs(self, directory=".", filename="config.yaml"):
        # Get the config directory and filename from the environment variables if provided
        env_directory = os.environ.get("LFAI_CONFIG_PATH", directory)
        if env_directory:
            directory = env_directory
        env_filename = os.environ.get("LFAI_CONFIG_FILENAME", filename)
        if env_filename:
            filename = env_filename

        self.directory = directory
        self.filename = filename

        # Process all the configs that were already in the directory
        self.load_all_configs(directory, filename)

        # Set up the event handler and observer
        event_handler = ConfigHandler(self)
        observer = Observer()
        observer.schedule(event_handler, path=directory, recursive=False)

        # Start the observer
        observer.start()
        logger.info(f"Started watching directory: {directory}")

        try:
            while True:
                await asyncio.sleep(1)
        except (KeyboardInterrupt, asyncio.CancelledError):
            # Stop the observer if the script is interrupted
            observer.stop()
            logger.info(f"Stopped watching directory: {directory}")

        # Wait for the observer to finish
        observer.join()

    async def clear_all_models(self):
        # Reset the model config on shutdown (so old model configs don't get cached)
        self.models = {}
        self.config_sources = {}
        logger.info("All models have been removed")

    def load_config_file(self, directory: str, config_file: str):
        logger.info(f"Loading config file: {directory}/{config_file}")

        # Load the config file into the config object
        config_path = os.path.join(directory, config_file)
        try:
            with open(config_path) as c:
                # Load the file into a python object
                if config_path.endswith(".toml"):
                    loaded_artifact = toml.load(c)
                elif config_path.endswith(".yaml"):
                    loaded_artifact = yaml.safe_load(c)
                else:
                    logger.error(f"Unsupported file type: {config_path}")
                    return

                # Parse the object into our config
                self.parse_models(loaded_artifact, config_file)

            logger.info(f"Loaded artifact at {config_path}")
        except Exception as e:
            logger.error(f"Failed to load config file {config_path}: {e}")

    def load_all_configs(self, directory="", filename="config.yaml"):
        logger.info(
            f"Loading all configs in {directory} that match the name '{filename}'"
        )

        if not os.path.exists(directory):
            logger.error(f"The config directory ({directory}) does not exist")
            return "THE CONFIG DIRECTORY DOES NOT EXIST"

        # Get all config files and load them into the config object
        config_files = glob.glob(os.path.join(directory, filename))
        for config_path in config_files:
            dir_path, file_path = os.path.split(config_path)
            self.load_config_file(directory=dir_path, config_file=file_path)

    def get_model_backend(self, model: str) -> Model | None:
        return self.models.get(model)

    def parse_models(self, loaded_artifact, config_file):
        for m in loaded_artifact.get("models", []):
            model_config = Model(name=m["name"], backend=m["backend"])

            self.models[m["name"]] = model_config
            self.config_sources.setdefault(config_file, []).append(m["name"])
            logger.info(f"Added {m['name']} to model config")

    def remove_model_by_config(self, config_file):
        model_names = self.config_sources.get(config_file, [])
        for model_name in model_names:
            self.models.pop(model_name, None)
            logger.info(f"Removed {model_name} from model config")

        # Clear config once all corresponding models are deleted
        self.config_sources.pop(config_file, None)
