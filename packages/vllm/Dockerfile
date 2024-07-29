ARG LOCAL_VERSION
FROM ghcr.io/defenseunicorns/leapfrogai/leapfrogai-sdk:${LOCAL_VERSION} AS sdk

FROM nvidia/cuda:12.2.2-devel-ubuntu22.04 AS builder

# set SDK location and Python version
ARG SDK_DEST=src/leapfrogai_sdk/build \
    PYTHON_VERSION=3.11.6

# use root user for deps installation and nonroot user creation
USER root
# get deps for vllm compilation, model download, and pyenv + python
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get -y install \
    git \
    make \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    wget \
    curl \
    llvm \
    libncurses5-dev \
    libncursesw5-dev \
    tk-dev \
    libffi-dev

# setup nonroot user and permissions
RUN groupadd -g 65532 vglusers && \
    useradd -ms /bin/bash nonroot -u 65532 -g 65532 && \
    usermod -a -G video,sudo nonroot
USER nonroot

# copy-in SDK from sdk stage and vllm source code from host
WORKDIR /home/leapfrogai
COPY --from=sdk --chown=nonroot:nonroot /leapfrogai/${SDK_DEST} ./${SDK_DEST}
COPY --chown=nonroot:nonroot packages/vllm packages/vllm

# create virtual environment for light-weight portability and minimal libraries
ENV PYENV_GIT_TAG=v2.4.8
RUN curl https://pyenv.run | bash

ENV PYENV_ROOT="$HOME/.pyenv" \
    PATH="$PYENV_ROOT/bin:$PATH"
RUN pyenv install ${PYTHON_VERSION} && \
    pyenv global ${PYTHON_VERSION} && \
    python3 -m venv .venv

# set path to venv python
ENV PATH="/home/leapfrogai/.venv/bin:$PATH"

RUN rm -f packages/vllm/build/*.whl && \
    python -m pip wheel packages/vllm -w packages/vllm/build --find-links=${SDK_DEST} && \
    pip install packages/vllm/build/lfai_vllm*.whl --no-index --find-links=packages/vllm/build/

# Model download arguments
ARG HF_HUB_ENABLE_HF_TRANSFER="1" \
    REPO_ID="TheBloke/Synthia-7B-v2.0-GPTQ" \
    REVISION="gptq-4bit-32g-actorder_True"

RUN pip install -U huggingface_hub[cli,hf_transfer] && \
    python3 packages/vllm/src/model_download.py

#################
# FINAL CONTAINER
#################

FROM nvidia/cuda:12.2.2-runtime-ubuntu22.04

# set SDK location
ARG SDK_DEST=src/leapfrogai_sdk/build

# Model-specific arguments
ARG TRUST_REMOTE_CODE="True" \
    MODEL_SOURCE=".model/" \
    MAX_CONTEXT_LENGTH=32768 \
    STOP_TOKENS='["</s>"]' \
    PROMPT_FORMAT_CHAT_SYSTEM="SYSTEM: {}\n" \
    PROMPT_FORMAT_CHAT_ASSISTANT="ASSISTANT: {}\n" \
    PROMPT_FORMAT_CHAT_USER="USER: {}\n" \
    PROMPT_FORMAT_DEFAULTS_TOP_P=1.0 \
    PROMPT_FORMAT_DEFAULTS_TOP_K=0 \
    TENSOR_PARALLEL_SIZE=1

# setup nonroot user and permissions
USER root
RUN groupadd -g 65532 vglusers && \
    useradd -ms /bin/bash nonroot -u 65532 -g 65532 && \
    usermod -a -G video,sudo nonroot
USER nonroot

WORKDIR /home/leapfrogai

COPY --from=sdk --chown=nonroot:nonroot /leapfrogai/${SDK_DEST} ./${SDK_DEST}
COPY --from=builder --chown=nonroot:nonroot /home/leapfrogai/.venv /home/leapfrogai/.venv
COPY --from=builder --chown=nonroot:nonroot /home/leapfrogai/packages/vllm/src /home/leapfrogai/packages/vllm/src
COPY --from=builder --chown=nonroot:nonroot /home/leapfrogai/.model /home/leapfrogai/.model

# activate python virtual environment
ENV PATH="/home/leapfrogai/.venv/bin:$PATH"

# Load ARG values into env variables for pickup by confz
ENV LAI_HF_HUB_ENABLE_HF_TRANSFER=${HF_HUB_ENABLE_HF_TRANSFER} \
    LAI_REPO_ID=${REPO_ID} \
    LAI_REVISION=${REVISION} \
    LAI_TRUST_REMOTE_CODE=${TRUST_REMOTE_CODE} \
    LAI_TENSOR_PARALLEL_SIZE=${TENSOR_PARALLEL_SIZE} \
    LAI_MODEL_SOURCE=${MODEL_SOURCE} \
    LAI_MAX_CONTEXT_LENGTH=${MAX_CONTEXT_LENGTH} \
    LAI_STOP_TOKENS=${STOP_TOKENS} \
    LAI_PROMPT_FORMAT_CHAT_SYSTEM=${PROMPT_FORMAT_CHAT_SYSTEM} \
    LAI_PROMPT_FORMAT_CHAT_ASSISTANT=${PROMPT_FORMAT_CHAT_ASSISTANT} \
    LAI_PROMPT_FORMAT_CHAT_USER=${PROMPT_FORMAT_CHAT_USER} \
    LAI_PROMPT_FORMAT_DEFAULTS_TOP_P=${PROMPT_FORMAT_DEFAULTS_TOP_P} \
    LAI_PROMPT_FORMAT_DEFAULTS_TOP_K=${PROMPT_FORMAT_DEFAULTS_TOP_K}

EXPOSE 50051:50051

ENTRYPOINT ["python", "-m", "leapfrogai_sdk.cli", "--app-dir=packages/vllm/src/", "main:Model"]
