FROM ghcr.io/defenseunicorns/leapfrogai/base:0.0.4

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY repeater.py .

# Publish port
EXPOSE 50051:50051

# Enjoy
ENTRYPOINT ["python3", "repeater.py"]
