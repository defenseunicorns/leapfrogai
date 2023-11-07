import os

from leapfrogai.config import BackendConfig


def test_apply_chat_template():
    os.environ["LEAPFROGAI_CONFIG_FILE"] = "tests/fixtures/config.yaml"
    config = BackendConfig()
