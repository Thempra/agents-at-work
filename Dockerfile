# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create a non-root user and switch to it
RUN groupadd -r app && \
    useradd -r -g app app && \
    mkdir /app && \
    chown -R app:app /app

# Copy the current directory contents into the container at /app
USER app
WORKDIR /app

# Install any needed packages specified in requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files and initialize database
COPY . .

# Run migrations if necessary
RUN alembic upgrade head

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
