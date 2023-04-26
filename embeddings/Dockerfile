FROM nvidia/cuda:11.7.1-devel-ubuntu22.04

# Update, install
RUN apt update && \
    apt install -y build-essential python3 python3-pip git

# Create user instead of using root
ENV USER='user'
RUN groupadd -r user && useradd -m -r -g $USER $USER


RUN mkdir -p /home/$USER

RUN chown $USER:$USER /home/$USER
RUN chmod 700 /home/$USER


USER root
RUN pip install --no-cache-dir --user --upgrade pip setuptools wheel
USER $USER



# Define workdir
WORKDIR /home/$USER/app


# Install project
COPY . .
RUN pip install  --no-cache-dir --user  -r requirements.txt


# Get model weights and tokenizer
RUN python3 get_models.py

# Publish port
EXPOSE 50051:50051

# Enjoy
ENTRYPOINT ["python3", "server.py"]
CMD ["--address", "0.0.0.0:50051"]
