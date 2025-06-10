#!/bin/bash

# run.sh - Build and run Lightbulb_AI container
# Myriad Cognitive Architecture - Phase 1

set -e  # Exit on any error

AGENT_NAME="lightbulb_ai"
PORT=5001

echo "=== Myriad Cognitive Architecture - Lightbulb_AI Agent ==="
echo "Building and running ${AGENT_NAME} on port ${PORT}"

# Stop and remove existing container if it exists
echo "Stopping existing container (if any)..."
docker stop ${AGENT_NAME} 2>/dev/null || true
docker rm ${AGENT_NAME} 2>/dev/null || true

# Build the Docker image
echo "Building Docker image..."
docker build -t ${AGENT_NAME}:latest .

# Run the container
echo "Starting container..."
docker run -d \
    --name ${AGENT_NAME} \
    -p ${PORT}:5001 \
    --restart unless-stopped \
    ${AGENT_NAME}:latest

echo "Container started successfully!"
echo "Agent is running on http://localhost:${PORT}"
echo ""
echo "Available endpoints:"
echo "  - http://localhost:${PORT}/health (Health check)"
echo "  - http://localhost:${PORT}/query (Main query endpoint)"
echo "  - http://localhost:${PORT}/info (Agent information)"
echo ""
echo "To view logs: docker logs ${AGENT_NAME}"
echo "To stop: docker stop ${AGENT_NAME}"