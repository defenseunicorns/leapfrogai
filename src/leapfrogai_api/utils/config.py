import fnmatch
import glob
import logging
import os
import time
import toml
import yaml
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from leapfrogai_api.typedef.models import Model

logger = logging.getLogger(__name__)


class ConfigHandler(FileSystemEventHandler):
    def __init__(self, config):
        self.config = config

    def on_created(self, event):
        if not event.is_directory:
            self.config.handle_file_change(event.src_path)

    def on_modified(self, event):
        if not event.is_directory:
            self.config.handle_file_change(event.src_path)

    def on_deleted(self, event):
        if not event.is_directory:
            self.config.handle_file_deletion(event.src_path)


class Config:
    models: dict[str, Model] = {}
    config_sources: dict[str, list] = {}

    def __init__(
        self, models: dict[str, Model] = {}, config_sources: dict[str, list] = {}
    ):
        self.models = models
        self.config_sources = config_sources

    def __str__(self):
        return f"Models: {self.models}"

    async def watch_and_load_configs(self, directory=".", filename="config.yaml"):
        # Get the config directory and filename from the environment variables if provided
        env_directory = os.environ.get("LFAI_CONFIG_PATH", directory)
        if env_directory is not None and env_directory != "":
            directory = env_directory
        env_filename = os.environ.get("LFAI_CONFIG_FILENAME", filename)
        if env_filename is not None and env_filename != "":
            filename = env_filename

        # Process all the configs that were already in the directory
        self.load_all_configs(directory, filename)

        # Set up the watchdog observer
        event_handler = ConfigHandler(self)
        observer = Observer()
        observer.schedule(event_handler, directory, recursive=False)
        observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

    def handle_file_change(self, file_path):
        directory, file_name = os.path.split(file_path)
        if fnmatch.fnmatch(file_name, self.filename):
            self.load_config_file(directory, file_name)

    def handle_file_deletion(self, file_path):
        file_name = os.path.basename(file_path)
        if fnmatch.fnmatch(file_name, self.filename):
            self.remove_model_by_config(file_name)

    async def load_config_file(self, directory: str, config_file: str):
        logger.info("Loading config file: {}/{}".format(directory, config_file))

        # load the config file into the config object
        config_path = os.path.join(directory, config_file)
        with open(config_path) as c:
            # Load the file into a python object
            loaded_artifact = {}
            if config_path.endswith(".toml"):
                loaded_artifact = toml.load(c)
            elif config_path.endswith(".yaml"):
                loaded_artifact = yaml.safe_load(c)
            else:
                # TODO: Return an error ???
                logger.error(f"Unsupported file type: {config_path}")
                return

            # parse the object into our config
            self.parse_models(loaded_artifact, config_file)

        logger.info("loaded artifact at {}".format(config_path))

        return

    def load_all_configs(self, directory="", filename="config.yaml"):
        logger.info(
            "Loading all configs in {} that match the name '{}'".format(
                directory, filename
            )
        )

        if not os.path.exists(directory):
            logger.error("The config directory ({}) does not exist".format(directory))
            return "THE CONFIG DIRECTORY DOES NOT EXIST"

        # Get all config files and load them into the config object
        config_files = glob.glob(os.path.join(directory, filename))
        for config_path in config_files:
            dir_path, file_path = os.path.split(config_path)
            self.load_config_file(directory=dir_path, config_file=file_path)

        return

    def get_model_backend(self, model: str) -> Model | None:
        if model in self.models:
            return self.models[model]
        else:
            return None

    def parse_models(self, loaded_artifact, config_file):
        for m in loaded_artifact["models"]:
            model_config = Model(name=m["name"], backend=m["backend"])

            self.models[m["name"]] = model_config
            try:
                self.config_sources[config_file].append(m["name"])
            except KeyError:
                self.config_sources[config_file] = [m["name"]]
            logger.info("added {} to model config".format(m["name"]))

    def remove_model_by_config(self, config_file):
        for model_name in self.config_sources[config_file]:
            self.models.pop(model_name)
            logger.info("removed {} from model config".format(model_name))

        # clear config once all corresponding models are deleted
        self.config_sources.pop(config_file)

    def clear_all_models(self):
        # reset the model config on shutdown (so old model configs don't get cached)
        self.models = {}
        self.config_sources = {}
        logger.info("All models have been removed")
