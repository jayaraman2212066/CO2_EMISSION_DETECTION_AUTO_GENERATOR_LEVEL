# Use a lightweight Python base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install PostgreSQL client libraries and other necessary build tools
# These are needed for database connectivity and potentially other build steps
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy the rest of the application code into the container
COPY . /app

# Expose the port the application listens on (Assuming Flask/Gunicorn default is 5000, adjust if needed)
EXPOSE $PORT

# Define the command to run your application using Gunicorn
CMD ["/bin/bash", "-c", "gunicorn --bind 0.0.0.0:$PORT --timeout 120 --workers 2 --threads 2 app:app"] 