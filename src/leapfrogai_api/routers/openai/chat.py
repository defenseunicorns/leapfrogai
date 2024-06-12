"""OpenAI Chat API router."""

from typing import Annotated
from fastapi import HTTPException, APIRouter, Depends
from fastapi.security import HTTPBearer
from leapfrogai_api.backend.grpc_client import (
    chat_completion,
    stream_chat_completion,
)
from leapfrogai_api.backend.helpers import grpc_chat_role
from leapfrogai_api.routers.supabase_session import Session
from leapfrogai_api.utils import get_model_config
from leapfrogai_api.utils.config import Config
from leapfrogai_api.backend.types import ChatCompletionRequest
import leapfrogai_sdk as lfai

router = APIRouter(prefix="/openai/v1/chat", tags=["openai/chat"])
security = HTTPBearer()


@router.post("/completions")
async def chat_complete(
    req: ChatCompletionRequest,
    model_config: Annotated[Config, Depends(get_model_config)],
    session: Session,
):
    """Complete a chat conversation with the given model."""

    model = model_config.get_model_backend(req.model)
    if model is None:
        raise HTTPException(
            status_code=405,
            detail=f"Model {req.model} not found. Currently supported models are {list(model_config.models.keys())}",
        )

    chat_items: list[lfai.ChatItem] = []
    for m in req.messages:
        chat_items.append(lfai.ChatItem(role=grpc_chat_role(m.role), content=m.content))
    request = lfai.ChatCompletionRequest(
        chat_items=chat_items,
        max_new_tokens=req.max_tokens,
        temperature=req.temperature,
    )

    if req.stream:
        return await stream_chat_completion(model, request)
    else:
        return await chat_completion(model, request)
