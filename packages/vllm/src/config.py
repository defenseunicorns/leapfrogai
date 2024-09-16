from typing import Literal, Optional

from confz import BaseConfig, EnvSource
from pydantic import Field


class ConfigOptions(BaseConfig):
    tensor_parallel_size: int = Field(
        default=1,
        title="GPU Utilization Count",
        description="The number of gpus to spread the tensor processing across."
        "This must be divisible to the number of attention heads in the model",
        examples=[1, 2, 3],
    )
    quantization: Literal[
        "aqlm",
        "awq",
        "deepspeedfp",
        "fp8",
        "marlin",
        "gptq_marlin_24",
        "gptq_marlin",
        "gptq",
        "squeezellm",
        "sparseml",
        "None",
        "",
    ] = Field(
        title="quantization",
        description="Quantization type of the model"
        "Force GPTQ instead of GPTQ_Marlin by explicitly providing `gptq` as value.",
        examples=["awq", "fp8", "gptq_marlin", "gptq", "squeezellm", "None"],
    )
    enforce_eager: bool = Field(
        title="Enable Eager Mode",
        description="Enable eager mode to start token generation immediately after prompt processing."
        "Potentially reduces initial latency at the cost of slightly higher memory usage."
        "Should be set to False in production environments with higher GPU memory.",
        examples=[True, False],
    )
    gpu_memory_utilization: float = Field(
        title="GPU Memory Limit",
        description="Maximum amount of GPU vRAM allocated to the vLLM engine and worker(s)",
        examples=[0.50, 0.80, 0.90],
    )
    engine_use_ray: bool = Field(
        title="Use Ray for Engine",
        description="If True, uses Ray for managing the execution engine. Allows for distributed inferencing in multi-node situations.",
        examples=[True, False],
    )
    worker_use_ray: bool = Field(
        title="Use Ray for Worker",
        description="If True, uses Ray for distributed worker management. Allows for distributed inferencing in multi-node situations.",
        examples=[True, False],
    )
    trust_remote_code: bool = Field(
        title="Trust Downloaded Model Code",
        description="Whether to trust inferencing code downloaded as part of the model download."
        "Please review the Python code in the .model/ directory before trusting custom model code.",
        examples=[True, False],
    )


class DownloadOptions(BaseConfig):
    repo_id: str = Field(
        description="The HuggingFace git repository ID",
        examples=[
            "defenseunicorns/Hermes-2-Pro-Mistral-7B-4bit-32g",
            "justinthelaw/Phi-3-mini-128k-instruct-4bit-128g",
        ],
    )
    revision: str = Field(
        description="The HuggingFace repository git branch to use",
        examples=["main", "gptq-4bit-64g-actorder_True"],
    )


# vLLM specific runtime configuration options
class AppConfig(BaseConfig):
    backend_options: ConfigOptions
    CONFIG_SOURCES = [
        EnvSource(
            allow_all=True,
            prefix="VLLM_",
            remap={
                "tensor_parallel_size": "backend_options.tensor_parallel_size",
                "trust_remote_code": "backend_options.trust_remote_code",
                "enforce_eager": "backend_options.enforce_eager",
                "quantization": "backend_options.quantization",
                "gpu_memory_utilization": "backend_options.gpu_memory_utilization",
                "worker_use_ray": "backend_options.worker_use_ray",
                "engine_use_ray": "backend_options.engine_use_ray",
            },
        )
    ]


class DownloadConfig(BaseConfig):
    download_options: Optional[DownloadOptions]
    CONFIG_SOURCES = [
        EnvSource(
            allow_all=True,
            prefix="LFAI_",
            remap={
                "repo_id": "download_options.repo_id",
                "revision": "download_options.revision",
            },
        )
    ]
