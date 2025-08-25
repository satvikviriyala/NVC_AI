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
COPY services/api_gateway/ /app/services/api_gateway/

# The command to run the FastAPI server with uvicorn
CMD ["uvicorn", "services.api_gateway.main:app", "--host", "0.0.0.0", "--port", "8000"]
