import os

os.environ["LEAPFROGAI_CONFIG_FILE"] = "tests/fixtures/config.yaml"

from leapfrogai.chat.chat_pb2 import ChatItem, ChatRole
from leapfrogai.config import BackendConfig


def test_apply_chat_template():
    config = BackendConfig()
    expected = """<|im_start|>system
Hello<|im_end|>
<|im_start|>assistant
"""
    assert (
        config.apply_chat_template([ChatItem(role=ChatRole.SYSTEM, content="Hello")])
        == expected
    )
