ARG ARCH=amd64

# hardened and slim python w/ developer tools image
FROM ghcr.io/defenseunicorns/leapfrogai/python:3.11-dev-${ARCH} as builder

WORKDIR /leapfrogai

# create virtual environment for light-weight portability and minimal libraries
RUN python3.11 -m venv .venv
ENV PATH="/leapfrogai/.venv/bin:$PATH"

# copy and install all python dependencies
COPY build/*.whl build/
COPY build/lfai_repeater*.whl .
RUN pip install lfai_repeater*.whl --no-index --find-links=build/

# hardened and slim python image
FROM ghcr.io/defenseunicorns/leapfrogai/python:3.11-${ARCH}

ENV PATH="/leapfrogai/.venv/bin:$PATH"

WORKDIR /leapfrogai

COPY --from=builder /leapfrogai/.venv/ /leapfrogai/.venv/

COPY repeater.py .

# Publish port
EXPOSE 50051:50051

# Run the repeater model
ENTRYPOINT ["python", "-u", "repeater.py"]
