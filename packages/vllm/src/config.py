from typing import Literal, Optional

from confz import BaseConfig, EnvSource
from pydantic import Field


class ConfigOptions(BaseConfig):
    model_path: str = Field(
        title="Model Files Location",
        description="Location of the model files to be loaded into the vLLM engine.",
        examples=["/data/.model"],
    )
    tensor_parallel_size: int = Field(
        title="GPU Utilization Count",
        description="The number of gpus to spread the tensor processing across."
        "This must be divisible to the number of attention heads in the model",
        examples=[1, 2, 3],
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
        examples=[0.50, 0.90, 0.99],
    )
    engine_use_ray: bool = Field(
        title="Use Ray for Engine",
        description="Enable distributed inferencing for multi-node situations.",
        examples=[True, False],
    )
    worker_use_ray: bool = Field(
        title="Use Ray for Worker",
        description="Enable distributed inferencing for multi-node situations.",
        examples=[True, False],
    )
    trust_remote_code: bool = Field(
        title="Trust Downloaded Model Code",
        description="Whether to trust inferencing code downloaded as part of the model download."
        "Please review the Python code in the .model/ directory before trusting custom model code.",
        examples=[True, False],
    )


class DownloadOptions(BaseConfig):
    hf_hub_enable_hf_transfer: Literal["0", "1"] = Field(
        description="Option (0 - Disable, 1 - Enable) for faster transfers, tradeoff stability for faster speeds"
    )
    repo_id: str = Field(
        description="The HuggingFace git repository ID",
        examples=[
            "TheBloke/Synthia-7B-v2.0-GPTQ",
            "migtissera/Synthia-MoE-v3-Mixtral-8x7B",
            "microsoft/phi-2",
        ],
    )
    revision: str = Field(
        description="The HuggingFace repository git branch to use",
        examples=["main", "gptq-4bit-64g-actorder_True"],
    )


class AppConfig(BaseConfig):
    backend_options: ConfigOptions
    CONFIG_SOURCES = [
        EnvSource(
            allow_all=True,
            prefix="LAI_",
            remap={
                "model_path": "backend_options.model_path",
                "tensor_parallel_size": "backend_options.tensor_parallel_size",
                "trust_remote_code": "backend_options.trust_remote_code",
                "enforce_eager": "backend_options.enforce_eager",
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
            prefix="LAI_",
            remap={
                "hf_hub_enable_hf_transfer": "download_options.hf_hub_enable_hf_transfer",
                "repo_id": "download_options.repo_id",
                "revision": "download_options.revision",
            },
        )
    ]
