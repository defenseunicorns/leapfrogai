ARG ARCH=amd64

FROM ghcr.io/defenseunicorns/leapfrogai/python:3.11-dev-${ARCH} as builder

WORKDIR /leapfrogai

# copy the api dependencies over
# NOTE: We are copying to this filename because installing 'optional extras' from a wheel requires the absolute path to the wheel file (instead of a wildcard whl)
COPY build/*.whl build/
COPY build/leapfrogai_api*.whl .
RUN pip install leapfrogai_api*.whl --no-index --find-links=build/

FROM ghcr.io/defenseunicorns/leapfrogai/python:3.11-${ARCH}

WORKDIR /leapfrogai

COPY --from=builder /home/nonroot/.local/lib/python3.11/site-packages /home/nonroot/.local/lib/python3.11/site-packages
COPY --from=builder /home/nonroot/.local/bin/uvicorn /home/nonroot/.local/bin/uvicorn



EXPOSE 8080

ENTRYPOINT ["/home/nonroot/.local/bin/uvicorn", "leapfrogai_api.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8080", "--log-level", "debug"]
