import logging
import os

from confz import BaseConfig, FileSource
from google.protobuf.internal.containers import RepeatedCompositeFieldContainer

from leapfrogai import ChatItem, ChatRole


class LLMDefaults(BaseConfig):
    temperature: float = 0.5
    top_k: int = 80
    top_p: float = 0.9
    repetition_penalty: float = 1.0
    max_new_tokens: int = 256


class ChatFormat(BaseConfig):
    system: str | None = None
    assistant: str | None = None
    user: str | None = None


class PromptFormat(BaseConfig):
    chat: ChatFormat | None = None


class ModelConfig(BaseConfig):
    type: str | None = None
    source: str | None = "./model"
    file: str | None = None
    allow_remote_caching: bool = False
    trust_remote_code: bool = False


class BackendConfig(BaseConfig):
    name: str | None = None
    model: ModelConfig | None = None
    max_context_length: int = 2048
    stop_tokens: list[str] | None = None
    prompt_format: PromptFormat | None = None
    defaults: LLMDefaults = LLMDefaults()

    CONFIG_SOURCES = FileSource(
        file=os.getenv("LEAPFROGAI_CONFIG_FILE", "config.yaml"), optional=True
    )

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
