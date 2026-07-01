# TaskOps container image.
FROM python:3.12-slim

# Runtime knobs.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    DATABASE_PATH=/data/taskops.db

WORKDIR /app

# Dependency layer first so it is cached until requirements.txt changes.
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Non-root user and a writable, persistent data directory.
RUN useradd --create-home --uid 1000 appuser \
    && mkdir -p /data \
    && chown appuser:appuser /data

# Application code (changes most often -> latest layers).
COPY --chown=appuser:appuser app/ ./app/
COPY --chown=appuser:appuser wsgi.py ./

USER appuser

# SQLite database lives here; declared as a volume for persistence.
VOLUME ["/data"]

EXPOSE 5000

# Health probe uses the Python already in the image -- no curl, so the image
# needs no apt packages at all (smaller and fewer CVEs for Trivy to flag).
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD ["python", "-c", "import sys,urllib.request; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:5000/health', timeout=2).status == 200 else 1)"]

# gthread workers: threads share one process, so blocking I/O (SQLite, slow
# clients) doesn't stall a whole worker. /dev/shm avoids gunicorn heartbeat
# writes hitting the container's overlay filesystem.
CMD ["gunicorn", \
     "--workers", "2", \
     "--threads", "4", \
     "--worker-class", "gthread", \
     "--worker-tmp-dir", "/dev/shm", \
     "--access-logfile", "-", \
     "--bind", "0.0.0.0:5000", \
     "wsgi:app"]
