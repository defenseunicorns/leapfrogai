FROM cgr.dev/chainguard/python:latest-dev as builder

WORKDIR /whisper

# Install project
COPY --chown=user:user requirements.txt .
COPY . .
RUN pip install -r requirements.txt --user

FROM cgr.dev/chainguard/python:latest

WORKDIR /whisper

COPY --from=builder /home/nonroot/.local/lib/python3.11/site-packages /home/nonroot/.local/lib/python3.11/site-packages

COPY --chown=user:user main.py .
COPY --chown=user:user .python-version .

COPY --chown=user:user pyproject.toml .
COPY --chown=user:user README.md .

# Enjoy
ENTRYPOINT ["python3", "main.py"]
