from huggingface_hub import snapshot_download
import os

REPO_ID = os.environ.get("REPO_ID", "TheBloke/Synthia-7B-v2.0-AWQ")
REVISION = os.environ.get("REVISION", "main")

os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"

snapshot_download(
    repo_id=REPO_ID,
    local_dir=".model",
    local_dir_use_symlinks=False,
    revision=REVISION,
)