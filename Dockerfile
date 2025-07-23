# Use Python base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y gcc libpq-dev

# Copy pyproject.toml and install dependencies via Hatch
COPY pyproject.toml .
COPY . /app/

# Install hatch and uv
RUN pip install --no-cache-dir hatch uv

# Install dependencies using uv (respects pyproject.toml)
RUN pip install -e .

# Expose FastAPI default port
EXPOSE 5000

# Run the application with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000"]
