FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements (we'll use the main requirements.txt for now)
COPY ../../requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application
COPY app.py .

# Expose port 5001
EXPOSE 5001

# Run the application
CMD ["python", "app.py"]