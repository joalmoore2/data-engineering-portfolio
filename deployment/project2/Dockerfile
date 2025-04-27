# Use the official lightweight Python image.
FROM python:3.12

LABEL maintainer="JoAnne Moore"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory in the container
WORKDIR /app

# Install system dependencies (Rust, GCC, build tools)
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libffi-dev \
    libssl-dev \
    curl \
    rustc \
    cargo

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Expose the port that the FastAPI app runs on
EXPOSE 8000

# Command to run the API using uvicorn
CMD ["uvicorn", "api_python:app", "--host", "0.0.0.0", "--port", "8000"]