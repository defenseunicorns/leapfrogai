ARG LOCAL_VERSION
FROM ghcr.io/defenseunicorns/leapfrogai/leapfrogai-sdk:${LOCAL_VERSION} AS sdk

# hardened and slim python w/ developer tools image
FROM ghcr.io/defenseunicorns/leapfrogai/python:3.11-dev AS builder
ARG SDK_DEST=src/leapfrogai_sdk/build
USER root
WORKDIR /leapfrogai

# create virtual environment for light-weight portability and minimal libraries
RUN python3.11 -m venv .venv
ENV PATH="/leapfrogai/.venv/bin:$PATH"

# copy and install all python dependencies
# NOTE: We are copying the leapfrogai whl to this filename because installing 'optional extras' from
#       a wheel requires the absolute path to the wheel file (instead of a wildcard whl)
COPY --from=sdk /leapfrogai/${SDK_DEST} ${SDK_DEST}
COPY packages/text-embeddings packages/text-embeddings

RUN rm -f packages/text-embeddings/build/*.whl && \
    python -m pip wheel packages/text-embeddings -w packages/text-embeddings/build --find-links=${SDK_DEST} && \
    pip install packages/text-embeddings/build/lfai_text_embeddings*.whl --no-index --find-links=packages/text-embeddings/build/

# hardened and slim python image
FROM ghcr.io/defenseunicorns/leapfrogai/python:3.11

ENV PATH="/leapfrogai/.venv/bin:$PATH"

WORKDIR /leapfrogai

COPY --from=builder /leapfrogai/.venv/ /leapfrogai/.venv/

COPY packages/text-embeddings/main.py .

EXPOSE 50051

ENTRYPOINT ["python", "-u", "main.py"]
