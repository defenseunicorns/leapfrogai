"""CRUD Operations for FileObject"""

from supabase_py_async import AsyncClient
from openai.types import FileObject, FileDeleted


class CRUDFileObject:
    """CRUD Operations for FileObject"""

    def __init__(self, model: type[FileObject]):
        self.model = model

    async def create(
        self, client: AsyncClient, file_object: FileObject
    ) -> FileObject | None:
        """Create a new file object."""
        data, _count = (
            await client.table("file_objects")
            .insert(file_object.model_dump())
            .execute()
        )

        _, response = data

        if response:
            return self.model(**response[0])
        return None

    async def get(self, client: AsyncClient, file_id: str) -> FileObject | None:
        """Get a file object by its ID."""
        data, _count = (
            await client.table("file_objects").select("*").eq("id", file_id).execute()
        )

        _, response = data

        if response:
            return self.model(**response[0])
        return None

    async def list(self, client: AsyncClient) -> list[FileObject] | None:
        """List all file objects."""
        data, _count = await client.table("file_objects").select("*").execute()

        _, response = data

        if response:
            return [self.model(**item) for item in response]
        return None

    async def update(
        self, client: AsyncClient, file_id: str, file_object: FileObject
    ) -> FileObject | None:
        """Update a file object by its ID."""
        data, _count = (
            await client.table("file_objects")
            .update(file_object.model_dump())
            .eq("id", file_id)
            .execute()
        )

        _, response = data

        if response:
            return self.model(**response[0])
        return None

    async def delete(self, client: AsyncClient, file_id: str) -> FileDeleted:
        """Delete a file object by its ID."""
        data, _count = (
            await client.table("file_objects").delete().eq("id", file_id).execute()
        )

        _, response = data

        return FileDeleted(id=file_id, deleted=bool(response), object="file")
