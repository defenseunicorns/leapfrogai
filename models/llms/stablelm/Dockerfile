ARG IMAGE_TAG
FROM ghcr.io/defenseunicorns/leapfrogai/base:${IMAGE_TAG}

# Install project
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY get_models.py get_models.py
# # Get model weights and tokenizer
RUN python3 get_models.py

COPY *.py ./

# Publish port
EXPOSE 50051:50051

# Enjoy
ENTRYPOINT ["python3", "stablelm.py"]
