# Use a Python image with uv pre-installed as base layer
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Copy the service into the image and sync with new environment
WORKDIR /app
ADD . /app
RUN uv sync --frozen

# Start the service by default
CMD ["uv", "run", "run.py"]