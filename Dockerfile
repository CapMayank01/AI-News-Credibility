FROM python:3.11.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN useradd -m -u 1000 appuser

# Upgrade pip
RUN pip install --upgrade pip --root-user-action=ignore

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --root-user-action=ignore -r requirements.txt

# Copy application
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Set PYTHONPATH environment variable so app modules can be loaded from backend subfolder
ENV PYTHONPATH=/app/backend

# Run the application
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port $PORT"]
