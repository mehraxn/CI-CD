#!/usr/bin/env bash
#
# rollback.sh — revert the production stack to the previously deployed tag.
#
# Reads the tag recorded by deploy.sh (.previous_tag), rewrites IMAGE_TAG in the
# compose .env, re-deploys with that tag, and health-checks through nginx.
# Prints a clear ROLLBACK SUCCEEDED / FAILED status.
#
# Optional env: DEPLOY_DIR, COMPOSE_FILE, HTTP_PORT, HEALTH_URL, STATE_FILE.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEPLOY_DIR="${DEPLOY_DIR:-$(cd "${SCRIPT_DIR}/.." && pwd)}"
COMPOSE_FILE="${COMPOSE_FILE:-${DEPLOY_DIR}/docker-compose.prod.yml}"
HTTP_PORT="${HTTP_PORT:-80}"
HEALTH_URL="${HEALTH_URL:-http://localhost:${HTTP_PORT}/health}"
STATE_FILE="${STATE_FILE:-${DEPLOY_DIR}/.previous_tag}"

cd "${DEPLOY_DIR}"

# ---- Validate prerequisites -------------------------------------------------
if [[ ! -f .env ]]; then
  echo "ROLLBACK FAILED: no .env found in ${DEPLOY_DIR}; deploy first." >&2
  exit 1
fi
if [[ ! -f "${STATE_FILE}" ]]; then
  echo "ROLLBACK FAILED: no previous tag recorded at ${STATE_FILE}." >&2
  exit 1
fi
PREV_TAG="$(cat "${STATE_FILE}")"
if [[ -z "${PREV_TAG}" ]]; then
  echo "ROLLBACK FAILED: recorded previous tag is empty." >&2
  exit 1
fi
echo "Rolling back to tag ${PREV_TAG}..."

# ---- Point compose at the previous tag --------------------------------------
# Replace the IMAGE_TAG line in place; the rest of .env (secret, image) stays.
if grep -q '^IMAGE_TAG=' .env; then
  sed -i "s/^IMAGE_TAG=.*/IMAGE_TAG=${PREV_TAG}/" .env
else
  echo "IMAGE_TAG=${PREV_TAG}" >>.env
fi

# ---- Re-deploy --------------------------------------------------------------
docker compose -f "${COMPOSE_FILE}" pull
docker compose -f "${COMPOSE_FILE}" up -d --remove-orphans

# ---- Health check -----------------------------------------------------------
echo "Verifying health at ${HEALTH_URL}..."
for attempt in $(seq 1 20); do
  if curl -fsS "${HEALTH_URL}" 2>/dev/null | grep -q '"status": *"ok"'; then
    echo "ROLLBACK SUCCEEDED: now running tag ${PREV_TAG}."
    exit 0
  fi
  echo "  attempt ${attempt}/20: not ready yet, retrying in 3s..."
  sleep 3
done

echo "ROLLBACK FAILED: tag ${PREV_TAG} did not become healthy. Recent logs:" >&2
docker compose -f "${COMPOSE_FILE}" logs --tail 50 >&2 || true
exit 1
