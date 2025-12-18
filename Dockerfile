# Stage 1: build system dependencies
FROM python:3.9-slim AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libopenblas-dev \
    libhdf5-dev \
    libprotobuf-dev \
    protobuf-compiler \
    python3-dev \
    curl \
    git \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir dvc

# Stage 2: final image
FROM tensorflow/tensorflow:2.13.0-cpu-slim

WORKDIR /app
COPY --from=builder /app /app

EXPOSE 5000
CMD ["python", "app.py"]
