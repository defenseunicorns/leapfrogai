from __future__ import annotations

import logging
import traceback

from openai.types.beta import (
    AssistantResponseFormatOption,
    FileSearchTool,
    Assistant,
    AssistantToolChoiceOption,
    AssistantTool,
    AssistantToolChoice,
)
from openai.types.beta.assistant_stream_event import (
    ThreadRunCreated,
    ThreadRunQueued,
    ThreadRunInProgress,
    ThreadRunCompleted,
)
from openai.types.beta.thread import ToolResources as BetaThreadToolResources
from openai.types.beta.threads import Run
from openai.types.beta.threads.run_create_params import TruncationStrategy
from pydantic import BaseModel, Field, ValidationError

from leapfrogai_api.backend.constants import (
    DEFAULT_MAX_COMPLETION_TOKENS,
    DEFAULT_MAX_PROMPT_TOKENS,
)
from leapfrogai_api.backend.converters import (
    from_assistant_stream_event_to_str,
)
from leapfrogai_api.data.crud_assistant import CRUDAssistant, FilterAssistant
from leapfrogai_api.routers.supabase_session import Session

logger = logging.getLogger(__name__)


class RunCreateParamsRequestBase(BaseModel):
    assistant_id: str = Field(default="", examples=["123ab"])
    instructions: str = Field(default="", examples=["You are a helpful AI assistant."])
    max_completion_tokens: int | None = Field(
        default=DEFAULT_MAX_COMPLETION_TOKENS, examples=[DEFAULT_MAX_COMPLETION_TOKENS]
    )
    max_prompt_tokens: int | None = Field(
        default=DEFAULT_MAX_PROMPT_TOKENS, examples=[DEFAULT_MAX_PROMPT_TOKENS]
    )
    metadata: dict | None = Field(default={}, examples=[{}])
    model: str | None = Field(default=None, examples=["llama-cpp-python"])
    response_format: AssistantResponseFormatOption | None = Field(
        default=None, examples=["auto"]
    )
    temperature: float | None = Field(default=None, examples=[1.0])
    tool_choice: AssistantToolChoiceOption | None = Field(
        default="auto", examples=["auto"]
    )
    tools: list[AssistantTool] = Field(
        default=[], examples=[[FileSearchTool(type="file_search")]]
    )
    top_p: float | None = Field(default=None, examples=[1.0])
    truncation_strategy: TruncationStrategy | None = Field(
        default=None, examples=[TruncationStrategy(type="auto", last_messages=None)]
    )
    parallel_tool_calls: bool | None = Field(default=False, examples=[False])

    def __init__(self, **data):
        super().__init__(**data)
        # TODO: Temporary fix to ensure max_completion_tokens and max_prompt_tokens are set
        if self.max_completion_tokens is None or self.max_completion_tokens < 1:
            logger.warning(
                "max_completion_tokens is not set or is less than 1, setting to %s",
                DEFAULT_MAX_COMPLETION_TOKENS,
            )
            self.max_completion_tokens = DEFAULT_MAX_COMPLETION_TOKENS
        if self.max_prompt_tokens is None or self.max_prompt_tokens < 1:
            logger.warning(
                "max_prompt_tokens is not set or is less than 1, setting to %s",
                DEFAULT_MAX_PROMPT_TOKENS,
            )
            self.max_prompt_tokens = DEFAULT_MAX_PROMPT_TOKENS

    @staticmethod
    def get_initial_messages_base(run: Run) -> list[str]:
        return [
            from_assistant_stream_event_to_str(
                ThreadRunCreated(data=run, event="thread.run.created")
            ),
            from_assistant_stream_event_to_str(
                ThreadRunQueued(data=run, event="thread.run.queued")
            ),
            from_assistant_stream_event_to_str(
                ThreadRunInProgress(data=run, event="thread.run.in_progress")
            ),
        ]

    @staticmethod
    def get_ending_messages_base(run: Run) -> list[str]:
        return [
            from_assistant_stream_event_to_str(
                ThreadRunCompleted(data=run, event="thread.run.completed")
            )
        ]

    async def update_with_assistant_data(self, session: Session) -> Assistant | None:
        crud_assistant = CRUDAssistant(session)
        assistant = await crud_assistant.get(
            filters=FilterAssistant(id=self.assistant_id)
        )

        if assistant:
            self.model = self.model or assistant.model
            self.temperature = self.temperature or assistant.temperature
            self.top_p = self.top_p or assistant.top_p
            self.instructions = self.instructions or assistant.instructions or ""

        return assistant

    def can_use_rag(
        self,
        tool_resources: BetaThreadToolResources | None,
    ) -> bool:
        if not tool_resources:
            return False

        has_tool_choice: bool = self.tool_choice is not None
        has_tool_resources: bool = bool(
            tool_resources.file_search and tool_resources.file_search.vector_store_ids
        )

        if has_tool_choice and has_tool_resources:
            if isinstance(self.tool_choice, str):
                return self.tool_choice == "auto" or self.tool_choice == "required"
            else:
                try:
                    if isinstance(self.tool_choice, AssistantToolChoice):
                        return self.tool_choice.type == "file_search"
                except ValidationError:
                    traceback.print_exc()
                    logger.error(
                        "Cannot use RAG for request, failed to validate tool for thread"
                    )
                    return False

        return False
