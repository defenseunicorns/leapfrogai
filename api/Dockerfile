FROM python:3.10

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install peft

ADD models.toml .

ADD simple_ai ./simple_ai

EXPOSE 8080

# Set the command to run the application
ENTRYPOINT [ "python" ]
CMD [ "-m", "simple_ai", "serve",  "--host", "0.0.0.0" ]


