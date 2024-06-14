from openai.types.beta import Thread
from openai.types.beta.threads import Message, TextContentBlock, Text

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