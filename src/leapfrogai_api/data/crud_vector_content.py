"""CRUD Operations for VectorStore."""

from supabase import AClient as AsyncClient
from leapfrogai_api.data.crud_base import get_user_id
import ast
from leapfrogai_api.typedef.vectorstores import SearchItem, SearchResponse
from leapfrogai_api.backend.constants import TOP_K
from leapfrogai_api.typedef.vectorstores import Vector


class CRUDVectorContent:
    """CRUD Operations for VectorStore"""

    def __init__(self, db: AsyncClient):
        self.db = db
        self.table_name = "vector_content"

    async def add_vectors(self, object_: list[Vector]) -> list[Vector]:
        """Create new row."""

        user_id = await get_user_id(self.db)

        rows = []

        for vector in object_:
            dict_ = vector.model_dump()
            dict_["user_id"] = user_id
            if "id" in dict_:
                del dict_["id"]

            rows.append(dict_)

        data, _count = await self.db.table(self.table_name).insert(rows).execute()

        _, response = data

        final_response = []
        try:
            for item in response:
                if "user_id" in item:
                    del item["user_id"]
                if isinstance(item["embedding"], str):
                    item["embedding"] = self.string_to_float_list(item["embedding"])
                final_response.append(
                    Vector(
                        id=item["id"],
                        vector_store_id=item["vector_store_id"],
                        file_id=item["file_id"],
                        content=item["content"],
                        metadata=item["metadata"],
                        embedding=item["embedding"],
                    )
                )

            return final_response
        except Exception as e:
            raise e

    async def get_vector(self, vector_id: str) -> Vector:
        """Get a vector by its ID."""
        data, _count = (
            await self.db.table(self.table_name)
            .select("*")
            .eq("id", vector_id)
            .single()
            .execute()
        )

        _, response = data

        if isinstance(response["embedding"], str):
            response["embedding"] = self.string_to_float_list(response["embedding"])

        return Vector(
            id=response["id"],
            vector_store_id=response["vector_store_id"],
            file_id=response["file_id"],
            content=response["content"],
            metadata=response["metadata"],
            embedding=response["embedding"],
        )

    async def delete_vectors(self, vector_store_id: str, file_id: str) -> bool:
        """Delete a vector store file by its ID."""
        data, _count = (
            await self.db.table(self.table_name)
            .delete()
            .eq("vector_store_id", vector_store_id)
            .eq("file_id", file_id)
            .execute()
        )

        _, response = data

        return bool(response)

    async def similarity_search(
        self, query: list[float], vector_store_id: str, k: int = TOP_K
    ) -> SearchResponse:
        user_id = await get_user_id(self.db)

        params = {
            "query_embedding": query,
            "match_limit": k,
            "vs_id": vector_store_id,
            "user_id": user_id,
        }

        result = await self.db.rpc("match_vectors", params).execute()

        try:
            response = result.data
            return SearchResponse(data=[SearchItem(**item) for item in response])
        except Exception as e:
            raise e

    @staticmethod
    def string_to_float_list(s: str) -> list[float]:
        try:
            # Remove any whitespace and convert to a Python list
            cleaned_string = s.strip()
            python_list = ast.literal_eval(cleaned_string)

            # Convert all elements to float
            return [float(x) for x in python_list]
        except (ValueError, SyntaxError) as e:
            raise e
