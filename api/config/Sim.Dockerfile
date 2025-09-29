FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && \
  apt-get install -y --no-install-recommends \
  iputils-ping \
  curl \
  && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY telemetry_sim.py .

# Run the simulator
CMD ["python", "-u", "telemetry_sim.py"]
