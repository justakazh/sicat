# Use official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies (Nmap is required for scanning)
RUN apt-get update && apt-get install -y \
    nmap \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the application
# This uses setup.py to install dependencies and the 'sicat' command
RUN pip install --no-cache-dir .

# Expose port 5000 for the Web Interface
EXPOSE 5000

# Define a volume to persist configuration (e.g., gh_token in config.json)
VOLUME ["/root/.sicat"]

# Set the entrypoint to the sicat command
ENTRYPOINT ["sicat"]

# Default argument (can be overridden)
CMD ["--help"]
