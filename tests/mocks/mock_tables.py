from pydantic import BaseModel

from openai.types.beta import Thread, Assistant
from openai.types.beta.threads import Message, TextContentBlock, Text, Run


class MockModel(BaseModel):
    id: int
    name: str


mock_data_model = MockModel(id=1, name="mock-data")

mock_assistant = Assistant(
    id="0",
    created_at=0,
    model="mock-data",
    object="assistant",
    tools=[],
    instructions="mock-data",
)

mock_thread = Thread(id="1", created_at=0, object="thread")

mock_run = Run(
    id="0",
    assistant_id="0",
    created_at=0,
    instructions="mock-data",
    model="mock-data",
    object="thread.run",
    parallel_tool_calls=False,
    status="in_progress",
    thread_id="0",
    tools=[],
)

mock_message = Message(
    id="",
    thread_id="",
    created_at=0,
    object="thread.message",
    status="in_progress",
    role="assistant",
    content=[
        TextContentBlock(text=Text(value="mock-data", annotations=[]), type="text")
    ],
)


class MockApiKey(BaseModel):
    user_id: str


mock_api_key = MockApiKey(user_id="mock-api-key")
