# Security

This project applies a handful of practical, verifiable controls. It is a
portfolio app, not a hardened production system — the controls below are what is
actually implemented.

## Application-level controls

- **Parameterized SQL.** Every statement in `app/database.py` uses placeholders
  (`?`) with bound parameters. User input is never concatenated into SQL,
  preventing SQL injection.
- **No hardcoded secrets.** `app/config.py` reads `FLASK_SECRET_KEY`,
  `DATABASE_PATH`, and `MAX_TITLE_LENGTH` from the environment. The only literal
  is a clearly non-secret development fallback for the session key.
- **Input validation.** Task creation requires a non-empty title within
  `MAX_TITLE_LENGTH`; empty/whitespace input is rejected and re-rendered.
- **Output escaping.** Templates use Jinja2 autoescaping (enabled by default for
  `.html`), mitigating reflected/stored XSS in rendered task content. This is
  covered by `tests/test_security.py`, which asserts an HTML/script payload in a
  task title and description is escaped.
- **Secret required in production.** The production compose file and deploy
  script refuse to start without `FLASK_SECRET_KEY`. The app factory also logs a
  warning if the insecure development fallback key is used outside of tests.

## Container controls

- Built from `python:3.12-slim` (smaller attack surface than a full image).
- Runs as a **non-root** user (`appuser`, uid 1000).
- Dependencies are installed from a **pinned** `requirements.txt`.
- A `HEALTHCHECK` allows the orchestrator to detect an unhealthy container.

## Automated scanning

| Tool      | Scope                         | Where                                          |
| --------- | ----------------------------- | ---------------------------------------------- |
| bandit    | Python SAST over `app/`       | CI `quality` + `make security` / `bandit -r app` |
| pip-audit | Dependency CVEs (runtime)     | CI `quality` + `make audit` / `pip-audit -r requirements.txt` |
| Trivy     | Container image CVEs          | CI `docker` job, after build (HIGH/CRITICAL → fail) |

bandit and pip-audit run on every push and pull request and locally via the
`Makefile`. Trivy runs in the CI `docker` job against the freshly built image.

### Configuration

- bandit is configured in `pyproject.toml` to exclude the `tests/` directory.
- pip-audit audits the pinned runtime dependencies in `requirements.txt`.
- Trivy fails on `HIGH,CRITICAL` with `ignore-unfixed: true`, so the build is
  blocked by actionable, fixable vulnerabilities but not by un-patchable
  base-image CVEs.

## Dependency hygiene

- Runtime and dev dependencies are pinned to exact versions.
- A previously flagged Flask advisory (GHSA-68rp-wp8r-4726) was remediated by
  pinning Flask to 3.1.3; gunicorn is pinned to 23.0.0. `pip-audit` reports no
  known vulnerabilities at the time of writing.
- Re-run `make audit` periodically and bump pins when new advisories appear.

## Secrets handling

- Real secrets live in GitHub Actions secrets and the server environment, never
  in the repository. `.env` is gitignored; only `.env.example` is committed.
- `GITHUB_TOKEN` is short-lived and scoped to the workflow run.

## Known limitations (out of scope)

- No authentication or authorization — all routes are public.
- CSRF protection is a minimal in-house implementation (session token +
  constant-time compare); a framework like Flask-WTF would add per-form
  tokens and time limits.
- No rate limiting or TLS termination in the app itself (TLS would be terminated
  at nginx/load balancer in a real deployment; HTTPS is a future improvement).
- SQLite is demo / small-deployment level (single-writer).

These are deliberately listed so the security posture is not overstated.

## Future security improvements

- Swap the in-house CSRF implementation for **Flask-WTF** if forms grow.
- **Authentication / authorization** (per-user task lists).
- **HTTPS** terminated at the proxy — Let's Encrypt, Caddy, or Traefik.
- **PostgreSQL** instead of SQLite for concurrent, multi-instance deployments.
- **Dependabot** for automated dependency-update PRs.
- Broader **SAST/DAST** coverage in CI.
