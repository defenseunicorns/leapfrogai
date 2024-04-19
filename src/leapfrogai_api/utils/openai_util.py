""" This module contains utility functions for interacting with OpenAI API. """
import logging
from typing import Dict, List, Union
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


def validate_tools_typed_dict(data: List[Dict]) -> List[AssistantTool]:
    """Validate a tool typed dict."""
    for tool_data in data:
        if "type" not in tool_data:
            raise ValueError("Tool type not specified.")

        tool_type = tool_data["type"]
        if tool_type not in tool_mapping:
            raise ValueError(f"Unknown tool type: {tool_type}")

        tool_class = tool_mapping[tool_type]
        tool_instance = tool_class(**tool_data)

    if tool_instance is None:
        raise ValueError("No tools specified.")

    if len(data) > 128:
        raise ValueError("Too many tools specified.")

    if isinstance(tool_instance, list):
        return tool_instance

    return [tool_instance]


def strings_to_tools(tool_names: Union[str, List[str]]) -> List[AssistantTool]:
    """Convert a list of tool names to a list of tool instances."""
    tools = []
    included_types = set()  # Set to track included tool types

    if isinstance(tool_names, str):
        tool_names = [tool_names]

    for name in tool_names:
        if name in tool_mapping and name not in included_types:
            tool_class = tool_mapping[name]
            tool_instance = tool_class(type=name)
            tools.append(tool_instance)
            included_types.add(name)  # Mark this type as included
        elif name not in tool_mapping:
            logging.warning("Unknown tool type: %s", name)
            raise ValueError(f"Unknown tool type: {name}")

    return tools


def tools_to_strings(tools: List[AssistantTool]) -> List[str]:
    """Convert a list of tool instances to a list of tool names."""
    return [tool.type for tool in tools]
