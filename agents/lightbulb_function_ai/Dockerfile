FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements (we'll use the main requirements.txt for now)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application
COPY agents/lightbulb_function_ai/app.py .

# Expose port 5002
EXPOSE 5002

# Run the application
CMD ["python", "app.py"]