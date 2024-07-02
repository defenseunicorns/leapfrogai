ARG ARCH
ARG LOCAL_VERSION
FROM ghcr.io/defenseunicorns/leapfrogai/leapfrogai-sdk:${LOCAL_VERSION} as sdk

# hardened and slim python w/ developer tools image
FROM --platform=$BUILDPLATFORM ghcr.io/defenseunicorns/leapfrogai/python:3.11-dev as builder
ARG SDK_DEST=src/leapfrogai_sdk/build
USER root
WORKDIR /leapfrogai

# download model
RUN python -m pip install -U huggingface_hub[cli,hf_transfer]
ARG REPO_ID=TheBloke/SynthIA-7B-v2.0-GGUF
ARG FILENAME=synthia-7b-v2.0.Q4_K_M.gguf
ARG REVISION=3f65d882253d1f15a113dabf473a7c02a004d2b5

# NOTE: This is checking for a pre-downloaded model file in the local build dir before downloading the model from HuggingFace
# TODO: Add checksum validation to verify the model in the local build-dir is the model we expect
COPY packages/llama-cpp-python/scripts/model_download.py scripts/model_download.py
RUN REPO_ID=${REPO_ID} FILENAME=${FILENAME} REVISION=${REVISION} python3.11 scripts/model_download.py
RUN mv .model/*.gguf .model/model.gguf


# create virtual environment for light-weight portability and minimal libraries
RUN python3.11 -m venv .venv
ENV PATH="/leapfrogai/.venv/bin:$PATH"

# copy the llama-cpp-python build dependencies over
# NOTE: We are copying to this filename because installing 'optional extras' from a wheel requires the absolute path to the wheel file (instead of a wildcard whl)
COPY --from=sdk /leapfrogai/${SDK_DEST} ${SDK_DEST}
COPY packages/llama-cpp-python packages/llama-cpp-python

RUN rm -f packages/llama-cpp-python/build/*.whl
RUN python -m pip wheel packages/llama-cpp-python -w packages/llama-cpp-python/build --find-links=${SDK_DEST}

RUN pip install packages/llama-cpp-python/build/lfai_llama_cpp_python*.whl --no-index --find-links=packages/llama-cpp-python/build/

# hardened and slim python image
FROM --platform=$BUILDPLATFORM ghcr.io/defenseunicorns/leapfrogai/python:3.11

ENV PATH="/leapfrogai/.venv/bin:$PATH"

WORKDIR /leapfrogai

COPY --from=builder /leapfrogai/.venv/ /leapfrogai/.venv/
COPY --from=builder /leapfrogai/.model/ /leapfrogai/.model/

COPY packages/llama-cpp-python/main.py .
COPY packages/llama-cpp-python/config.yaml .

EXPOSE 50051:50051

ENTRYPOINT ["python", "-m", "leapfrogai_sdk.cli", "--app-dir=.", "main:Model"]
