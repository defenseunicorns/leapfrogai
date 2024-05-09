"""This module contains utility functions for interacting with OpenAI API."""

from openai.types.beta import (
    CodeInterpreterTool,
    FileSearchTool,
    FunctionTool,
    AssistantTool,
)

tool_mapping = {
    "code_interpreter": CodeInterpreterTool,
    "file_search": FileSearchTool,
    "function_tool": FunctionTool,
}


def validate_tools_typed_dict(data: list[dict]) -> list[AssistantTool]:
    """Validate a tool typed dict."""

    max_supported_tools = 128  # OpenAI sets this to 128

    if len(data) > max_supported_tools:
        raise ValueError("Too many tools specified.")
    if len(data) == 0:
        raise ValueError("No tools specified.")

    for tool_data in data:
        if "type" not in tool_data:
            raise ValueError("Tool type not specified.")

        tool_type = tool_data["type"]
        if tool_type not in tool_mapping:
            raise ValueError(f"Unknown tool type: {tool_type}")

        tool_class = tool_mapping[tool_type]
        tool_instance = tool_class(**tool_data)

    if isinstance(tool_instance, list):
        return tool_instance

    return [tool_instance]
