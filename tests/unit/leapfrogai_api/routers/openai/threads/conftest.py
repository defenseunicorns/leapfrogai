from openai.types.beta import Thread, Assistant
from openai.types.beta.threads import Message, TextContentBlock, Text, Run


mock_thread = Thread(
    id="", 
    created_at=0,
    object="thread"
)

mock_message = Message(
    id="",
    thread_id="",
    created_at=0,
    object="thread.message",
    status="in_progress",
    role="assistant",
    content=[TextContentBlock(text=Text(value="mock-data", annotations=[]), type="text")],
)

mock_assistant = Assistant(
    id = "0",
    created_at = 0,
    model = "mock-data",
    object = "assistant",
    tools = [],
    instructions="mock-data"
)

mock_run = Run(
    id = "0",
    assistant_id = "0",
    created_at = 0,
    instructions = "mock-data",
    model = "mock-data",
    object = "thread.run",
    parallel_tool_calls = False,
    status = "in_progress",
    thread_id = "0",
    tools = []
)