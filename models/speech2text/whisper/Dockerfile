FROM python:3.11.6-bookworm

# Install project
COPY --chown=user:user requirements.txt .
RUN pip3 install -r requirements.txt

COPY --chown=user:user main.py .
COPY --chown=user:user .python-version .

COPY --chown=user:user pyproject.toml .
COPY --chown=user:user README.md .

# Enjoy
ENTRYPOINT ["python3", "main.py"]
