from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from leapfrogai_api.routers.supabase_session import Session
from leapfrogai_api.utils.config import Config
from leapfrogai_api.utils import get_model_config
from leapfrogai_api.typedef.counting import TokenCountRequest, TokenCountResponse
from leapfrogai_api.backend.grpc_client import token_count as count_tokens
import leapfrogai_sdk as lfai

router = APIRouter(prefix="/leapfrogai/v1/token_count", tags=["leapfrogai/token_count"])


@router.post("/token_count", response_model=TokenCountResponse)
async def token_count(
    session: Session,
    model_config: Annotated[Config, Depends(get_model_config)],
    request: TokenCountRequest,
) -> TokenCountResponse:
    model = model_config.get_model_backend(request.model)

    if not model:
        raise HTTPException(
            status_code=404, detail=f"Model '{request.model}' not found"
        )

    try:
        return await count_tokens(model, lfai.TokenCountRequest(text=request.text))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error counting tokens: {str(e)}")
