FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-devel

# Create user instead of using root
ENV USER='user'
RUN groupadd -r user && useradd -r -g $USER $USER
RUN mkdir -p /home/$USER
RUN chown -R $USER /home/$USER
RUN chmod a+rwx -R  /home/$USER
USER $USER

# Define workdir
RUN mkdir /home/$USER/app
WORKDIR /home/$USER/app

# Install requirements
COPY --chown=user:user requirements.txt .
RUN pip install -r requirements.txt

# Get model weights and tokenizer
COPY --chown=user:user get_model.py .
RUN python3 get_model.py

# Move the model runner (most likely to change, so add last to avoid layer cache invalidations)
COPY --chown=user:user model.py .

# Publish port
EXPOSE 50051:50051

# Enjoy
ENTRYPOINT ["python3", "model.py"]
CMD ["--address", "0.0.0.0:50051"]
