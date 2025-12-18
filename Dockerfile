# Base image
FROM python:3.8-slim

# Set environment variables to prevent Python from writing .pyc files & Ensure Python output is not buffered
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install system dependencies required by TensorFlow
RUN apt-get update && apt-get install -y \
    build-essential \
    libatlas-base-dev \
    libhdf5-dev \
    libprotobuf-dev \
    protobuf-compiler \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy code & requirements
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install TensorFlow separately (optional, you could include in requirements.txt)
RUN pip install tensorflow-cpu==2.20.0 --no-cache-dir --progress-bar=on -v
RUN pip install dvc --no-cache-dir

# (Optional) Pre-train model during image build
# Be careful: this makes image building slow
# RUN python pipeline/training_pipeline.py

# Expose Flask port
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]
