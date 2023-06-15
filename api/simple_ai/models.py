import os
import pathlib
import sys
from dataclasses import dataclass
from typing import Any, Iterable, Union

import grpc
import httpx
import leapfrog

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

path = pathlib.Path(os.environ.get("SIMPLEAI_CONFIG_PATH", "models.toml"))
with path.open(mode="rb") as fp:
    MODELS_ZOO = tomllib.load(fp)


@dataclass(unsafe_hash=True)
class RpcCompletionLanguageModel:
    name: str
    url: str

    def complete(
        self,
        prompt: str = "<|endoftext|>",
        suffix: str = "",
        max_tokens: int = 7,
        temperature: float = 1.0,
        top_p: float = 1.0,
        n: int = 1,
        stream: bool = False,
        logprobs: int = 0,
        echo: bool = False,
        stop: str = "",
        presence_penalty: float = 0.0,
        frequence_penalty: float = 0.0,
        best_of: int = 0,
        logit_bias: dict = {},
    ) -> str:
        with grpc.insecure_channel(self.url) as channel:
            stub = leapfrog.CompletionServiceStub(channel)
            request = leapfrog.CompletionRequest(
                prompt=prompt,
                suffix=suffix,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
                n=n,
                stream=stream,
                logprobs=logprobs,
                echo=echo,
                stop=stop,
                presence_penalty=presence_penalty,
                frequence_penalty=frequence_penalty,
                best_of=best_of,
                logit_bias=logit_bias
            )

            response: leapfrog.CompletionResponse = stub.Complete(request)
            return response.completion


@dataclass(unsafe_hash=True)
class RpcEmbeddingLanguageModel:
    name: str
    url: str

    def embed(
        self,
        inputs: Union[str, list] = "",
    ) -> Iterable[str]:
        with grpc.insecure_channel(self.url) as channel:
            stub = leapfrog.EmbeddingsServiceStub(channel)
            request = leapfrog.EmbeddingRequest(inputs=inputs)
            response: leapfrog.EmbeddingResponse = stub.CreateEmbedding(
                request)
            return response.embeddings


@dataclass(unsafe_hash=True)
class HttpClientAudioModel:
    name: str
    url: str

    async def run(self, audio, task: str, source_language: str = "en") -> str:
        async with httpx.AsyncClient() as client:
            files = {"file": audio.file}
            data = {"task": task, "language": source_language}
            response = await client.post(
                f"{self.url}/transcribe", files=files, data=data, timeout=None
            )
            return response.json()["result"]


def select_model_type(model_interface: str = "gRPC", task: str = "complete"):
    if model_interface == "gRPC":
        if task == "embed":
            return RpcEmbeddingLanguageModel
        return RpcCompletionLanguageModel
    if model_interface == "http":
        return HttpClientAudioModel
    return RpcCompletionLanguageModel


def get_model(model_id: str, metadata: dict = MODELS_ZOO, task: str = "complete"):
    if model_id in metadata.keys():
        model_interface = metadata.get(model_id).get("network", dict())
        model_url = model_interface.get("url", None)
        model_interface = model_interface.get("type", None)
        return select_model_type(model_interface, task)(name=model_id, url=model_url)
    else:
        return None


def list_models(metadata: dict = MODELS_ZOO) -> dict[str, list[dict[str, Any]] | str]:
    return dict(
        data=[{"id": key, **meta.get("metadata")}
              for key, meta in metadata.items()],
        object="list",
    )


def get_model_infos(model_id, metadata: dict = MODELS_ZOO) -> dict[str, Any]:
    if model_id in metadata.keys():
        return {"id": model_id, **metadata.get(model_id).get("metadata")}
    return {}
