""" Wrapper class for interacting with the Supabase database. """
import logging
import os
from dotenv import load_dotenv
from openai.types.beta import Assistant
from openai.types.beta.assistant import ToolResources
from supabase.client import Client, create_client
from leapfrogai_api.utils.openai_util import strings_to_tools, tools_to_strings


def get_connection() -> Client:
    """Get the connection to the Supabase database."""
    try:
        load_dotenv()
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        supabase: Client = create_client(
            supabase_url=supabase_url, supabase_key=supabase_key
        )
        return supabase
    except Exception as exc:
        logging.error("Unable to connect to the Supabase database")
        raise ConnectionError("Unable to connect to the Supabase database") from exc


class SupabaseWrapper:
    """Wrapper class for interacting with the Supabase database."""

    def __init__(self):
        pass

    ### Assistant Methods ###

    def upsert_assistant(self, assistant: Assistant, client: Client = get_connection()):
        """Create an assistant in the database."""

        try:
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
            return

        except Exception as exc:
            raise ValueError("Unable to create the assistant") from exc

    def list_assistants(self, client: Client = get_connection()):
        """List all the assistants in the database."""

        try:
            response = client.table("assistant_objects").select("*").execute()
            print(response.data[0]["tools"])
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

    def retrieve_assistant(self, assistant_id, client: Client = get_connection()):
        """Retrieve the assistant from the database."""

        try:
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

    def delete_assistant(self, assistant_id, client: Client = get_connection()):
        """Delete the assistant from the database."""

        try:
            client.table("assistant_objects").delete().eq("id", assistant_id).execute()
        except Exception as exc:
            raise FileNotFoundError(
                f"No assistant found with id: {assistant_id}"
            ) from exc
