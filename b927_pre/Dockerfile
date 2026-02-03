FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Install the package in development mode
RUN pip install -e .

# Start container with interactive shell instead of running tests
CMD ["/bin/bash"]