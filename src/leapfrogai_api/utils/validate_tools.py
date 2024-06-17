"""Utility functions for validating tools and tool resources."""

from typing import Union
from openai.types.beta import (
    AssistantTool,
    AssistantToolChoice,
    AssistantToolChoiceOption,
)
from openai.types.beta.assistant import ToolResources as BetaAssistantToolResources
from openai.types.beta.thread import ToolResourcesCodeInterpreter
from openai.types.beta.thread import ToolResources as BetaThreadToolResources

SUPPORTED_TOOLS = ["file_search"]


def validate_assistant_tool(tool: AssistantTool) -> bool:
    """Validate an AssistantTool."""
    if tool.type not in SUPPORTED_TOOLS:
        return False
    return True


def validate_tool_resources(
    tool_resources: Union[BetaAssistantToolResources, BetaThreadToolResources],
) -> bool:
    """Validate a ToolResources object."""
    if hasattr(tool_resources, "code_interpreter") and isinstance(tool_resources.code_interpreter, ToolResourcesCodeInterpreter):
        return False
    return True


def validate_assistant_tool_choice_option(
    tool_choice_option: AssistantToolChoiceOption,
) -> bool:
    """Validate an AssistantToolChoiceOption."""
    if isinstance(tool_choice_option, AssistantToolChoice):
        if tool_choice_option.type not in SUPPORTED_TOOLS:
            return False
    return True
