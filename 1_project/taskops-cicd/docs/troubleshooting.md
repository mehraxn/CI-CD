# Troubleshooting

Common problems and how to fix them, grouped by area.

## Local development

### `python wsgi.py` fails or wrong Python version

The project targets Python 3.12. Check `python --version`. On Windows the `py`
launcher can install and select it:

```bash
py install 3.12
py -3.12 -m venv .venv
```

### `gunicorn` won't run on Windows

Expected. gunicorn depends on Unix-only modules and is used **inside the
container**. For local runs use `python wsgi.py` (Flask dev server) or run the
app via Docker.

### `ModuleNotFoundError: app`

Run from the project root (where `pyproject.toml` lives). pytest is configured
with `pythonpath = ["."]`; for ad-hoc scripts ensure the root is on
`PYTHONPATH`.

### Virtual environment: activation does nothing / wrong packages

Create and activate the venv from the project root: `python -m venv .venv`,
then `source .venv/bin/activate` (macOS/Linux) or `.venv\Scripts\Activate.ps1`
(Windows PowerShell). `which python` (or `Get-Command python`) should point
inside `.venv`.

### Missing dependencies (ImportError / ModuleNotFoundError for a package)

Install dev requirements into the active venv: `pip install -r
requirements-dev.txt`. The runtime-only set is `requirements.txt`.

### Tests fail

Run `python -m pytest -v` to see which test and why. After code or dependency
changes, reinstall (`pip install -r requirements-dev.txt`) and re-run. Tests use
an isolated temp SQLite database, so a stale `taskops.db` is never the cause.

### Database file keeps reappearing / stale data

The dev database is the file at `DATABASE_PATH` (default `taskops.db`). Delete
it to reset, or point `DATABASE_PATH` at a throwaway path. Tests never use it —
they create a temp file per run.

## Quality gates

### black or isort "would reformat"

Run the formatters to fix in place:

```bash
make format        # black . && isort .
```

`make format-check` (and CI) only check; they do not modify files.

### ruff `UP` errors about typing

ruff's `UP` rules modernize type hints (e.g. `Optional[X]` → `X | None`). Apply
fixes with `ruff check --fix .`.

### pip-audit reports a vulnerability

Bump the affected package in `requirements.txt` to the listed fix version,
reinstall, and re-run:

```bash
pip install -r requirements.txt
make audit
```

## Docker

### `docker: command not found` locally

Docker is not installed on the machine. Install Docker Desktop (Windows/macOS)
or Docker Engine (Linux). CI builds the image on GitHub-hosted runners
regardless of your local setup.

### Health check fails right after start

The app needs a moment to boot. `deploy.sh`, `smoke_test.sh`, and the CI smoke
step already retry. If it still fails, inspect logs:

```bash
docker logs <container>
```

A common cause is a missing `FLASK_SECRET_KEY` in production paths — the app and
compose require it.

### Container exits immediately

Check logs. Likely causes: `/data` not writable (the image creates it owned by
`appuser`; a host bind mount with wrong ownership can break this — prefer the
named volume) or a bad environment value.

### Port already in use (5000 or 80)

Another process/container holds the port. Find and stop it (`docker ps` then
`docker rm -f <name>`), or choose a different host port: `APP_PORT=5001 docker
compose up` (dev), or `HTTP_PORT=8080 docker compose -f docker-compose.prod.yml
up -d` (prod).

### Docker build fails

Re-run with full output: `docker build -t taskops:test .`. Common causes:
no network to fetch the base image / wheels, or an out-of-date Docker. The build
context is trimmed by `.dockerignore`, so `.venv`/caches are not the cause.

### nginx returns 502 / cannot reach app

In the prod stack, nginx proxies to `app:5000` over the compose network. A 502
means the app container isn't healthy. Check `docker compose -f
docker-compose.prod.yml ps` and `docker logs taskops-app`. nginx waits on the
app's healthcheck (`depends_on: condition: service_healthy`), so a crash-looping
app (often a missing `FLASK_SECRET_KEY`) is the usual cause.

## CI/CD

### Workflows don't run on GitHub

GitHub Actions only reads workflows from `.github/workflows/` **at the
repository root**. If this project lives in a subdirectory of a larger repo, the
workflows must be moved to the repo-root `.github/workflows/` (and paths in the
steps adjusted) to be picked up.

### CD: `denied` / `unauthorized` pushing to GHCR

Ensure the `deploy` job has `permissions: packages: write` (it does in
`cd.yml`) and that you are pushing to `ghcr.io/<owner>/...` matching the
repository owner.

### CD: SSH step fails to connect

Verify the `DEPLOY_HOST`, `DEPLOY_USER`, `DEPLOY_PORT`, and `DEPLOY_SSH_KEY`
secrets. The key must be the **private** key (full PEM, including header/footer)
whose public counterpart is in the server's `authorized_keys`.

### CD: server can't pull the image

The package is private by default. The deploy passes `GHCR_USER`/`GHCR_TOKEN`
so `deploy.sh` can `docker login`. For manual pulls outside the workflow, log in
on the server with a PAT, or make the GHCR package public.

### Post-deploy smoke test fails but the app is up

Production runs behind nginx on port 80, and the smoke test targets
`http://<DEPLOY_HOST>/health` to match. If `/health` works on the server
(`curl http://localhost/health` on the host) but the CD smoke test fails from
the runner, the cause is almost always networking: port 80 is not reachable from
GitHub's runners (firewall/security group). Open port 80, or point `HEALTH_URL`
at a reachable address.

## Scripts

### Scripts fail with `bad interpreter` or `\r` errors on the server

The script files have CRLF line endings. This repo includes a `.gitattributes`
forcing LF for `*.sh`; ensure it is committed and re-checkout, or run
`dos2unix scripts/*.sh` on the server.

### `rollback.sh` says "no previous tag recorded"

`deploy.sh` writes the previously deployed tag to `.previous_tag` (next to the
compose file) only after at least one prior deploy. A first-ever deploy has
nothing to roll back to.
