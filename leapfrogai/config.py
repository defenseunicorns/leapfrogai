from confz import BaseConfig, FileSource


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

    CONFIG_SOURCES = FileSource(file="config.yaml")

    def apply_chat_template(prompt):
        pass
