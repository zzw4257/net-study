# Use a common base image like Ubuntu, which is more likely to be cached.
FROM ubuntu:22.04

# Avoid interactive prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

# Install Python, pip, and the 'requests' library
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    pip3 install --no-cache-dir requests && \
    rm -rf /var/lib/apt/lists/*

# Set python3 as the default python
RUN ln -s /usr/bin/python3 /usr/bin/python

# Set the working directory in the container
WORKDIR /app

# Create a non-root user and group
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

# Copy the script that will be run into the container
COPY . /app

# Change the owner of the /app directory
RUN chown -R appuser:appgroup /app

# Switch to the non-root user
USER appuser

# The command to run when the container starts.
CMD ["python", "user_script.py"]
