# Enhanced Input Processor Dockerfile
# Builds the "Sensory Cortex" microservice

FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the input processor module
COPY processing/input_processor/ ./processing/input_processor/

# Copy the main processing module init
COPY processing/__init__.py ./processing/

# Set Python path to include the app directory
ENV PYTHONPATH=/app

# Expose the service port
EXPOSE 5003

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5003/health || exit 1

# Run the Flask application
CMD ["python", "-m", "processing.input_processor.app"]
