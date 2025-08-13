# Agent Registry Service Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

# Install system dependencies required for building Python packages
RUN apt-get update && apt-get install -y build-essential

RUN pip install --no-cache-dir -r requirements.txt

COPY orchestration/agent_registry_service/ ./orchestration/agent_registry_service/
COPY orchestration/__init__.py ./orchestration/

ENV PYTHONPATH=/app

EXPOSE 5006

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5006/health || exit 1

CMD ["python", "-m", "orchestration.agent_registry_service.app"]