import os

from huggingface_hub import snapshot_download

REPO_ID = os.environ.get("REPO_ID", "hkunlp/instructor-xl")
REVISION = os.environ.get("REVISION", "ce48b213095e647a6c3536364b9fa00daf57f436")

os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"

snapshot_download(
    repo_id=REPO_ID,
    local_dir=".model",
    local_dir_use_symlinks=False,
    revision=REVISION,
)
