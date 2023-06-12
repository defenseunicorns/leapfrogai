# Base image
FROM nvidia/cuda:11.7.1-devel-ubuntu22.04

# Environment variables
ENV USER='pyuser' \
    WORKPATH=/home/${USER} \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_ROOT_USER_ACTION=ignore \
    POETRY_HOME="/opt/poetry" \
    POETRY_VERSION=1.5.1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:1024

# Set work directory
WORKDIR ${WORKPATH}

# Update the base ubuntu image with dependencies needed for poetry
RUN apt-get update && apt-get install -y \
    curl \
    python3-pip \
    python3-venv

# Install poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Create a non-root user and switch to it
RUN useradd -m ${USER}

# Copy pyproject.toml and poetry.lock file into the working directory
COPY --chown=${USER}:${USER} pyproject.toml poetry.lock ${WORKPATH}/

# Install the dependencies
RUN $POETRY_HOME/bin/poetry install

# Copy the rest of your application code into the working directory
COPY --chown=${USER}:${USER} . ${WORKPATH}/

# Get model weights and tokenizer
RUN python3 get_models.py

# Publish port
EXPOSE 50051

# Run the server
ENTRYPOINT ["python3", "server.py"]
CMD ["--address", "0.0.0.0:50051"]
