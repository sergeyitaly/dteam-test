FROM python:3.9-slim-bookworm

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIP_NO_CACHE_DIR 1
ENV PIP_DISABLE_PIP_VERSION_CHECK 1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    python3-dev \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libcairo2 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m appuser && \
    mkdir /app && \
    chown appuser:appuser /app

WORKDIR /app

# Install Python dependencies
COPY pyproject.toml poetry.lock* ./

RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --no-interaction --no-ansi

# Copy application code
COPY --chown=appuser:appuser . .

# Install additional production dependencies explicitly
RUN pip install \
    django-celery-results==2.5.1 \
    django-celery-beat==2.5.0 \
    redis==4.6.0

# Collect static files
RUN python manage.py collectstatic --noinput

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1