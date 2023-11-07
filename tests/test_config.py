import os

from confz import FileSource

from leapfrogai import ChatItem, ChatRole
from leapfrogai.config import BackendConfig


def test_no_config():
    config = BackendConfig()
    assert config.defaults.temperature == 0.5


def test_apply_chat_template():
    os.environ["LEAPFROGAI_CONFIG_FILE"] = "tests/fixtures/config.yaml"
    config = BackendConfig()
    with config.change_config_sources(
        FileSource(file=os.getenv("LEAPFROGAI_CONFIG_FILE", "config.yaml"))
    ):
        expected = """<|im_start|>system
Hello<|im_end|>
<|im_start|>assistant
"""
        assert (
            BackendConfig().apply_chat_template(
                [ChatItem(role=ChatRole.SYSTEM, content="Hello")]
            )
            == expected
        )
