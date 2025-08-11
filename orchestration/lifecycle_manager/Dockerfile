# Lifecycle Manager Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Copy requirements from the root
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the lifecycle manager module
COPY orchestration/lifecycle_manager/ ./orchestration/lifecycle_manager/

# Copy the main orchestration module init
COPY orchestration/__init__.py ./orchestration/

# Set Python path to include the app directory
ENV PYTHONPATH=/app

# Expose the service port
EXPOSE 5005

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5005/health || exit 1

# Run the Flask application
CMD ["python", "-m", "orchestration.lifecycle_manager.app"]