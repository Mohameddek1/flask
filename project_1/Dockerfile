# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements.txt first to leverage caching
COPY requirement.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirement.txt

# Copy the rest of the application files
COPY . /app/

# Expose the Flask default port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
