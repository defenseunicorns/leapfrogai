FROM ghcr.io/defenseunicorns/leapfrogai/python:3.11-dev-amd64 as builder

WORKDIR /leapfrogai

# Install python requirements
COPY requirements.txt .

RUN pip install -r requirements.txt --user

# Use ffmpeg image to get compiled binaries
FROM cgr.dev/chainguard/ffmpeg:latest as ffmpeg

WORKDIR /leapfrogai

# Combine python libraries built in builder and ffmpeg binaries from ffmpeg into the final image
FROM ghcr.io/defenseunicorns/leapfrogai/python:3.11-amd64

WORKDIR /leapfrogai

COPY --from=ffmpeg /usr/bin/ffmpeg /usr/bin
COPY --from=ffmpeg /usr/bin/ffprobe /usr/bin
COPY --from=ffmpeg /usr/lib/lib* /usr/lib
COPY --from=builder /home/nonroot/.local/lib/python3.11/site-packages /home/nonroot/.local/lib/python3.11/site-packages

COPY main.py .
COPY .python-version .

COPY pyproject.toml .
COPY README.md .

# Publish port
EXPOSE 50052:50051

# Enjoy
ENTRYPOINT ["python3", "-u", "main.py"]