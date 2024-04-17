ARG IMAGE_TAG
FROM ghcr.io/defenseunicorns/leapfrogai/base:${IMAGE_TAG}

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY repeater.py .

# Publish port
EXPOSE 50051:50051

# Enjoy
ENTRYPOINT ["python3", "repeater.py"]
