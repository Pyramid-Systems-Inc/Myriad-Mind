# GraphDB Manager AI Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Copy requirements from the root
COPY requirements.txt .

# Install system dependencies required for building Python packages
RUN apt-get update && apt-get install -y build-essential

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the graphdb manager module
COPY agents/graphdb_manager_ai/ ./agents/graphdb_manager_ai/

# Set Python path to include the app directory
ENV PYTHONPATH=/app

# Expose the service port
EXPOSE 5008

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:5008/health || exit 1

# Run the Flask application
CMD ["python", "-m", "agents.graphdb_manager_ai.app"]