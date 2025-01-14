# Use Python slim image as base
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && apt-get clean

# Copy requirements file and install dependencies
COPY ./requirements.txt /app/
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the Django application code
COPY .  /app/

# Expose the Django development server port
EXPOSE 8000

# Default command to run the Django app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
