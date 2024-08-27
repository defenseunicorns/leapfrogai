import os
import hashlib
import urllib.request

REPO_ID = os.environ.get("REPO_ID", "")
FILENAME = os.environ.get("FILENAME", "")
REVISION = os.environ.get("REVISION", "main")
CHECKSUM = os.environ.get("SHA256_CHECKSUM", "")
OUTPUT_FILE = os.environ.get("OUTPUT_FILE", ".model/model.gguf")


def download_model():
    # Check if the model is already downloaded.
    if os.path.exists(OUTPUT_FILE) and CHECKSUM != "":
        if hashlib.sha256(open(OUTPUT_FILE, "rb").read()).hexdigest() == CHECKSUM:
            print("Model already downloaded.")
            return

    # Validate that require environment variables are provided
    if REPO_ID == "" or FILENAME == "":
        print("Please provide REPO_ID and FILENAME environment variables.")
        return

    # Download the model!
    print("Downloading model... This may take a while.")
    if not os.path.exists(".model"):
        os.mkdir(".model")
    urllib.request.urlretrieve(
        f"https://huggingface.co/{REPO_ID}/resolve/{REVISION}/{FILENAME}", OUTPUT_FILE
    )


if __name__ == "__main__":
    download_model()
