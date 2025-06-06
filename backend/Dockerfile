# Build stage
FROM python:3.11-slim AS builder

# Set build-time environment variables
ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    POETRY_VERSION=1.7.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PATH="/opt/poetry/bin:$PATH"

# Install system dependencies required for building
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    poetry --version

# Copy dependency files
COPY pyproject.toml poetry.lock ./

# Copy application code for installation
COPY app ./app
COPY utils ./utils
COPY routers ./routers
COPY services ./services
COPY models ./models
COPY api_models ./api_models
COPY config ./config

# Install dependencies and project
RUN poetry install --no-dev

# Runtime stage
FROM python:3.11-slim

# Set runtime environment variables
ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PORT=8000 \
    HOST=0.0.0.0 \
    PYTHONPATH=/app

# Install system dependencies required at runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser

WORKDIR /app

# Copy virtual environment and application code
COPY --from=builder /app/.venv /app/.venv
COPY --chown=appuser:appuser app ./app
COPY --chown=appuser:appuser utils ./utils
COPY --chown=appuser:appuser routers ./routers
COPY --chown=appuser:appuser services ./services
COPY --chown=appuser:appuser models ./models
COPY --chown=appuser:appuser api_models ./api_models
COPY --chown=appuser:appuser config ./config

# Switch to non-root user
USER appuser

# Add virtual environment to PATH
ENV PATH="/app/.venv/bin:$PATH"

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT}/health || exit 1

# Expose port
EXPOSE ${PORT}

# Start command using environment variables
CMD ["/app/.venv/bin/uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4", "--limit-concurrency", "1000", "--backlog", "2048"]