"""CRUD Operations for the Files Bucket."""

from supabase_py_async import AsyncClient
from fastapi import UploadFile

from leapfrogai_api.data.async_mixin import AsyncMixin
from leapfrogai_api.routers.supabase_session import get_user_session


class CRUDFileBucket(AsyncMixin):
    """CRUD Operations for FileBucket."""

    async def __ainit__(self, jwt: str, model: type[UploadFile]):
        self.client: AsyncClient = await get_user_session(jwt)
        self.model: type[UploadFile] = model

    async def upload(self, file: UploadFile, id_: str):
        """Upload a file to the file bucket."""

        return await self.client.storage.from_("file_bucket").upload(
            file=file.file.read(), path=f"{id_}"
        )

    async def download(self, id_: str):
        """Get a file from the file bucket."""

        return await self.client.storage.from_("public/file_bucket").download(path=f"{id_}")

    async def delete(self, id_: str):
        """Delete a file from the file bucket."""

        return await self.client.storage.from_("file_bucket").remove(paths=f"{id_}")
