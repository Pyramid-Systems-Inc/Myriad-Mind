# Integration Tester AI Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Copy requirements from the root
COPY requirements.txt .

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential

# Install python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the integration tester module and the orchestration logic it needs
COPY agents/integration_tester_ai/ ./agents/integration_tester_ai/
COPY orchestration/ ./orchestration/

# Set Python path to include the app directory
ENV PYTHONPATH=/app

# Expose the service port
EXPOSE 5009

# Run the Flask application
CMD ["python", "-m", "agents.integration_tester_ai.app"]