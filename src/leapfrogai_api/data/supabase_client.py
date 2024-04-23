"""Wrapper class for interacting with the Supabase database."""

import logging
import os
from typing import List
from fastapi import UploadFile
from openai.types import FileObject, FileDeleted
from openai.types.beta import Assistant, AssistantDeleted
from openai.types.beta.assistant import ToolResources
from supabase.client import Client, create_client
from leapfrogai_api.utils.openai_util import strings_to_tools, tools_to_strings


def get_connection(
    supabase_url=os.getenv("SUPABASE_URL"), supabase_key=os.getenv("SUPABASE_KEY")
) -> Client:
    """Get the connection to the Supabase database."""

    if not supabase_url or not supabase_key:
        raise ConnectionError("Invalid Supabase URL or Key provided.")

    try:
        supabase: Client = create_client(
            supabase_url=supabase_url, supabase_key=supabase_key
        )
        return supabase
    except Exception as exc:
        logging.error("Unable to connect to Supabase database at %s", supabase_url)
        raise ConnectionError(
            f"Unable to connect to Supabase database at {supabase_url}"
        ) from exc


def test_connection(
    supabase_url=os.getenv("SUPABASE_URL"), supabase_key=os.getenv("SUPABASE_KEY")
) -> bool:
    """Test the connection to the Supabase database."""

    if not supabase_url or not supabase_key:
        logging.error("Invalid Supabase URL or Key provided.")
        return False

    try:
        supabase = get_connection(supabase_url=supabase_url, supabase_key=supabase_key)
        supabase.storage.from_("file_bucket").list()
        return True
    except Exception:
        logging.error(
            "Unable to connect to the Supabase database at %s",
            os.getenv("SUPABASE_URL"),
        )
        return False


class SupabaseWrapper:
    """Wrapper class for interacting with the Supabase database."""

    def __init__(self, client: Client = None):
        pass

    ### File Methods ###

    def upsert_file(
        self,
        file: UploadFile,
        file_object: FileObject,
        client: Client = None,
    ) -> FileObject:
        """Upsert the documents and their embeddings in the database."""

        try:
            client = client if client else get_connection()
            client.table("file_objects").upsert(
                [
                    {
                        "id": file_object.id,
                        "bytes": file_object.bytes,
                        "created_at": file_object.created_at,
                        "filename": file_object.filename,
                        "object": file_object.object,
                        "purpose": file_object.purpose,
                        "status": file_object.status,
                        "status_details": file_object.status_details,
                    }
                ]
            ).execute()

            client.storage.from_("file_bucket").upload(
                file=file.file.read(), path=f"{file_object.id}"
            )
            return file_object
        except Exception as exc:
            raise FileNotFoundError("Unable to store file") from exc

    def list_files(
        self, purpose: str = "assistants", client: Client = None
    ) -> List[FileObject]:
        """List all the files in the database."""

        try:
            client = client if client else get_connection()
            response = (
                client.table("file_objects")
                .select("*")
                .eq("purpose", purpose)
                .execute()
            )
            file_objects = [
                FileObject(
                    id=data["id"],
                    bytes=data["bytes"],
                    created_at=data["created_at"],
                    filename=data["filename"],
                    object=data["object"],
                    purpose=data["purpose"],
                    status=data["status"],
                    status_details=data["status_details"],
                )
                for data in response.data
            ]
            return file_objects
        except Exception as exc:
            raise FileNotFoundError("No file objects found in the database") from exc

    def get_file_object(self, file_id: str, client: Client = None) -> FileObject:
        """Get the file object from the database."""

        try:
            client = client if client else get_connection()
            response = (
                client.table("file_objects").select("*").eq("id", file_id).execute()
            )
        except Exception as exc:
            raise FileNotFoundError(
                f"No file found with the given id: {file_id}"
            ) from exc

        if len(response.data) == 0:
            raise FileNotFoundError(f"No file found with the given id: {file_id}")

        if len(response.data) > 1:
            raise ValueError("Multiple files found with the same id")

        data = response.data[0]
        file_object = FileObject(
            id=data["id"],
            bytes=data["bytes"],
            created_at=data["created_at"],
            filename=data["filename"],
            object=data["object"],
            purpose=data["purpose"],
            status=data["status"],
            status_details=data["status_details"],
        )
        return file_object

    def delete_file(self, file_id: str, client: Client = None) -> FileDeleted:
        """Delete the file and its vectors from the database."""

        try:
            client = client if client else get_connection()
            # Delete the file object
            file_path = (
                client.table("file_objects")
                .select("filename")
                .eq("id", file_id)
                .execute()
                .data
            )

            if len(file_path) == 0:
                raise FileNotFoundError(
                    f"Delete FileObject: No file found with id: {file_id}"
                )

            client.table("file_objects").delete().eq("id", file_id).execute()
        except Exception as exc:
            raise FileNotFoundError(
                f"Delete FileObject: No file found with id: {file_id}"
            ) from exc

        try:
            # Delete the file from bucket
            client.storage.from_("file_bucket").remove(f"{file_id}")
        except Exception as exc:
            raise FileNotFoundError(
                f"Delete File: No file found with id: {file_id}"
            ) from exc

        return FileDeleted(id=file_id, object="file", deleted=True)

    def get_file_content(self, file_id: str, client: Client = None):
        """Get the file content from the bucket."""

        try:
            client = client if client else get_connection()
            file_path = (
                client.table("file_objects")
                .select("filename")
                .eq("id", file_id)
                .execute()
                .data
            )

            file_path = file_path[0]["filename"]
            return client.storage.from_("file_bucket").download(f"{file_id}")
        except Exception as exc:
            raise FileNotFoundError(
                f"Get FileContent: No file found with id: {file_id}"
            ) from exc

    ### Assistant Methods ###

    def upsert_assistant(
        self, assistant: Assistant, client: Client = None
    ) -> Assistant:
        """Create an assistant in the database."""

        try:
            client = client if client else get_connection()
            client.table("assistant_objects").upsert(
                [
                    {
                        "id": assistant.id,
                        "object": assistant.object,
                        "created_at": assistant.created_at,
                        "name": assistant.name,
                        "description": assistant.description,
                        "model": assistant.model,
                        "instructions": assistant.instructions,
                        "tools": tools_to_strings(assistant.tools),
                        "tool_resources": ToolResources.model_dump_json(
                            assistant.tool_resources
                        ),
                        "metadata": assistant.metadata,
                        "top_p": assistant.top_p,
                        "temperature": assistant.temperature,
                        "response_format": assistant.response_format,
                    }
                ]
            ).execute()
            return assistant

        except Exception as exc:
            raise ValueError("Unable to create the assistant") from exc

    def list_assistants(self, client: Client = None) -> List[Assistant]:
        """List all the assistants in the database."""

        try:
            client = client if client else get_connection()
            response = client.table("assistant_objects").select("*").execute()
            assistants = [
                Assistant(
                    id=data["id"],
                    object=data["object"],
                    created_at=data["created_at"],
                    name=data["name"],
                    description=data["description"],
                    model=data["model"],
                    instructions=data["instructions"],
                    tools=strings_to_tools(data["tools"]),
                    tool_resources=ToolResources.model_validate_json(
                        data["tool_resources"]
                    ),
                    metadata=data["metadata"],
                    top_p=data["top_p"],
                    temperature=data["temperature"],
                    response_format=data["response_format"],
                )
                for data in response.data
            ]
            return assistants
        except Exception as exc:
            raise FileNotFoundError(
                "No assistant objects found in the database"
            ) from exc

    def retrieve_assistant(self, assistant_id: str, client: Client = None) -> Assistant:
        """Retrieve the assistant from the database."""

        try:
            client = client if client else get_connection()
            response = (
                client.table("assistant_objects")
                .select("*")
                .eq("id", assistant_id)
                .execute()
            )
            data = response.data[0]
            assistant = Assistant(
                id=data["id"],
                object=data["object"],
                created_at=data["created_at"],
                name=data["name"],
                description=data["description"],
                model=data["model"],
                instructions=data["instructions"],
                tools=strings_to_tools(data["tools"]),
                tool_resources=ToolResources.model_validate_json(
                    data["tool_resources"]
                ),
                metadata=data["metadata"],
                top_p=data["top_p"],
                temperature=data["temperature"],
                response_format=data["response_format"],
            )
            return assistant
        except Exception as exc:
            raise FileNotFoundError(
                f"No assistant found with id: {assistant_id}"
            ) from exc

    def delete_assistant(
        self, assistant_id: str, client: Client = None
    ) -> AssistantDeleted:
        """Delete the assistant from the database."""

        try:
            client = client if client else get_connection()
            client.table("assistant_objects").delete().eq("id", assistant_id).execute()
            return AssistantDeleted(
                id=assistant_id, deleted=True, object="assistant.deleted"
            )
        except Exception as exc:
            raise FileNotFoundError(
                f"No assistant found with id: {assistant_id}"
            ) from exc
