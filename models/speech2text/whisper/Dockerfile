# Using this instead of chainguard due to whisper having a dependency on an incompatible Python version
FROM python:3.11.6-bookworm

RUN apt-get -y update
RUN apt-get install -y ffmpeg

# Install project
COPY --chown=user:user requirements.txt .
RUN pip3 install -r requirements.txt

COPY --chown=user:user main.py .
COPY --chown=user:user .python-version .

COPY --chown=user:user pyproject.toml .
COPY --chown=user:user README.md .

# Enjoy
ENTRYPOINT ["python3", "-u", "main.py"]
