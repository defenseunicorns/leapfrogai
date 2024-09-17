from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict
from leapfrogai_api.utils.config import get_model_config, Model
import grpc
import leapfrogai_pb2
import leapfrogai_pb2_grpc

router = APIRouter()


class TokenCountRequest(BaseModel):
    model: str
    text: str


class TokenCountResponse(BaseModel):
    token_count: int


async def count_tokens_grpc(model: Model, text: str) -> int:
    async with grpc.aio.insecure_channel(f"{model.backend}:50051") as channel:
        stub = leapfrogai_pb2_grpc.LLMStub(channel)
        request = leapfrogai_pb2.TokenCountRequest(text=text)
        response = await stub.CountTokens(request)
        return response.count


@router.post("/token_count", response_model=TokenCountResponse)
async def token_count(request: TokenCountRequest) -> Dict[str, int]:
    model_config = get_model_config()
    model = model_config.models.get(request.model)

    if not model:
        raise HTTPException(
            status_code=404, detail=f"Model '{request.model}' not found"
        )

    try:
        token_count = await count_tokens_grpc(model, request.text)
        return {"token_count": token_count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error counting tokens: {str(e)}")
