"""CRUD operations for the Message object."""

from supabase_py_async import AsyncClient
from openai.types.beta.threads import Message


class CRUDMessageObject:
    """CRUD Operations for MessageObject"""

    def __init__(self, model: type[Message]):
        self.model = model

    async def create(
        self, client: AsyncClient, message_object: Message
    ) -> Message | None:
        """Create a new message object."""
        data, _count = (
            await client.table("message_objects")
            .insert(message_object.model_dump())
            .execute()
        )

        _, response = data

        if response:
            return self.model(**response[0])
        return None

    async def get(self, client: AsyncClient, message_id: str) -> Message | None:
        """Get a message object by its ID."""
        data, _count = (
            await client.table("message_objects")
            .select("*")
            .eq("id", message_id)
            .execute()
        )

        _, response = data

        if data:
            return self.model(**response[0])
        return None

    async def list(self, client: AsyncClient) -> list[Message] | None:
        """List all message objects."""
        data, _count = await client.table("message_objects").select("*").execute()

        _, response = data

        if response:
            return [self.model(**item) for item in response]
        return None

    async def update(
        self, client: AsyncClient, message_id: str, message_object: Message
    ) -> Message | None:
        """Update a message object by its ID."""
        data, _count = (
            await client.table("message_objects")
            .update(message_object.model_dump())
            .eq("id", message_id)
            .execute()
        )

        _, response = data

        if response:
            return self.model(**response[0])
        return None

    async def delete(self, client: AsyncClient, message_id: str) -> Message | None:
        """Delete a message object by its ID."""
        data, _count = (
            await client.table("message_objects")
            .delete()
            .eq("id", message_id)
            .execute()
        )

        _, response = data

        if response:
            return self.model(**response[0])
        return None
