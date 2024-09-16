ARG LOCAL_VERSION
FROM ghcr.io/defenseunicorns/leapfrogai/leapfrogai-sdk:${LOCAL_VERSION} AS sdk

# hardened and slim python w/ developer tools image
FROM ghcr.io/defenseunicorns/leapfrogai/python:3.11-dev AS builder

ARG SDK_DEST=src/leapfrogai_sdk/build

USER root

WORKDIR /leapfrogai

COPY --from=sdk /leapfrogai/${SDK_DEST} ${SDK_DEST}
COPY packages/repeater packages/repeater

# create virtual environment for light-weight portability and minimal libraries
RUN python -m venv .venv
ENV PATH="/leapfrogai/.venv/bin:$PATH"

RUN rm -f packages/repeater/build/*.whl && \
    python -m pip wheel packages/repeater -w packages/repeater/build --find-links=${SDK_DEST} && \
    pip install packages/repeater/build/lfai_repeater*.whl --no-index --find-links=packages/repeater/build/

# hardened and slim python image
FROM ghcr.io/defenseunicorns/leapfrogai/python:3.11

ENV PATH="/leapfrogai/.venv/bin:$PATH"

WORKDIR /leapfrogai

COPY --from=builder /leapfrogai/.venv/ /leapfrogai/.venv/
COPY packages/repeater/main.py .
COPY packages/repeater/config.yaml .

# Publish port
EXPOSE 50051

# Run the repeater model
ENTRYPOINT ["python", "-m", "leapfrogai_sdk.cli", "--app-dir=.", "main:Model"]
