ARG IMAGE_TAG
FROM ghcr.io/defenseunicorns/leapfrogai/base:${IMAGE_TAG}

# Install project
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY main.py .

# Publish port
EXPOSE 50051:50051

# Enjoy
ENTRYPOINT ["python3", "main.py"]
