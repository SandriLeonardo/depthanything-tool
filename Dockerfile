# ── Stage: runtime ────────────────────────────────────────────────────────────
# CPU-only image. For GPU support swap the base image with the CUDA variant:
#   FROM pytorch/pytorch:2.3.0-cuda12.1-cudnn8-runtime
FROM python:3.11-slim

LABEL maintainer="leosa"
LABEL description="Depth Anything V2 — convert any image to a depth map PNG"

# System dependencies needed by OpenCV / Pillow
RUN apt-get update && apt-get install -y --no-install-recommends \
        libglib2.0-0 \
        libgl1 \
        libheif1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies first (layer-cached until requirements change)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy inference script
COPY run_depth.py .

# Hugging Face model cache lives in a named volume so it's not re-downloaded
# on every run (see docker-compose.yml)
ENV HF_HOME=/cache/huggingface

# Default: process /data/input.jpg → /data/output/depth.png
# Override at runtime with: docker run ... --input ... --output ...
ENTRYPOINT ["python", "run_depth.py"]
CMD ["--input", "/data/input.jpg", "--output", "/data/output/depth.png", "--model", "small"]
