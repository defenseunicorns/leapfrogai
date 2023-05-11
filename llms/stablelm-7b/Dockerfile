FROM nvidia/cuda:11.7.1-devel-ubuntu22.04

# Update, install
RUN apt update && \
    apt install -y build-essential python3 python3-pip git

# Create user instead of using root
ENV USER='user'
RUN groupadd -r user && useradd -r -g $USER $USER


RUN mkdir -p /home/$USER

RUN chown -R $USER /home/$USER
RUN chmod a+rwx -R  /home/$USER
USER $USER


RUN pip install --upgrade pip setuptools wheel


# Define workdir
WORKDIR /home/$USER/app


# Install project
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY get_models.py get_models.py
# # Get model weights and tokenizer
RUN python3 get_models.py

COPY *.py .

# Publish port
EXPOSE 50051:50051

ENV PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:1024

# Enjoy
ENTRYPOINT ["python3", "server.py"]
CMD ["--address", "0.0.0.0:50051"]
