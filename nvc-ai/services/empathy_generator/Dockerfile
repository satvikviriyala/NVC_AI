# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies first for layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the shared libraries
COPY libs/ /app/libs/

# Copy the service-specific code
COPY services/empathy_generator/ /app/services/empathy_generator/

# The command to run the gRPC server
CMD ["python", "-u", "services/empathy_generator/main.py"]
