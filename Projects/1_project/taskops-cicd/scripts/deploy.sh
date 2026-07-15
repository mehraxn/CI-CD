#!/usr/bin/env bash
#
# deploy.sh — deploy TaskOps using the production compose stack (app + nginx).
#
# Pulls the requested image, writes a locked-down .env for compose, brings the
# stack up, and waits for /health (served through nginx on port 80) to report
# ok. Records the previously deployed tag so rollback.sh can revert.
#
# Required env:
#   IMAGE             image repository, e.g. ghcr.io/<owner>/taskops
#   FLASK_SECRET_KEY  Flask session signing key
# Optional env:
#   IMAGE_TAG (default "latest"), MAX_TITLE_LENGTH (default 120),
#   HTTP_PORT (default 80), GHCR_USER/GHCR_TOKEN (to pull private images),
#   DEPLOY_DIR, COMPOSE_FILE, HEALTH_URL.
set -euo pipefail

# ---- Resolve the deploy directory (where the compose file lives) ------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEPLOY_DIR="${DEPLOY_DIR:-$(cd "${SCRIPT_DIR}/.." && pwd)}"
COMPOSE_FILE="${COMPOSE_FILE:-${DEPLOY_DIR}/docker-compose.prod.yml}"

# ---- Configuration ----------------------------------------------------------
IMAGE="${IMAGE:?IMAGE must be set (e.g. ghcr.io/<owner>/taskops)}"
IMAGE_TAG="${IMAGE_TAG:-latest}"
HTTP_PORT="${HTTP_PORT:-80}"
HEALTH_URL="${HEALTH_URL:-http://localhost:${HTTP_PORT}/health}"
STATE_FILE="${STATE_FILE:-${DEPLOY_DIR}/.previous_tag}"
: "${FLASK_SECRET_KEY:?FLASK_SECRET_KEY must be set}"

cd "${DEPLOY_DIR}"

# ---- Authenticate to GHCR (optional) ----------------------------------------
if [[ -n "${GHCR_USER:-}" && -n "${GHCR_TOKEN:-}" ]]; then
  echo "Logging in to ghcr.io as ${GHCR_USER}..."
  echo "${GHCR_TOKEN}" | docker login ghcr.io -u "${GHCR_USER}" --password-stdin
fi

# ---- Record the currently deployed tag for rollback -------------------------
if [[ -f .env ]]; then
  CURRENT_TAG="$(sed -n 's/^IMAGE_TAG=//p' .env | head -n1 || true)"
  if [[ -n "${CURRENT_TAG:-}" ]]; then
    echo "${CURRENT_TAG}" >"${STATE_FILE}"
    echo "Recorded previous tag for rollback: ${CURRENT_TAG}"
  fi
fi

# ---- Write the compose env file (contains a secret -> 0600) -----------------
echo "Writing ${DEPLOY_DIR}/.env..."
(
  umask 077
  cat >.env <<EOF
IMAGE=${IMAGE}
IMAGE_TAG=${IMAGE_TAG}
FLASK_SECRET_KEY=${FLASK_SECRET_KEY}
MAX_TITLE_LENGTH=${MAX_TITLE_LENGTH:-120}
HTTP_PORT=${HTTP_PORT}
EOF
)

# ---- Pull and start the stack ----------------------------------------------
echo "Deploying ${IMAGE}:${IMAGE_TAG} via ${COMPOSE_FILE}..."
docker compose -f "${COMPOSE_FILE}" pull
docker compose -f "${COMPOSE_FILE}" up -d --remove-orphans

# ---- Wait for health (through nginx) ----------------------------------------
echo "Waiting for ${HEALTH_URL} to become healthy..."
for attempt in $(seq 1 20); do
  if curl -fsS "${HEALTH_URL}" 2>/dev/null | grep -q '"status": *"ok"'; then
    echo "Deploy succeeded: ${IMAGE}:${IMAGE_TAG} is healthy."
    exit 0
  fi
  echo "  attempt ${attempt}/20: not ready yet, retrying in 3s..."
  sleep 3
done

echo "ERROR: stack did not become healthy. Recent logs:" >&2
docker compose -f "${COMPOSE_FILE}" logs --tail 50 >&2 || true
exit 1
