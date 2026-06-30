#!/usr/bin/env bash
#
# smoke_test.sh — verify the /health endpoint reports status "ok".
#
# Exits 0 only when the endpoint returns a JSON body containing "status":"ok".
# Retries a few times so it can be used right after a deploy/start.
set -euo pipefail

# ---- Configuration (override via environment) -------------------------------
HEALTH_URL="${HEALTH_URL:-http://localhost:5000/health}"
RETRIES="${RETRIES:-10}"
SLEEP_SECONDS="${SLEEP_SECONDS:-3}"

echo "Smoke testing ${HEALTH_URL} (up to ${RETRIES} attempts)..."
for attempt in $(seq 1 "${RETRIES}"); do
  if body="$(curl -fsS "${HEALTH_URL}" 2>/dev/null)" \
      && echo "${body}" | grep -q '"status": *"ok"'; then
    echo "OK: ${body}"
    exit 0
  fi
  echo "  attempt ${attempt}/${RETRIES}: not healthy yet, retrying in ${SLEEP_SECONDS}s..."
  sleep "${SLEEP_SECONDS}"
done

echo "ERROR: ${HEALTH_URL} did not return status ok." >&2
exit 1
