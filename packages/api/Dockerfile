ARG ARCH=amd64
ARG SDK_SRC=src/leapfrogai_sdk

FROM ghcr.io/defenseunicorns/leapfrogai/python:3.11-dev-${ARCH} as builder

WORKDIR /leapfrogai

# copy source
USER root
COPY src ./src
RUN chown -R nonroot:nonroot ./src
USER nonroot

# build sdk
RUN python -m pip wheel ./src/leapfrogai_sdk -w build

# build api
RUN python -m pip wheel ./src/leapfrogai_api -w build --find-links=build/

# install
RUN pip install build/leapfrogai_api-*.whl --no-index --find-links=build/

FROM ghcr.io/defenseunicorns/leapfrogai/python:3.11-${ARCH}

WORKDIR /leapfrogai

COPY --from=builder /home/nonroot/.local/lib/python3.11/site-packages /home/nonroot/.local/lib/python3.11/site-packages
COPY --from=builder /home/nonroot/.local/bin/uvicorn /home/nonroot/.local/bin/uvicorn



EXPOSE 8080

ENTRYPOINT ["/home/nonroot/.local/bin/uvicorn", "leapfrogai_api.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8080"]
