# ARG IMAGE_TAG
# FROM ghcr.io/defenseunicorns/leapfrogai/base:${IMAGE_TAG}

FROM cgr.dev/chainguard/python:3.10-dev as builder


WORKDIR /app

# Install project
COPY requirements.txt .
RUN pip install -r requirements.txt --user

COPY leapfrogai leapfrogai

RUN pip install leapfrogai --user

FROM cgr.dev/chainguard/python:3.10

WORKDIR /app

# Make sure you update Python version in path
COPY --from=builder /home/nonroot/.local/lib/python3.10/site-packages /home/nonroot/.local/lib/python3.10/site-packages

COPY main.py .

# Publish port
EXPOSE 50051:50051

ENV MODEL TheBloke/mpt-30B-chat-GGML

# Enjoy
ENTRYPOINT ["python", "/app/main.py"]
