#!/usr/bin/env bash
#
# backup_db.sh — copy the TaskOps SQLite database to a timestamped backup file.
#
# Uses SQLite's online backup (consistent even while the app is running) when
# the container is up; otherwise falls back to copying the database file.
set -euo pipefail

# ---- Configuration (override via environment) -------------------------------
CONTAINER_NAME="${CONTAINER_NAME:-taskops-app}"
DB_PATH="${DATABASE_PATH:-/data/taskops.db}"   # path inside the container
HOST_DB_PATH="${HOST_DB_PATH:-}"               # optional path on the host
BACKUP_DIR="${BACKUP_DIR:-./backups}"
TIMESTAMP="$(date +%Y%m%d-%H%M%S)"
BACKUP_FILE="${BACKUP_DIR}/taskops-${TIMESTAMP}.db"

mkdir -p "${BACKUP_DIR}"

if docker ps --format '{{.Names}}' | grep -qx "${CONTAINER_NAME}"; then
  # Container is running: take a consistent online backup via Python's sqlite3.
  echo "Backing up live database from container ${CONTAINER_NAME}..."
  docker exec "${CONTAINER_NAME}" python -c "
import os, sqlite3
src = sqlite3.connect(os.environ.get('DATABASE_PATH', '${DB_PATH}'))
dst = sqlite3.connect('/tmp/taskops-backup.db')
with dst:
    src.backup(dst)
dst.close(); src.close()
"
  docker cp "${CONTAINER_NAME}:/tmp/taskops-backup.db" "${BACKUP_FILE}"
  docker exec "${CONTAINER_NAME}" rm -f /tmp/taskops-backup.db
elif [[ -n "${HOST_DB_PATH}" && -f "${HOST_DB_PATH}" ]]; then
  # Container not running: copy the file directly from the host.
  echo "Container not running; copying ${HOST_DB_PATH} from host..."
  cp "${HOST_DB_PATH}" "${BACKUP_FILE}"
else
  echo "ERROR: no running container and no readable HOST_DB_PATH to back up." >&2
  exit 1
fi

echo "Backup written to ${BACKUP_FILE}"
