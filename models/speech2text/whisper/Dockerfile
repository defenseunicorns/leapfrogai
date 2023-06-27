ARG IMAGE_TAG
FROM ghcr.io/defenseunicorns/leapfrogai/base:${IMAGE_TAG}
# Install project

COPY --chown=user:user main.py .
COPY --chown=user:user get_model.py .
COPY --chown=user:user .python-version .
COPY --chown=user:user requirements.lock .
COPY --chown=user:user pyproject.toml .
COPY --chown=user:user README.md .
RUN /home/$USER/.rye/shims/rye sync --no-dev --no-lock
RUN /home/$USER/.rye/shims/rye run python get_model.py

# Publish port
ENV UVICORN_HOST=0.0.0.0
ENV UVICORN_PORT=8000
EXPOSE 8000:8000

# Enjoy
ENTRYPOINT ["/home/user/.rye/shims/rye", "run"]
CMD ["uvicorn", "main:app"]
