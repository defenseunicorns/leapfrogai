ARG IMAGE_TAG
FROM ghcr.io/defenseunicorns/leapfrogai/base:${IMAGE_TAG}
# Install project
RUN curl -sSf https://rye-up.com/get | RYE_VERSION="0.4.0" RYE_INSTALL_OPTION="--yes" bash
COPY --chown=user:user requirements.txt .
RUN rye sync

COPY --chown=user:user main.py .
# COPY --chown=user:user get_model.py .
COPY --chown=user:user .python-version .

COPY --chown=user:user pyproject.toml .
COPY --chown=user:user README.md .

# Enjoy
ENTRYPOINT ["rye", "run", "python", "main.py"]
