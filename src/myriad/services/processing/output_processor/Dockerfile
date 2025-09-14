# Enhanced Output Processor Dockerfile
# Builds the "Motor Cortex" microservice

FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install system dependencies required for building Python packages
RUN apt-get update && apt-get install -y build-essential

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the output processor module
COPY processing/output_processor/ ./processing/output_processor/

# Copy the main processing module init
COPY processing/__init__.py ./processing/

# Set Python path to include the app directory
ENV PYTHONPATH=/app

# Expose the service port
EXPOSE 5004

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5004/health || exit 1

# Run the Flask application
CMD ["python", "-m", "processing.output_processor.app"]