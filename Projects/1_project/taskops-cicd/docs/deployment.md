# Deployment

Production uses **one** strategy: the published GHCR image running **behind
nginx** via `docker-compose.prod.yml`. The CD workflow and the scripts in
`scripts/` both follow this same path, so there is no port/topology mismatch.

```
  Internet ─▶ nginx (taskops-nginx, :80) ─▶ taskops-app (gunicorn, :5000)
                                              └─ SQLite on taskops-data volume
```

## Prerequisites on the server

- A **Linux VM/host** you control.
- **Docker Engine** installed and running.
- The **Docker Compose plugin** (`docker compose`, v2) installed.
- **Port 80 open** to the internet (and reachable from GitHub runners for the
  post-deploy smoke test).
- **SSH access** for the deploy user, and that user able to run `docker`
  (in the `docker` group or via a sudo policy).
- Outbound access to `ghcr.io` to pull the image.

> **Honest note:** these workflows and scripts are validated locally, but the
> real CD path (GitHub Actions → SSH → server) can only be confirmed after you
> push the repo, configure the secrets below, and point it at a real server.

## Required GitHub Actions secrets

| Secret            | Used by                  | Purpose                                                          |
| ----------------- | ------------------------ | --------------------------------------------------------------- |
| `GITHUB_TOKEN`    | GHCR login / image pull  | **Auto-provided**; the job grants `packages: write`.            |
| `DEPLOY_HOST`     | scp/ssh + smoke test     | Server hostname or IP.                                           |
| `DEPLOY_USER`     | scp/ssh                  | SSH username.                                                    |
| `DEPLOY_SSH_KEY`  | scp/ssh                  | Private SSH key (PEM); public half in the server's `authorized_keys`. |
| `DEPLOY_PORT`     | scp/ssh                  | SSH port (e.g. 22).                                             |
| `FLASK_SECRET_KEY`| `deploy.sh` / compose    | Flask session signing key for the running container.            |

Configure under **Settings → Secrets and variables → Actions**. Generate a key:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

## Recommended: branch protection

Because CD deploys on every push to `main`, protect the branch so only verified
code lands there. Under **Settings → Branches → Add branch ruleset** (or
classic branch protection) for `main`:

- **Require a pull request before merging** (no direct pushes to `main`).
- **Require status checks to pass** — select the CI `quality` and `docker` jobs
  so lint/tests/security/Trivy must be green before merge.
- Optionally require the branch to be **up to date** before merging.

The CD `verify` job re-runs the core gates as a safety net, but branch
protection prevents broken code from reaching `main` in the first place.

## How the image reference stays configurable

`docker-compose.prod.yml` does not hardcode a personal image. It reads a
configurable reference with a generic default:

```yaml
image: "${IMAGE:-ghcr.io/your-username/taskops}:${IMAGE_TAG:-latest}"
```

`deploy.sh` writes these (plus the secret) to a `0600` `.env` next to the
compose file, which `docker compose` reads automatically.

## Automated deployment (CD)

On push to `main`, after the `verify` gates pass, CD builds and pushes the
image, copies the compose stack to `~/taskops/`, and runs `deploy.sh` over SSH.
Nothing to do manually.

## Manual deployment

On the server, with `docker-compose.prod.yml`, `docker/nginx.conf`, and
`scripts/` present (e.g. under `~/taskops/`):

```bash
export IMAGE=ghcr.io/<owner>/taskops
export IMAGE_TAG=<commit-sha>        # or "latest"
export FLASK_SECRET_KEY=...          # required
# export GHCR_USER=<user> GHCR_TOKEN=<token>   # if the image is private
bash scripts/deploy.sh
```

`deploy.sh`:

1. Optionally logs in to GHCR.
2. Records the currently deployed tag to `.previous_tag` (for rollback).
3. Writes a `0600` `.env` for compose (`IMAGE`, `IMAGE_TAG`, `FLASK_SECRET_KEY`,
   `MAX_TITLE_LENGTH`, `HTTP_PORT`).
4. `docker compose -f docker-compose.prod.yml pull && up -d`.
5. Waits for `http://localhost:80/health` (through nginx); prints compose logs
   on failure.

Override defaults via `IMAGE_TAG`, `HTTP_PORT`, `HEALTH_URL`, `DEPLOY_DIR`,
`COMPOSE_FILE`.

## Backups

```bash
bash scripts/backup_db.sh            # -> ./backups/taskops-YYYYMMDD-HHMMSS.db
```

While the stack is up, the script takes a **consistent** SQLite online backup
from the `taskops-app` container (not a raw file copy). If the container is
down, set `HOST_DB_PATH` to copy from the host.

## Rollback

```bash
bash scripts/rollback.sh
```

Reads `.previous_tag` (written by `deploy.sh`), rewrites `IMAGE_TAG` in `.env`,
re-deploys with `docker compose`, health-checks through nginx, and prints
`ROLLBACK SUCCEEDED` or `ROLLBACK FAILED`. A first-ever deploy has no previous
tag to roll back to and fails clearly.

## Verifying a deploy

```bash
HEALTH_URL=http://<host>/health bash scripts/smoke_test.sh
```

Exits 0 only when `/health` returns `status: ok`.

## Notes

- `GITHUB_TOKEN` is valid only during the workflow run; the server uses it to
  pull during the deploy window. For out-of-band pulls, use a PAT or make the
  GHCR package public.
- The local dev stack (`docker-compose.yml`) is separate: it builds the image
  and publishes the app directly on `APP_PORT` (5000) without nginx.
