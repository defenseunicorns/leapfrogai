

# LeapfrogAI llama-cpp-python Backend

A LeapfrogAI API-compatible [instructor-xl](https://huggingface.co/hkunlp/instructor-xl) model for creating embeddings across CPU and GPU infrastructures.


# Usage

### Local Development

To run the text-embeddings backend locally (starting from the root directory of the repository):

```shell
# Setup Virtual Environment if you haven't done so already
python -m venv .venv
source .venv/bin/activate

# install dependencies
python -m pip install src/leapfrogai_sdk
cd packages/text-embeddings
python -m pip install .[dev]

# download the model
python scripts/model_download.py

# start the model backend
python -u main.py
```
