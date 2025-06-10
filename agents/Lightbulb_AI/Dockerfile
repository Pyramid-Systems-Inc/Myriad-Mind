# Dockerfile for Lightbulb_AI Agent
# Myriad Cognitive Architecture - Phase 1

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the agent application
COPY agent_app.py .

# Expose the port
EXPOSE 5001

# Set environment variables
ENV PORT=5001
ENV PYTHONUNBUFFERED=1

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5001/health || exit 1

# Run the application
CMD ["python", "agent_app.py"]