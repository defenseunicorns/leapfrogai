"""CRUD Operations for ThreadObject."""

from supabase_py_async import AsyncClient
from openai.types.beta import Thread, ThreadDeleted


class CRUDThreadObject:
    """CRUD Operations for ThreadObject"""

    def __init__(self, model: type[Thread]):
        self.model = model

    async def create(self, client: AsyncClient, thread_object: Thread) -> Thread | None:
        """Create a new thread object."""
        data, _count = (
            await client.table("thread_objects")
            .insert(thread_object.model_dump())
            .execute()
        )

        _, response = data

        if response:
            return self.model(**response[0])
        return None

    async def get(self, client: AsyncClient, thread_id: str) -> Thread | None:
        """Get a thread object by its ID."""
        data, _count = (
            await client.table("thread_objects")
            .select("*")
            .eq("id", thread_id)
            .execute()
        )

        _, response = data

        if data:
            return self.model(**response[0])
        return None

    async def list(self, client: AsyncClient) -> list[Thread] | None:
        """List all thread objects."""
        data, _count = await client.table("thread_objects").select("*").execute()

        _, response = data

        if response:
            return [self.model(**item) for item in response]
        return None

    async def update(
        self, client: AsyncClient, thread_id: str, thread_object: Thread
    ) -> Thread | None:
        """Update a thread object by its ID."""
        data, _count = (
            await client.table("thread_objects")
            .update(thread_object.model_dump())
            .eq("id", thread_id)
            .execute()
        )

        _, response = data

        if response:
            return self.model(**response[0])
        return None

    async def delete(self, client: AsyncClient, thread_id: str) -> ThreadDeleted:
        """Delete a thread object by its ID."""
        data, _count = (
            await client.table("thread_objects").delete().eq("id", thread_id).execute()
        )

        return ThreadDeleted(id=thread_id)
