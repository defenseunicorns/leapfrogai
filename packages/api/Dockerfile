ARG ARCH
FROM ghcr.io/defenseunicorns/leapfrogai/leapfrogai-sdk:latest as sdk

FROM ghcr.io/defenseunicorns/leapfrogai/python:3.11-dev-${ARCH} as builder
ARG SDK_DEST=src/leapfrogai_sdk/build
USER root
WORKDIR /leapfrogai

# copy the api dependencies over
# NOTE: We are copying to this filename because installing 'optional extras' from a wheel requires the absolute path to the wheel file (instead of a wildcard whl)
COPY --from=sdk /leapfrogai/${SDK_DEST} ${SDK_DEST}
COPY src/leapfrogai_api src/leapfrogai_api

RUN python -m venv .venv
ENV PATH="/leapfrogai/.venv/bin:$PATH"

RUN rm -f packages/api/build/*.whl
RUN python -m pip wheel src/leapfrogai_api -w packages/api/build --find-links=${SDK_DEST}
RUN pip install packages/api/build/leapfrogai_api*.whl --no-index --find-links=packages/api/build/

FROM ghcr.io/defenseunicorns/leapfrogai/python:3.11-${ARCH}
ENV PATH="/leapfrogai/.venv/bin:$PATH"
WORKDIR /leapfrogai

COPY --from=builder /leapfrogai/.venv/ /leapfrogai/.venv/

EXPOSE 8080

ENTRYPOINT ["uvicorn", "leapfrogai_api.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8080", "--log-level", "debug"]
