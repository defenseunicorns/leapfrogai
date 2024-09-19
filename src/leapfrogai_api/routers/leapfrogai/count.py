from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from leapfrogai_api.routers.supabase_session import Session
from leapfrogai_api.utils.config import Config
from leapfrogai_api.utils import get_model_config
from leapfrogai_api.typedef.counting import (
    TokenCountRequestHttp,
    TokenCountResponseHttp,
)
from leapfrogai_api.backend.grpc_client import create_token_count
import leapfrogai_sdk as lfai

router = APIRouter(prefix="/leapfrogai/v1/count", tags=["leapfrogai/count"])


@router.post("/tokens")
async def tokens(
    session: Session,
    model_config: Annotated[Config, Depends(get_model_config)],
    request: TokenCountRequestHttp,
) -> TokenCountResponseHttp:
    model = model_config.get_model_backend(request.model)

    if not model:
        raise HTTPException(
            status_code=404, detail=f"Model '{request.model}' not found"
        )

    try:
        return await create_token_count(
            model, lfai.TokenCountRequest(text=request.text)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error counting tokens: {str(e)}")
