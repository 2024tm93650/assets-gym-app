FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

# Create a non-root user for security
RUN adduser --disabled-password --no-create-home gymuser
USER gymuser

# Expose port 5000
EXPOSE 5000

# Run the Flask application
CMD ["python", "app.py"]
