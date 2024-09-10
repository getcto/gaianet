# Use the official Ubuntu base image
FROM ubuntu:latest

# Set environment variables to avoid user interaction during package installations
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies and necessary packages including lsof
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    curl \
    bash \
    lsof \
    netcat-openbsd && \
    rm -rf /var/lib/apt/lists/*

# Create and activate a virtual environment
RUN python3 -m venv /env

# Set the environment variable for the virtual environment
ENV PATH="/env/bin:$PATH"

# Install Python dependencies in the virtual environment
RUN pip install --no-cache-dir \
    pandas \
    sentence-transformers \
    qdrant-client \
    einops

# Download and execute the GaiaNet installation script
RUN curl -sSfL 'https://github.com/GaiaNet-AI/gaianet-node/releases/latest/download/install.sh' | bash

# Add the GaiaNet binary path to PATH
ENV PATH="/root/gaianet/bin:$PATH"

# Set the working directory
WORKDIR /app

# Copy the entrypoint script into the Docker image
COPY entrypoint.sh /app/entrypoint.sh

RUN chmod +x /app/entrypoint.sh

# Set the entry point to the script
ENTRYPOINT ["/app/entrypoint.sh"]
