# Use the official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy dependencies
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Expose FastAPI port 
EXPOSE 8001

# Set environment variable
ENV PYTHONUNBUFFERED=1

# Run the app using Python directly
CMD ["python", "app.py"]
