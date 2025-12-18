# Base image
FROM python:3.9-slim

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install system dependencies required for TensorFlow & Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libopenblas-dev \
    libatlas3-base \
    libhdf5-dev \
    libprotobuf-dev \
    protobuf-compiler \
    python3-dev \
    curl \
    git \
    && apt-get clean && rm -rf /var/lib/apt/lists/*


# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies + TensorFlow + DVC in a single layer
RUN pip install --no-cache-dir --default-timeout=600 --retries 10 -r requirements.txt \
    && rm -rf /root/.cache/pip
RUN pip install tensorflow-cpu==2.13.0 --no-cache-dir --progress-bar=on -v \
    && rm -rf /root/.cache/pip
RUN pip install dvc --no-cache-dir


# Expose Flask port
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]