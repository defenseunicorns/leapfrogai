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

# Move model files
COPY --chown=user:user mpt-7b-chat-offline ./mpt-7b-chat-offline

# Move the rest of the python files (most likely place layer cache will be invalidated)
COPY --chown=user:user *.py .

# install locally built leapfrog-0.3.0
COPY --chown=user:user leapfrogai-0.3.0-py3-none-any.whl .
RUN pip install leapfrogai-0.3.0-py3-none-any.whl
RUN rm leapfrogai-0.3.0-py3-none-any.whl

RUN ls -lah mpt-7b-chat-offline

# Publish port
EXPOSE 50051:50051

# Enjoy
ENTRYPOINT ["python3", "model.py"]