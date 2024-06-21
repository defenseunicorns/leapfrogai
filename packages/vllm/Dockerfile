FROM ghcr.io/defenseunicorns/leapfrogai/leapfrogai-sdk:latest as sdk

FROM nvidia/cuda:12.2.2-devel-ubuntu22.04 as builder
ARG SDK_DEST=src/leapfrogai_sdk/build

# Set the config file defaults
ARG PYTHON_VERSION=3.11.6
ARG HF_HUB_ENABLE_HF_TRANSFER="1"
ARG REPO_ID="TheBloke/Synthia-7B-v2.0-GPTQ"
ARG REVISION="gptq-4bit-32g-actorder_True"
ARG QUANTIZATION="gptq"
ARG MODEL_SOURCE=".model/"
ARG MAX_CONTEXT_LENGTH=32768
ARG STOP_TOKENS='["</s>","<|endoftext|>","<|im_end|>"]'
ARG PROMPT_FORMAT_CHAT_SYSTEM="SYSTEM: {}\n"
ARG PROMPT_FORMAT_CHAT_ASSISTANT="ASSISTANT: {}\n"
ARG PROMPT_FORMAT_CHAT_USER="USER: {}\n"
ARG PROMPT_FORMAT_DEFAULTS_TOP_P=1.0
ARG PROMPT_FORMAT_DEFAULTS_TOP_K=0
ARG TENSOR_PARALLEL_SIZE=1

ENV DEBIAN_FRONTEND=noninteractive

USER root

RUN groupadd -g 65532 vglusers && \
    useradd -ms /bin/bash nonroot -u 65532 -g 65532 && \
    usermod -a -G video,sudo nonroot

WORKDIR /home/leapfrogai

# grab necesary python dependencies
# TODO @JPERRY: Get context as to why we are doing this for this Dockerfile but not our other ones
RUN apt-get -y update \
    && apt-get install -y software-properties-common \
    && add-apt-repository universe \
    && add-apt-repository ppa:deadsnakes/ppa  \
    && apt-get -y update

# get deps for vllm compilation, model download, and pyenv
RUN apt-get -y install git python3-venv make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev tk-dev libffi-dev

COPY --from=sdk /leapfrogai/${SDK_DEST} ./${SDK_DEST}
COPY packages/vllm packages/vllm
RUN chown -R nonroot /home/leapfrogai/

USER nonroot

# # create virtual environment for light-weight portability and minimal libraries
RUN git clone --depth=1 https://github.com/pyenv/pyenv.git .pyenv
ENV PYENV_ROOT="/home/leapfrogai/.pyenv"
ENV PATH="$PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH"
RUN pyenv install ${PYTHON_VERSION}
RUN pyenv global ${PYTHON_VERSION}
RUN python3 -m venv .venv
ENV PATH="/home/leapfrogai/.venv/bin:$PATH"

RUN rm -f packages/vllm/build/*.whl
RUN python -m pip wheel packages/vllm -w packages/vllm/build --find-links=${SDK_DEST}
RUN pip install packages/vllm/build/lfai_vllm*.whl --no-index --find-links=packages/vllm/build/

FROM nvidia/cuda:12.2.2-runtime-ubuntu22.04
## COPIED FROM ABOVE ##
ARG SDK_DEST=src/leapfrogai_sdk/build
# Set the config file defaults
ARG PYTHON_VERSION=3.11.6
ARG HF_HUB_ENABLE_HF_TRANSFER="1"
ARG REPO_ID="TheBloke/Synthia-7B-v2.0-GPTQ"
ARG REVISION="gptq-4bit-32g-actorder_True"
ARG QUANTIZATION="gptq"
ARG MODEL_SOURCE=".model/"
ARG MAX_CONTEXT_LENGTH=32768
ARG STOP_TOKENS='["</s>","<|endoftext|>","<|im_end|>"]'
ARG PROMPT_FORMAT_CHAT_SYSTEM="SYSTEM: {}\n"
ARG PROMPT_FORMAT_CHAT_ASSISTANT="ASSISTANT: {}\n"
ARG PROMPT_FORMAT_CHAT_USER="USER: {}\n"
ARG PROMPT_FORMAT_DEFAULTS_TOP_P=1.0
ARG PROMPT_FORMAT_DEFAULTS_TOP_K=0
ARG TENSOR_PARALLEL_SIZE=1

ENV DEBIAN_FRONTEND=noninteractive

USER root

RUN groupadd -g 65532 vglusers && \
    useradd -ms /bin/bash nonroot -u 65532 -g 65532 && \
    usermod -a -G video,sudo nonroot

WORKDIR /home/leapfrogai

COPY --from=sdk /leapfrogai/${SDK_DEST} ./${SDK_DEST}
COPY --from=builder /home/leapfrogai/.venv /home/leapfrogai/.venv
COPY --from=builder /home/leapfrogai/packages/vllm/src /home/leapfrogai/packages/vllm/src
RUN chown -R nonroot /home/leapfrogai/

RUN apt-get -y update
RUN apt-get -y install git wget build-essential libssl-dev zlib1g-dev libffi-dev

USER nonroot

# # create virtual environment for light-weight portability and minimal libraries
RUN git clone --depth=1 https://github.com/pyenv/pyenv.git .pyenv
ENV PYENV_ROOT="/home/leapfrogai/.pyenv"
ENV PATH="$PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH"
RUN pyenv install ${PYTHON_VERSION}
ENV PATH="/home/leapfrogai/.venv/bin:$PATH"

# download model
ENV HF_HOME=/home/leapfrogai/.cache/huggingface

# Load ARG values into env variables for pickup by confz
ENV LAI_HF_HUB_ENABLE_HF_TRANSFER=${HF_HUB_ENABLE_HF_TRANSFER}
ENV LAI_REPO_ID=${REPO_ID}
ENV LAI_REVISION=${REVISION}
ENV LAI_QUANTIZATION=${QUANTIZATION}
ENV LAI_TENSOR_PARALLEL_SIZE=${TENSOR_PARALLEL_SIZE}
ENV LAI_MODEL_SOURCE=${MODEL_SOURCE}
ENV LAI_MAX_CONTEXT_LENGTH=${MAX_CONTEXT_LENGTH}
ENV LAI_STOP_TOKENS=${STOP_TOKENS}
ENV LAI_PROMPT_FORMAT_CHAT_SYSTEM=${PROMPT_FORMAT_CHAT_SYSTEM}
ENV LAI_PROMPT_FORMAT_CHAT_ASSISTANT=${PROMPT_FORMAT_CHAT_ASSISTANT}
ENV LAI_PROMPT_FORMAT_CHAT_USER=${PROMPT_FORMAT_CHAT_USER}
ENV LAI_PROMPT_FORMAT_DEFAULTS_TOP_P=${PROMPT_FORMAT_DEFAULTS_TOP_P}
ENV LAI_PROMPT_FORMAT_DEFAULTS_TOP_K=${PROMPT_FORMAT_DEFAULTS_TOP_K}

RUN pip install -U huggingface_hub[cli,hf_transfer]
RUN python3 packages/vllm/src/model_download.py

EXPOSE 50051:50051

ENTRYPOINT ["python", "-m", "leapfrogai_sdk.cli", "--app-dir=packages/vllm/src/", "main:Model"]