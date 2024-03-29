from typing import Literal, Optional

from confz import BaseConfig, EnvSource
from pydantic import Field


class ConfigOptions(BaseConfig):
    quantization: Literal[None, "awq", "gptq", "squeezellm"] = Field(
        default=None,
        description="Type of quantization, for un-quantized models omit this field",
    )


class DownloadOptions(BaseConfig):
    hf_hub_enable_hf_transfer: Literal["0", "1"] = Field(
        description="Option (0 - Disable, 1 - Enable) for faster transfers, tradeoff stability for faster speeds"
    )
    repo_id: str = Field(
        description="HuggingFace repo id",
        examples=[
            "TheBloke/Synthia-7B-v2.0-GPTQ",
            "migtissera/Synthia-MoE-v3-Mixtral-8x7B",
            "microsoft/phi-2",
        ],
    )
    revision: str = Field(
        description="The model branch to use",
        examples=["main", "gptq-4bit-64g-actorder_True"],
    )


class AppConfig(BaseConfig):
    backend_options: ConfigOptions
    download_options: Optional[DownloadOptions]
    CONFIG_SOURCES = [
        EnvSource(
            allow_all=True,
            prefix="LAI_",
            remap={
                "hf_hub_enable_hf_transfer": "download_options.hf_hub_enable_hf_transfer",
                "repo_id": "download_options.repo_id",
                "revision": "download_options.revision",
                "quantization": "backend_options.quantization",
            },
        )
    ]
