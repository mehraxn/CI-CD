# TaskOps container image.
FROM python:3.12-slim

# Runtime knobs.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    DATABASE_PATH=/data/taskops.db

# System packages: curl is needed by the HEALTHCHECK.
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Dependency layer first so it is cached until requirements.txt changes.
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Application code (changes most often -> latest layers).
COPY app/ ./app/
COPY wsgi.py ./

# Non-root user and a writable, persistent data directory.
RUN useradd --create-home --uid 1000 appuser \
    && mkdir -p /data \
    && chown -R appuser:appuser /app /data
USER appuser

# SQLite database lives here; declared as a volume for persistence.
VOLUME ["/data"]

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -fsS http://localhost:5000/health || exit 1

# Serve with gunicorn, 2 workers.
CMD ["gunicorn", "--workers", "2", "--bind", "0.0.0.0:5000", "wsgi:app"]
