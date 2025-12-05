FROM python:3.13-slim

WORKDIR /app

# Install system dependencies (optional but useful for many Python packages)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install uv (since the project uses pyproject/uv.lock)
RUN pip install --no-cache-dir uv

# Install Python dependencies using uv, leveraging the lockfile
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# Copy application code
COPY . .

# Default port (can be overridden at runtime)
ENV PORT=8000
EXPOSE 8000

# Run the app via run.py (which reads PORT from env)
CMD ["uv", "run", "python", "run.py"]


