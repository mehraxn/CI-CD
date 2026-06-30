# CI/CD Pipeline

Two GitHub Actions workflows drive the pipeline. They must live in
`.github/workflows/` at the **repository root** to run (see
[troubleshooting](troubleshooting.md#workflows-dont-run-on-github)).

## CI — `.github/workflows/ci.yml`

**Triggers:** every `push` (any branch) and every `pull_request`.

### Job: `quality` (ubuntu-latest)

1. Checkout.
2. Set up Python 3.12 with pip caching keyed on `requirements-dev.txt`.
3. Upgrade pip, install `requirements-dev.txt`.
4. Each gate is a separate step (any failure fails the job):
   `ruff check .`, `black --check .`, `isort --check-only .`, `pytest`,
   `bandit -r app`, `pip-audit -r requirements.txt`.

### Job: `docker` (needs: `quality`)

1. Checkout.
2. `docker build -t taskops:ci .`
3. **Trivy scan** of `taskops:ci` (`aquasecurity/trivy-action`). Fails the build
   on `HIGH,CRITICAL` vulnerabilities. `ignore-unfixed: true` keeps it realistic
   for a portfolio — un-patchable base-image CVEs don't block the build, but
   actionable ones do.
4. Run the container with a throwaway `FLASK_SECRET_KEY`.
5. Smoke-test `/health` in a retry loop (matches `"status": *"ok"`); prints
   `docker logs` and fails on timeout.
6. `if: always()` cleanup removes the container.

## CD — `.github/workflows/cd.yml`

**Trigger:** `push` to `main` only.

### Job: `verify` (ubuntu-latest)

Re-runs the critical gates (`ruff`, `black --check`, `isort --check-only`,
`pytest`, `bandit`) so a direct push of broken code to `main` is **not
deployed**. The `deploy` job depends on this job.

### Job: `deploy` (needs: `verify`)

**Permissions:** `contents: read`, `packages: write`.

1. Checkout.
2. Compute a **lowercase** image name (`ghcr.io/<owner-lowercased>/taskops`) so
   an uppercase owner/org can't break the GHCR push.
3. Log in to GHCR using `github.actor` + the auto-provided `GITHUB_TOKEN`.
4. Set up Buildx.
5. **Build the image locally** (`load: true`, not pushed yet), tagged with the
   commit SHA and `latest`.
6. **Trivy scan before publishing** — fails on fixable `HIGH,CRITICAL`. Because
   CD does not depend on CI, this guarantees a vulnerable image is never
   deployed.
7. **Push** both tags to GHCR.
8. Copy `docker-compose.prod.yml`, `docker/nginx.conf`, and `scripts/*.sh` to
   the server (`appleboy/scp-action`) under `~/taskops/`.
9. SSH in and run `deploy.sh`, passing `IMAGE`, `IMAGE_TAG` (the SHA),
   `FLASK_SECRET_KEY`, `MAX_TITLE_LENGTH`, `HTTP_PORT`, and GHCR pull
   credentials via the action's `envs`. `script_stop: true` fails fast.
10. Post-deploy: run `scripts/smoke_test.sh` against `http://<DEPLOY_HOST>/health`
    (port 80, through nginx); a non-healthy response fails the job.

## Image tagging

- `:<commit-sha>` — immutable; the deploy target, recorded for rollback.
- `:latest` — pointer to the most recent main build.

## Port consistency

The whole production path agrees on **port 80 / nginx**: the prod compose file
publishes nginx on 80, `deploy.sh` health-checks `http://localhost:80/health`,
and the CD smoke test checks `http://<host>/health`. There is no 5000-vs-80
mismatch.

## Required secrets

See [deployment.md](deployment.md#required-github-actions-secrets).

## Local parity

`make check` reproduces the CI `quality` job locally before you push.
