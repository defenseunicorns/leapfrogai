from __future__ import annotations

import logging
from contextlib import suppress
from fastapi import HTTPException, status
from typing import Literal
from pydantic import BaseModel, Field

from openai.types.beta import Assistant
from openai.types.beta import AssistantTool
from openai.types.beta.assistant import (
    ToolResources as BetaAssistantToolResources,
    ToolResourcesFileSearch,
)
from openai.types.beta.assistant_tool import FileSearchTool

from leapfrogai_api.backend.rag.index import IndexingService
from leapfrogai_api.typedef.vectorstores import CreateVectorStoreRequest
from leapfrogai_api.data.crud_vector_store import CRUDVectorStore, FilterVectorStore
from leapfrogai_api.routers.supabase_session import Session
from leapfrogai_api.utils.validate_tools import (
    validate_assistant_tool,
    validate_tool_resources,
)


logger = logging.getLogger(__name__)


class BaseAssistantRequest(BaseModel):
    """
    Base Request object for creating or modifying an assistant.
    This class should not be used directly. Use CreateAssistantRequest or ModifyAssistantRequest instead.
    Model field is required for CreateAssistantRequest, but optional for ModifyAssistantRequest.
    """

    name: str | None = Field(
        default=None,
        examples=["Froggy Assistant"],
        description="The name of the assistant. Optional.",
    )
    description: str | None = Field(
        default=None,
        examples=["A helpful assistant."],
        description="A description of the assistant's purpose. Optional.",
    )
    instructions: str | None = Field(
        default=None,
        examples=["You are a helpful assistant."],
        description="Instructions that the assistant should follow. Optional.",
    )
    tools: list[AssistantTool] | None = Field(
        default=None,
        examples=[[FileSearchTool(type="file_search")]],
        description="List of tools the assistant can use. Optional.",
    )
    tool_resources: BetaAssistantToolResources | None = Field(
        default=None,
        examples=[
            BetaAssistantToolResources(
                file_search=ToolResourcesFileSearch(vector_store_ids=[])
            )
        ],
        description="Resources for the tools used by the assistant. Optional.",
    )
    metadata: dict | None = Field(
        default={},
        examples=[{}],
        description="Additional metadata for the assistant. Optional.",
    )
    temperature: float | None = Field(
        default=None,
        examples=[1.0],
        description="Sampling temperature for the model. Optional.",
    )
    top_p: float | None = Field(
        default=None,
        examples=[1.0],
        description="Nucleus sampling parameter. Optional.",
    )
    response_format: Literal["auto"] | None = Field(
        default=None,
        examples=["auto"],
        description="The format of the assistant's responses. Currently only 'auto' is supported. Optional.",
    )

    # helper function to check for unsupported tools/tool resources, and if a new vector store needs to be added
    async def request_checks_and_modifications(self, session: Session):
        """
        Performs checks and modifications that occur in both create and modify requests

        Checks performed:
        - unsupported tools
        - unsupported tool resources

        Modifications performed:
        - vector store creation
        """

        async def new_vector_store_from_file_ids():
            logger.debug("Creating vector store for new assistant")
            indexing_service = IndexingService(db=session)
            vector_store_params_dict = vector_stores[0]

            if "file_ids" not in vector_store_params_dict:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="ToolResourcesFileSearchVectorStores found but no file ids were provided",
                )

            if not await indexing_service.file_ids_are_valid(
                vector_store_params_dict["file_ids"]
            ):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid file ids attached to assistants request",
                )

            vector_store_request = CreateVectorStoreRequest(
                file_ids=vector_store_params_dict["file_ids"],
                name="{}_vector_store".format(self.name),
                expires_after=None,
                metadata={},
            )

            vector_store = await indexing_service.create_new_vector_store(
                vector_store_request
            )

            self.tool_resources.file_search.vector_store_ids = [vector_store.id]

        async def attach_existing_vector_store_from_id():
            logger.debug(
                "Attaching vector store with id: {} to new assistant".format(ids[0])
            )
            crud_vector_store = CRUDVectorStore(db=session)
            try:
                existing_vector_store = await crud_vector_store.get(
                    filters=FilterVectorStore(id=ids[0])
                )
                if existing_vector_store is None:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Provided vector store id was not found",
                    )
            except Exception:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid vector store id was provided",
                )

        # check for unsupported tools
        if self.tools:
            for tool in self.tools:
                if not validate_assistant_tool(tool):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Unsupported tool type: {tool.type}",
                    )

        # check for unsupported tool resources
        if self.tool_resources and not validate_tool_resources(self.tool_resources):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported tool resource: {self.tool_resources}",
            )

        # check if a vector store needs to be built or added to this assistant
        if self.tool_resources and self.tool_resources.file_search is not None:
            ids = self.tool_resources.file_search.vector_store_ids or []
            vector_stores = (
                getattr(self.tool_resources.file_search, "vector_stores", []) or []
            )

            ids_len = len(ids)
            vector_stores_len = len(list(vector_stores))

            # too many ids or vector_stores provided
            if (ids_len + vector_stores_len) > 1:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="There can be a maximum of 1 vector store attached to the assistant",
                )

            # new vector store requested from file ids
            elif vector_stores_len == 1:
                await new_vector_store_from_file_ids()

            # attach already existing vector store from its id
            elif ids_len == 1:
                await attach_existing_vector_store_from_id()

            # nothing provided, no changes made
            else:
                logger.debug(
                    "No files or vector store id found; assistant will be created with no vector store"
                )

            # ensure the vector_stores field is removed regardless, if it exists
            with suppress(AttributeError):
                self.tool_resources.file_search.vector_stores = None


class CreateAssistantRequest(BaseAssistantRequest):
    """Request object for creating an assistant."""

    model: str = Field(
        default="llama-cpp-python",
        examples=["llama-cpp-python"],
        description="The model to be used by the assistant. Default is 'llama-cpp-python'.",
    )


class ModifyAssistantRequest(BaseAssistantRequest):
    """Request object for modifying an assistant."""

    model: str | None = Field(
        default=None,
        examples=["llama-cpp-python", None],
        description="The model to be used by the assistant. Default is 'llama-cpp-python'.",
    )


class ListAssistantsResponse(BaseModel):
    """Response object for listing assistants."""

    object: Literal["list"] = Field(
        default="list",
        description="The type of object. Always 'list' for this response.",
    )
    data: list[Assistant] = Field(description="A list of Assistant objects.")
