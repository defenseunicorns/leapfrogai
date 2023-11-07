import os

from confz import BaseConfig, FileSource
from google.protobuf.internal.containers import RepeatedCompositeFieldContainer

from .chat.chat_pb2 import ChatItem, ChatRole


class LLMDefaults(BaseConfig):
    temperature: float = 0.5
    top_k: int = 80
    top_p: float = 0.9


class ChatFormat(BaseConfig):
    system: str | None = None
    assistant: str | None = None
    user: str | None = None


class PromptFormat(BaseConfig):
    chat: ChatFormat | None = None


class BackendConfig(BaseConfig):
    name: str
    model_type: str | None = None
    trust_remote_code: bool = False
    model_context_length: int = 2048
    prompt_format: PromptFormat
    defaults: LLMDefaults

    CONFIG_SOURCES = FileSource(file=os.getenv("LEAPFROGAI_CONFIG_FILE", "config.yaml"))

    def apply_chat_template(
        self, chat_items: RepeatedCompositeFieldContainer[ChatItem]
    ) -> str:
        response_prefix = self.prompt_format.chat.assistant.split("{}")[0]
        prompt = ""
        for item in chat_items:
            if item.role == ChatRole.SYSTEM:
                prompt += self.prompt_format.chat.system.format(item.content)
            elif item.role == ChatRole.ASSISTANT:
                prompt += self.prompt_format.chat.assistant.format(item.content)
            elif item.role == ChatRole.USER:
                prompt += self.prompt_format.chat.user.format(item.content)
            elif item.role == ChatRole.FUNCTION:
                logging.warning(
                    "ChatRole FUNCTION is not implemented for this model and this ChatItem will be ignored."
                )
        # add the response prefix to start the model's reponse
        prompt += response_prefix
        return prompt
