FROM ghcr.io/defenseunicorns/leapfrogai/python:3.11-dev AS builder

ARG SDK_DEST=src/leapfrogai_sdk/build

USER root

WORKDIR /leapfrogai

COPY ./src/leapfrogai_sdk /leapfrogai/src/leapfrogai_sdk

RUN python -m venv .venv
ENV PATH="/leapfrogai/.venv/bin:$PATH"

RUN rm -f ${SDK_DEST}/*.whl && \
    python -m pip wheel src/leapfrogai_sdk -w ${SDK_DEST}
