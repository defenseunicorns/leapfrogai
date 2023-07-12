ARG IMAGE_TAG
FROM ghcr.io/defenseunicorns/leapfrogai/base:${IMAGE_TAG}
# Install project
# RUN curl -sSf https://rye-up.com/get | bash
COPY --chown=user:user requirements.txt .
RUN pip install -r requirements.txt

COPY --chown=user:user main.py .
COPY --chown=user:user get_model.py .
COPY --chown=user:user .python-version .

COPY --chown=user:user pyproject.toml .
COPY --chown=user:user README.md .

# Enjoy
ENTRYPOINT ["python3", "main.py"]
