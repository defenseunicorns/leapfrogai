import os

from huggingface_hub import hf_hub_download

REPO_ID = os.environ.get("REPO_ID", "TheBloke/SynthIA-7B-v2.0-GGUF")
FILENAME = os.environ.get("FILENAME", "synthia-7b-v2.0.Q4_K_M.gguf")
REVISION = os.environ.get("REVISION", "3f65d882253d1f15a113dabf473a7c02a004d2b5")

os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"

hf_hub_download(
    repo_id=REPO_ID,
    filename=FILENAME,
    local_dir=".model",
    local_dir_use_symlinks=False,
    revision=REVISION,
)
