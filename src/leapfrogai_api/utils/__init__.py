from leapfrogai_api.utils.config import Config

config = None


def get_model_config():
    global config
    if config is None:
        config = Config()
    return config
