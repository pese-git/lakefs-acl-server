# syntax=docker/dockerfile:1
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Install pip dependencies
COPY pyproject.toml uv.lock ./
RUN pip install --upgrade pip \
    && pip install uv
RUN uv pip install --system --no-cache-dir

# Copy all source code
COPY app ./app

# Expose the default FastAPI port
EXPOSE 8000

# Run FastAPI app with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
