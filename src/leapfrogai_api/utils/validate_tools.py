from typing import Union
from openai.types.beta import AssistantTool
from openai.types.beta.assistant import ToolResources as BetaAssistantToolResources
from openai.types.beta.thread import ToolResources as BetaThreadToolResources

SUPPORTED_TOOLS = ["file_search"]


def validate_assistant_tool(tool: AssistantTool) -> bool:
    if tool.type not in SUPPORTED_TOOLS:
        return False
    return True


def validate_tool_resources(
    tool_resources: Union[BetaAssistantToolResources, BetaThreadToolResources],
) -> bool:
    if tool_resources.code_interpreter:
        return False
    return True
