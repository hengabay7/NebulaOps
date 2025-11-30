FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y gcc wget curl

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Expose port
EXPOSE 5000

# Run app with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]

