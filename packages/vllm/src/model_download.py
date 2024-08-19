import os
from huggingface_hub import snapshot_download
from config import DownloadConfig

REPO_ID = DownloadConfig().download_options.repo_id
REVISION = DownloadConfig().download_options.revision

# enable hf_transfer to max-out model download bandwidth
os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"

print(f"Downloading model from {REPO_ID} at revision {REVISION}...")

snapshot_download(
    repo_id=REPO_ID,
    local_dir=".model",
    revision=REVISION,
)
