import fnmatch
import glob
import logging
import os
from typing import List

import toml
import yaml
from watchfiles import Change, awatch


class Model:
    name: str
    backend: str

    def __init__(self, name: str, backend: str, capabilities: List[str] | None = None):
        self.name = name
        self.backend = backend


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

        # Watch the directory for changes until the end of time
        while True:
            async for changes in awatch(directory, recursive=False, step=50):
                # get two unique lists of files that have been (updated files and deleted files)
                # (awatch can return duplicates depending on the type of updates that happen)
                logging.info("Config changes detected: {}".format(changes))
                unique_new_files = set()
                unique_deleted_files = set()
                for change in changes:
                    if change[0] == Change.deleted:
                        unique_deleted_files.add(os.path.basename(change[1]))
                    else:
                        unique_new_files.add(os.path.basename(change[1]))

                # filter the files to those that match the filename or glob pattern
                filtered_new_matches = fnmatch.filter(unique_new_files, filename)
                filtered_deleted_matches = fnmatch.filter(
                    unique_deleted_files, filename
                )

                # load all the updated config files
                for match in filtered_new_matches:
                    self.load_config_file(directory, match)

                # remove deleted models
                for match in filtered_deleted_matches:
                    self.remove_model_by_config(match)

    async def clear_all_models(self):
        # reset the model config on shutdown (so old model configs don't get cached)
        self.models = {}
        self.config_sources = {}
        logging.info("All models have been removed")

    def load_config_file(self, directory: str, config_file: str):
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
                logging.error(f"Unsupported file type: {config_path}")
                return

            # parse the object into our config
            self.parse_models(loaded_artifact, config_file)

        logging.info("loaded artifact at {}".format(config_path))

        return

    def load_all_configs(self, directory="", filename="config.yaml"):
        if not os.path.exists(directory):
            return "THE CONFIG DIRECTORY DOES NOT EXIST"

        # Get all config files
        config_files = glob.glob(os.path.join(directory, filename))

        # load all the found config files into the config object
        for config_path in config_files:
            self.load_config_file(directory, filename)

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
            logging.info("added {} to model config".format(m["name"]))

    def remove_model_by_config(self, config_file):
        for model_name in self.config_sources[config_file]:
            self.models.pop(model_name)
            logging.info("removed {} from model config".format(model_name))

        # clear config once all corresponding models are deleted
        self.config_sources.pop(config_file)
