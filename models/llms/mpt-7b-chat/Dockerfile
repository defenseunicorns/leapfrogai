ARG IMAGE_TAG
FROM ghcr.io/defenseunicorns/leapfrogai/base:${IMAGE_TAG}


# Install requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY get_model.py get_model.py
# # Get model weights and tokenizer
# RUN python3 get_model.py
COPY --chown=user:user mpt-7b-chat-offline mpt-7b-chat-offline

# Move the rest of the python files (most likely place layer cache will be invalidated)
COPY --chown=user:user *.py .

# Publish port
EXPOSE 50051:50051

# Enjoy
ENTRYPOINT ["python3", "model.py"]