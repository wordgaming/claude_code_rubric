# Use Python 3.12 slim image for smaller size
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install any system dependencies if needed
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     gcc \
#     && rm -rf /var/lib/apt/lists/*

# Copy the project files
COPY . .

# Install the package in development mode
RUN pip install --no-cache-dir -e .

# Default to bash shell for development
CMD ["/bin/bash"]