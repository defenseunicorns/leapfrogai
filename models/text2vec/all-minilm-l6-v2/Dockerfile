ARG IMAGE_TAG
FROM ghcr.io/defenseunicorns/leapfrogai/base:${IMAGE_TAG}
# Install project
COPY . .
RUN pip install  --no-cache-dir --user  -r requirements.txt


# Get model weights and tokenizer
RUN python3 get_models.py

# Publish port
EXPOSE 50051:50051

# Enjoy
ENTRYPOINT ["python3", "model.py"]
CMD ["--address", "0.0.0.0:50051"]
