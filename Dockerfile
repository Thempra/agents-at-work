Dockerfile
# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables to make the container run without prompts
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create a non-root user and switch to it
RUN useradd -m appuser
USER appuser

# Working directory inside the container
WORKDIR /app

# Copy project files into the container at /app
COPY . .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose port 8000 for FastAPI
EXPOSE 8000

# Command to run the app using Gunicorn with multiple workers
CMD ["gunicorn", "-w", "4", "-b", ":8000", "app.main:app"]
