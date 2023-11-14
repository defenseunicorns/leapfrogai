
import asyncio
from typing import Generator, Any, List

from leapfrogai import (
    ChatCompletionRequest,
    ChatCompletionResponse,
    ChatCompletionChoice,
    ChatItem,
    ChatRole
    )

from leapfrogai import (
    CompletionRequest,
    CompletionResponse,
    CompletionChoice
)

from leapfrogai import GrpcContext, serve
from leapfrogai import BackendConfig

from pydantic import BaseModel

class GenerationConfig(BaseModel):
    max_new_tokens: int
    temperature: float
    top_k: float
    top_p: float
    do_sample: bool
    n: int
    stop: List[str]
    repetition_penalty: float
    presence_penalty: float
    frequency_penalty: float
    best_of: str
    logit_bias: dict[str, int]
    return_full_text: bool
    truncate: int
    typical_p: float
    watermark: bool
    seed: int

def LLM(_cls):
    if not hasattr(_cls, "generate"):
        raise ValueError("LLM class requires a generate method")
    
    class NewClass(_cls):
        config: BackendConfig
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.config = BackendConfig()
            
        def _build_gen_stream(self, prompt: str, request: ChatCompletionRequest | CompletionRequest) -> Generator[str, Any, Any]:
            config = GenerationConfig(
                max_new_tokens=request.max_new_tokens,
                temperature=request.temperature,
                top_k=request.top_k,
                top_p=request.top_p,
                do_sample=request.do_sample,
                n=request.n,
                stop=request.stop,
                repetition_penalty=request.repetition_penalty,
                presence_penalty=request.presence_penalty,
                frequency_penalty=request.frequency_penalty,
                best_of=request.best_of,
                logit_bias=request.logit_bias,
                return_full_text=request.return_full_text,
                truncate=request.truncate,
                typical_p=request.typical_p,
                watermark=request.watermark,
                seed=request.seed
            )
            return self.generate(prompt, config) 
        
        async def ChatComplete(self, request: ChatCompletionRequest, context: GrpcContext) -> ChatCompletionResponse:
            gen_stream = self._build_gen_stream(self.config.apply_chat_template(request.chat_items), request)
            
            content = ""
            for text_chunk in gen_stream:
                content += text_chunk
                
            item = ChatItem(role=ChatRole.ASSISTANT, content=content)
            choice = ChatCompletionChoice(index=0, chat_item=item)
            return ChatCompletionResponse(choices=[choice])
        
        async def ChatCompleteStream(self, request: ChatCompletionRequest, context: GrpcContext) -> Generator[ChatCompletionResponse, Any, Any]:
            gen_stream = self._build_gen_stream(self.config.apply_chat_template(request.chat_items), request)
            
            for text_chunk in gen_stream:
                item = ChatItem(role=ChatRole.ASSISTANT, content=text_chunk)
                choice = ChatCompletionChoice(index=0, chat_item=item)

                yield ChatCompletionResponse(choices=[choice]) 
        
        async def Complete(self, request: CompletionRequest, context: GrpcContext) -> CompletionResponse:
            gen_stream = self._build_gen_stream(request.prompt, request) 
            
            content = ""
            for text_chunk in gen_stream:
                content += text_chunk
                
            choice = CompletionChoice(index=0, text=content)
            return CompletionResponse(choices=[choice])
        
        async def CompleteStream(self, request: CompletionRequest, context: GrpcContext) -> Generator[CompletionResponse, Any, Any]:
            gen_stream = self._build_gen_stream(request.prompt, request) 
            for text_chunk in gen_stream:
                choice = CompletionChoice(index=0, text=text_chunk)
                yield CompletionResponse(choices=[choice])
        
        def serve(self):
            asyncio.run(serve(self))
            
    NewClass.__name__ = _cls.__name__
    return NewClass