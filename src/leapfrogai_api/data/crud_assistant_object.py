"""CRUD Operations for Assistant."""

from supabase_py_async import AsyncClient
from openai.types.beta import Assistant, AssistantDeleted


class CRUDAssistant:
    """CRUD Operations for Assistant"""

    def __init__(self, model: type[Assistant]):
        self.model = model

    async def create(
        self, client: AsyncClient, assistant: Assistant
    ) -> Assistant | None:
        """Create a new assistant."""
        data, _count = (
            await client.table("assistant_objects")
            .insert(assistant.model_dump())
            .execute()
        )

        _, response = data

        if response:
            return self.model(**response[0])
        return None

    async def get(self, client: AsyncClient, assistant_id: str) -> Assistant | None:
        """Get an assistant by its ID."""
        data, _count = (
            await client.table("assistant_objects")
            .select("*")
            .eq("id", assistant_id)
            .execute()
        )

        _, response = data

        if data:
            return self.model(**response[0])
        return None

    async def list(self, client: AsyncClient) -> list[Assistant] | None:
        """List all assistants."""
        data, _count = await client.table("assistant_objects").select("*").execute()

        _, response = data

        if response:
            return [self.model(**item) for item in response]
        return None

    async def update(
        self, client: AsyncClient, assistant_id: str, assistant: Assistant
    ) -> Assistant | None:
        """Update an assistant by its ID."""
        data, _count = (
            await client.table("assistant_objects")
            .update(assistant.model_dump())
            .eq("id", assistant_id)
            .execute()
        )

        _, response = data

        if response:
            return self.model(**response[0])
        return None

    async def delete(self, client: AsyncClient, assistant_id: str) -> AssistantDeleted:
        """Delete an assistant by its ID."""
        data, _count = (
            await client.table("assistant_objects")
            .delete()
            .eq("id", assistant_id)
            .execute()
        )

        _, response = data

        return AssistantDeleted(
            id=assistant_id, deleted=bool(response), object="assistant.deleted"
        )
