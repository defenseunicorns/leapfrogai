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
    trust_remote_code: bool = Field(
        default=True,
        title="Trust Downloaded Model Code",
        description="Whether to trust code downloaded as part of the model download."
        "Please review the Python scripts in the .model/ directory before trusting custom model code.",
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
                "tensor_parallel_size": "backend_options.tensor_parallel_size",
                "trust_remote_code": "backend_options.trust_remote_code",
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
