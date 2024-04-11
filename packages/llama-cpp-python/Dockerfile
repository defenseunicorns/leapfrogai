
# hardened and slim python w/ developer tools image
FROM --platform=$BUILDPLATFORM ghcr.io/defenseunicorns/leapfrogai/python:3.11-dev as builder

WORKDIR /leapfrogai

# download model
RUN python -m pip install -U huggingface_hub[cli,hf_transfer]
ARG REPO_ID=TheBloke/SynthIA-7B-v2.0-GGUF
ARG FILENAME=synthia-7b-v2.0.Q4_K_M.gguf
ARG REVISION=3f65d882253d1f15a113dabf473a7c02a004d2b5

# NOTE: This is checking for a pre-downloaded model file in the local build dir before downloading the model from HuggingFace
# TODO: Add checksum validation to verify the model in the local build-dir is the model we expect
COPY scripts/model_download.py scripts/model_download.py
COPY build/*.gguf .model/
RUN if [[ -f .model/model.gguf ]] ; then : ; else REPO_ID=${REPO_ID} FILENAME=${FILENAME} REVISION=${REVISION} python3.11 scripts/model_download.py ; fi
RUN if [[ -f .model/model.gguf ]] ; then : ; else mv .model/*.gguf .model/model.gguf ; fi


# create virtual environment for light-weight portability and minimal libraries
RUN python3.11 -m venv .venv
ENV PATH="/leapfrogai/.venv/bin:$PATH"

# copy the llama-cpp-python build dependencies over
# NOTE: We are copying to this filename because installing 'optional extras' from a wheel requires the absolute path to the wheel file (instead of a wildcard whl)
COPY build/*.whl build/
COPY build/leapfrogai_api*.whl leapfrogai_api-100.100.100-py3-none-any.whl
RUN pip install leapfrogai_api-100.100.100-py3-none-any.whl[llama-cpp-python] --no-index --find-links=build/

# hardened and slim python image
FROM --platform=$BUILDPLATFORM ghcr.io/defenseunicorns/leapfrogai/python:3.11

ENV PATH="/leapfrogai/.venv/bin:$PATH"

WORKDIR /leapfrogai

COPY --from=builder /leapfrogai/.venv/ /leapfrogai/.venv/
COPY --from=builder /leapfrogai/.model/ /leapfrogai/.model/

COPY main.py .
COPY config.yaml .

EXPOSE 50051:50051

ENTRYPOINT ["python", "-m", "leapfrogai_api.types.cli", "--app-dir=.", "main:Model"]
