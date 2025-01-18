# Use a base image with Python and SQLite support
FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y sqlite3 libsqlite3-dev

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install -r requirements.txt

# Expose port (if needed for local testing)
EXPOSE 8000

# Command to run your application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
