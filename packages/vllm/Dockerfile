ARG LOCAL_VERSION
FROM ghcr.io/defenseunicorns/leapfrogai/leapfrogai-sdk:${LOCAL_VERSION} AS sdk

FROM nvidia/cuda:12.2.2-devel-ubuntu22.04 AS builder

# set SDK location
# set the pyenv and Python versions
ARG SDK_DEST=src/leapfrogai_sdk/build \
    PYTHON_VERSION=3.11.9 \
    PYENV_GIT_TAG=v2.4.8

# use root user for deps installation and nonroot user creation
USER root
# get deps for vllm compilation, pyenv, python and model downloading
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
    libffi-dev \
    liblzma-dev

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
RUN curl https://pyenv.run | bash && \
    echo "export PYENV_ROOT='$HOME/.pyenv'" >> ~/.bashrc && \
    echo "export PATH='$PYENV_ROOT/bin:$PATH'" >> ~/.bashrc && \
    echo "eval '$(pyenv init -)'" >> ~/.bashrc && \
    echo "eval '$(pyenv virtualenv-init -)'" >> ~/.bashrc

# Set environment variables
ENV PYENV_ROOT="/home/nonroot/.pyenv" \
    PATH="/home/nonroot/.pyenv/bin:$PATH"

# Install Python, set it as global, and create a venv
RUN . ~/.bashrc && \
    PYTHON_CONFIGURE_OPTS="--enable-shared" pyenv install ${PYTHON_VERSION} && \
    pyenv global ${PYTHON_VERSION} && \
    pyenv exec python -m venv .venv

# set path to venv python
ENV PATH="/home/leapfrogai/.venv/bin:$PATH"

RUN rm -f packages/vllm/build/*.whl && \
    python -m pip wheel packages/vllm -w packages/vllm/build --find-links=${SDK_DEST} && \
    pip install packages/vllm/build/lfai_vllm*.whl --no-index --find-links=packages/vllm/build/

FROM nvidia/cuda:12.2.2-runtime-ubuntu22.04

# set SDK location
ARG SDK_DEST=src/leapfrogai_sdk/build

# model-specific arguments
ARG ARG HF_HUB_ENABLE_HF_TRANSFER="1" \
    REPO_ID="TheBloke/Synthia-7B-v2.0-GPTQ" \
    REVISION="gptq-4bit-32g-actorder_True" \
    MODEL_SOURCE="/data/.model/" \
    MAX_CONTEXT_LENGTH=32768 \
    STOP_TOKENS='["</s>"]' \
    PROMPT_FORMAT_CHAT_SYSTEM="SYSTEM: {}\n" \
    PROMPT_FORMAT_CHAT_USER="USER: {}\n" \
    PROMPT_FORMAT_CHAT_ASSISTANT="ASSISTANT: {}\n" \
    PROMPT_FORMAT_DEFAULTS_TOP_P=1.0 \
    PROMPT_FORMAT_DEFAULTS_TOP_K=0 \
    TENSOR_PARALLEL_SIZE=1 \
    QUANTIZATION="gptq"

# setup nonroot user and permissions
USER root
RUN groupadd -g 65532 vglusers && \
    useradd -ms /bin/bash nonroot -u 65532 -g 65532 && \
    usermod -a -G video,sudo nonroot
USER nonroot

WORKDIR /home/leapfrogai

# copy-in SDK from sdk stagem model and vllm source code from builder
COPY --from=sdk --chown=nonroot:nonroot /leapfrogai/${SDK_DEST} ./${SDK_DEST}
COPY --from=builder --chown=nonroot:nonroot /home/leapfrogai/.venv /home/leapfrogai/.venv
COPY --from=builder --chown=nonroot:nonroot /home/leapfrogai/packages/vllm/src /home/leapfrogai/packages/vllm/src
# copy-in python binaries
COPY --from=builder --chown=nonroot:nonroot /home/nonroot/.pyenv/versions/${PYTHON_VERSION}/ /home/nonroot/.pyenv/versions/${PYTHON_VERSION}/

# load ARG values into env variables for pickup by confz
ENV LAI_HF_HUB_ENABLE_HF_TRANSFER=${HF_HUB_ENABLE_HF_TRANSFER} \
    LAI_REPO_ID=${REPO_ID} \
    LAI_REVISION=${REVISION} \
    LAI_MODEL_SOURCE=${MODEL_SOURCE} \
    LAI_MAX_CONTEXT_LENGTH=${MAX_CONTEXT_LENGTH} \
    LAI_STOP_TOKENS=${STOP_TOKENS} \
    LAI_PROMPT_FORMAT_CHAT_SYSTEM=${PROMPT_FORMAT_CHAT_SYSTEM} \
    LAI_PROMPT_FORMAT_CHAT_USER=${PROMPT_FORMAT_CHAT_USER} \
    LAI_PROMPT_FORMAT_CHAT_ASSISTANT=${PROMPT_FORMAT_CHAT_ASSISTANT} \
    LAI_PROMPT_FORMAT_DEFAULTS_TOP_P=${PROMPT_FORMAT_DEFAULTS_TOP_P} \
    LAI_PROMPT_FORMAT_DEFAULTS_TOP_K=${PROMPT_FORMAT_DEFAULTS_TOP_K} \
    LAI_TENSOR_PARALLEL_SIZE=${TENSOR_PARALLEL_SIZE} \
    LAI_QUANTIZATION=${QUANTIZATION} \
    # remove vLLM callback to stats server
    VLLM_NO_USAGE_STATS=1

ENV PATH="/home/leapfrogai/.venv/bin:$PATH"

EXPOSE 50051

ENTRYPOINT ["python", "-m", "leapfrogai_sdk.cli", "--app-dir=packages/vllm/src/", "main:Model"]
