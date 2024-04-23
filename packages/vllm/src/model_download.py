import os
from huggingface_hub import snapshot_download
from config import AppConfig

REPO_ID = AppConfig().download_options.repo_id
REVISION = AppConfig().download_options.revision
os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = (
    AppConfig().download_options.hf_hub_enable_hf_transfer
)

print(f"Downloading model from {REPO_ID} at revision {REVISION}...")

snapshot_download(
    repo_id=REPO_ID,
    local_dir=".model",
    local_dir_use_symlinks=False,
    revision=REVISION,
)
