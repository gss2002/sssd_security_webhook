# Base image with Python 3.9
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the application code to the container
COPY ./mutating_webhook_security.py /app

# Install required Python packages
RUN pip install --no-cache-dir flask

# Expose the port the application will run on
EXPOSE 443

# Run the application
CMD ["python", "mutating_webhook_security.py"]
