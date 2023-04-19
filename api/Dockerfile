FROM python:3.11

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install simple_ai_server peft


# Set the command to run the application
CMD [ "simple_ai serve" ]


