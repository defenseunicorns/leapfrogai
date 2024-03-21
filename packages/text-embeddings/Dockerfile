ARG ARCH=amd64

# hardened and slim python w/ developer tools image
FROM ghcr.io/defenseunicorns/leapfrogai/python:3.11-dev-${ARCH} as builder

WORKDIR /leapfrogai

# create virtual environment for light-weight portability and minimal libraries
RUN python3.11 -m venv .venv
ENV PATH="/leapfrogai/.venv/bin:$PATH"

# copy and install all python dependencies
# NOTE: We are copying the leapfrog whl to this filename because installing 'optional extras' from 
#       a wheel requires the absolute path to the wheel file (instead of a wildcard whl)
COPY build/*.whl build/
COPY build/*.tar.gz build/
COPY build/leapfrogai_api*.whl leapfrogai_api-100.100.100-py3-none-any.whl
RUN pip install build/*.tar.gz --no-deps
RUN pip install "leapfrogai_api-100.100.100-py3-none-any.whl[text-embeddings]" --no-index --find-links=build/


# download model
RUN python -m pip install -U huggingface_hub[cli,hf_transfer]
ARG REPO_ID="hkunlp/instructor-xl"
ARG REVISION="ce48b213095e647a6c3536364b9fa00daf57f436"
COPY scripts/model_download.py scripts/model_download.py
RUN REPO_ID=${REPO_ID} REVISION=${REVISION} python scripts/model_download.py

# hardened and slim python image
FROM ghcr.io/defenseunicorns/leapfrogai/python:3.11-${ARCH}

ENV PATH="/leapfrogai/.venv/bin:$PATH"

WORKDIR /leapfrogai

COPY --from=builder /leapfrogai/.venv/ /leapfrogai/.venv/
COPY --from=builder /leapfrogai/.model/ /leapfrogai/.model/

COPY main.py .

EXPOSE 50051:50051

ENTRYPOINT ["python", "-u", "main.py"]
