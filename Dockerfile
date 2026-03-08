# Use lightweight Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create non-root user
RUN useradd -m gymuser
USER gymuser

# Expose application port
EXPOSE 5000

# Run the Flask application
CMD ["python", "app.py"]