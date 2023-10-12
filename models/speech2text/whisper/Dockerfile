FROM cgr.dev/chainguard/python:latest-dev as builder

# Install project
COPY --chown=user:user requirements.txt .
RUN pip install -r requirements.txt --user

FROM cgr.dev/chainguard/python:latest

COPY --chown=user:user main.py .
# COPY --chown=user:user get_model.py .
COPY --chown=user:user .python-version .

COPY --chown=user:user pyproject.toml .
COPY --chown=user:user README.md .

# Enjoy
ENTRYPOINT ["python3", "main.py"]
