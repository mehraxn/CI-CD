# TaskOps — My Production-Style CI/CD Pipeline for a Flask App

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.1-000000?logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-stdlib-003B57?logo=sqlite&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-compose-2496ED?logo=docker&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-2088FF?logo=githubactions&logoColor=white)
![Security](https://img.shields.io/badge/Security-bandit%20%7C%20pip--audit%20%7C%20Trivy-1904DA?logo=aqua&logoColor=white)
![Tests](https://img.shields.io/badge/Tests-25%20passing-success)
![License](https://img.shields.io/badge/License-MIT-green)

> **TaskOps** is a small Flask + SQLite task tracker that I built to show off a
> **complete, production-style CI/CD pipeline** — not to be a giant app. The web
> app itself is kept simple on purpose, so the real star of the project is the
> **DevOps work around it**: testing, security scanning, containerization, image
> publishing, and automated deployment.

I made this as a **portfolio project** for junior DevOps / Cloud / CI-CD roles.
To be honest about the scope: it's a *production-style* delivery pipeline, not a
full SaaS product. I've listed every limitation openly further down.

---

## Table of contents

- [Why I built this](#why-i-built-this)
- [What the app does](#what-the-app-does)
- [The tech I used](#the-tech-i-used)
- [How the project is organized](#how-the-project-is-organized)
- [The CI/CD pipeline (the main part)](#the-cicd-pipeline-the-main-part)
- [What I actually did, step by step](#what-i-actually-did-step-by-step)
- [Run it on your machine](#run-it-on-your-machine)
- [Running with Docker](#running-with-docker)
- [Tests, code quality & security checks](#tests-code-quality--security-checks)
- [How deployment works](#how-deployment-works)
- [Secrets and environment variables](#secrets-and-environment-variables)
- [Screenshots](#screenshots)
- [What I learned](#what-i-learned)
- [Limitations (being honest)](#limitations-being-honest)
- [Future improvements](#future-improvements)
- [Deeper docs](#deeper-docs)
- [Resume bullet points](#resume-bullet-points)
- [License](#license)

---

## Why I built this

A lot of beginner projects stop at *"it runs on my laptop."* I wanted to show
the part that companies actually care about for a DevOps role: how you take a
normal app and get it **tested, scanned, packaged, published, and deployed
automatically**, so that every change goes through the same safe, repeatable
process instead of someone copying files by hand.

So I picked a tiny idea — a task tracker — and put a real engineering workflow
around it. The question I wanted the project to answer was:

> *"How do I take a simple Flask app and prepare it for real-world software
> delivery?"*

Every push to the repo runs quality checks, tests, and security scans. Every
merge to `main` builds a Docker image, pushes it to a registry, and deploys it.

---

## What the app does

TaskOps is a small internal-style task manager. You can:

- **See a homepage** that introduces the app and links to the task list.
- **View all tasks** in a dashboard, each showing its title, description,
  created date, and a **pending / completed** status pill.
- **Create a task** through a form, with proper **server-side validation**
  (title is required and length-limited, description is optional, empty or
  whitespace-only titles are rejected, and your input is kept if there's an
  error).
- **Mark a task as completed**, which updates its status and sends you back to
  the list.
- **Delete a task**, which removes it safely (deleting something that isn't
  there just does nothing instead of crashing).
- **Hit a `/health` endpoint** that returns JSON like
  `{"status":"ok","database":"ok"}` — used by Docker, the CI smoke test, and the
  deployment check. It returns `503` if the database check fails.

Under the hood I kept the code clean: the database logic lives in its own layer,
separate from the routes, and **every SQL query uses parameters** (no string
concatenation), so there's no SQL-injection risk. User content is rendered
through Jinja's auto-escaping, and I added a test that proves it's XSS-safe.

---

## The tech I used

| Area              | Choice                                               |
| ----------------- | ---------------------------------------------------- |
| Language          | Python 3.12                                          |
| Web framework     | Flask 3.1                                            |
| WSGI server       | gunicorn (2 workers, inside the container)           |
| Templating        | Jinja2 (auto-escaping on)                            |
| Database          | SQLite (Python's standard-library `sqlite3`)         |
| Styling           | Hand-written CSS (no framework)                      |
| Tests             | pytest (25 tests)                                    |
| Lint / format     | ruff, black, isort                                   |
| Security          | bandit (code), pip-audit (dependencies), Trivy (image)|
| Container         | Docker (`python:3.12-slim`) + Docker Compose         |
| Reverse proxy     | nginx (in production)                                |
| CI/CD             | GitHub Actions                                       |
| Registry          | GitHub Container Registry (ghcr.io)                  |

---

## How the project is organized

```text
taskops-cicd/
├── app/                        # the Flask application
│   ├── __init__.py             # app factory + logging + startup
│   ├── routes.py               # all the HTTP routes (thin handlers)
│   ├── database.py             # SQLite layer (parameterized queries only)
│   ├── config.py               # config read from environment variables
│   ├── templates/              # base, index, tasks, create_task (Jinja)
│   └── static/css/style.css    # hand-written styling
│
├── tests/                      # pytest suite (25 tests)
│   ├── conftest.py             # fixtures + throwaway test database
│   ├── test_routes.py          # pages, create/complete/delete, validation
│   ├── test_database.py        # CRUD on the data layer
│   ├── test_health.py          # /health ok + db-failure case
│   └── test_security.py        # XSS-escaping checks
│
├── scripts/                    # operations helpers
│   ├── deploy.sh               # pull image, run compose, wait for health
│   ├── rollback.sh             # roll back to the previous image tag
│   ├── backup_db.sh            # timestamped SQLite backup
│   └── smoke_test.sh           # check /health after a deploy
│
├── .github/workflows/
│   ├── ci.yml                  # runs on every push and pull request
│   └── cd.yml                  # runs only on push to main
│
├── docker/nginx.conf           # reverse proxy config (production)
├── docs/                       # architecture, ci-cd, deployment, security...
│
├── Dockerfile                  # non-root, healthchecked image
├── docker-compose.yml          # local dev stack
├── docker-compose.prod.yml     # production stack (app + nginx)
├── requirements.txt            # app dependencies
├── requirements-dev.txt        # dev/test/lint/security tools
├── Makefile                    # handy commands (make check, make clean...)
├── pyproject.toml              # tool config (ruff, black, isort, pytest)
├── .env.example                # template for environment variables
├── wsgi.py                     # entry point for gunicorn
├── LICENSE
└── README.md                   # you're reading it
```

---

## The CI/CD pipeline (the main part)

This is the heart of the project. Here's the whole flow from a `git push` to a
running app:

```text
Me
  │  git push
  ▼
GitHub repository  ──►  CI pipeline (every push / pull request)
  │                       ruff · black · isort · pytest · bandit · pip-audit
  │ merge to main          docker build · Trivy image scan · /health smoke test
  ▼
CD pipeline (only on main)
  │  re-run checks → docker build → Trivy scan → push image
  ▼
GitHub Container Registry  (ghcr.io/<me>/taskops:<commit-sha> + :latest)
  │  copy compose + nginx + scripts to the server, then run deploy.sh over SSH
  ▼
Linux server  ──►  docker compose -f docker-compose.prod.yml up -d
  ▼
nginx (port 80)  ──►  Flask / gunicorn (port 5000)  ──►  SQLite (data volume)
  ▼
post-deploy smoke test  ──►  http://<server>/health
```

### CI — `.github/workflows/ci.yml`

Runs on **every push (any branch)** and **every pull request**. It has two jobs:

1. **Quality & security gates** — checks formatting (`black`, `isort`), lints
   (`ruff`), runs the tests (`pytest`), scans the code (`bandit`), and audits
   the dependencies (`pip-audit`).
2. **Build & smoke-test the image** — builds the Docker image, scans it with
   **Trivy**, runs the container, and curls `/health` to make sure it really
   starts.

If any step fails, the whole run fails — so broken code, bad formatting, or a
security problem can't sneak through.

### CD — `.github/workflows/cd.yml`

Runs **only when code lands on `main`**. It:

1. **Verifies** the code again (lint, format, tests, bandit, pip-audit) so a bad
   commit is never deployed.
2. **Builds** the production image, **scans it with Trivy before publishing**,
   then **pushes** it to GitHub Container Registry tagged with both the commit
   SHA and `latest`.
3. **Deploys** by copying the compose file, nginx config, and scripts to the
   server over SSH, running `deploy.sh`, and finishing with a **health smoke
   test** against the live site.

There's a full walkthrough in [docs/ci-cd-pipeline.md](docs/ci-cd-pipeline.md).

---

## What I actually did, step by step

This is the order I built things in — basically the project's milestones.

### 1. Built the Flask app
I set up a clean Flask structure using the **application-factory pattern**, with
the routes, database layer, and config all separated. I added the homepage, the
task list, the create form, and the complete/delete actions, plus the `/health`
endpoint.

### 2. Added the database layer
I used SQLite with a small, reusable data-access module: a connection helper, an
init function that creates the schema, and CRUD functions. **Every query is
parameterized**, and the database logic never mixes with the route logic.

### 3. Wrote automated tests
I added a `pytest` suite (25 tests) covering page loads, task creation,
completion, deletion, validation of bad input, the database functions, the
`/health` endpoint (including the failure case), and an XSS-escaping check. Tests
run against a **separate throwaway database** so they never touch real data.

### 4. Added code-quality tools
I wired up **ruff** (linting), **black** (formatting), and **isort** (import
order), and configured them in `pyproject.toml`. I also added a `Makefile` so I
can run everything with one command.

### 5. Added security scanning
I added **bandit** to scan my Python code for security issues, **pip-audit** to
check my dependencies for known vulnerabilities, and later **Trivy** to scan the
built Docker image. I made sure no real secrets are in the repo — there's a
`.env.example` template and the real `.env` is git-ignored.

### 6. Containerized the app
I wrote a **Dockerfile** based on `python:3.12-slim` that runs as a **non-root
user**, has a **HEALTHCHECK**, caches the dependency layer, and serves the app
with gunicorn. I added a `docker-compose.yml` for local development and a
`docker-compose.prod.yml` that runs the app behind an **nginx reverse proxy**
with a persistent volume for the database.

### 7. Built the CI pipeline
I created `.github/workflows/ci.yml` so that every push and pull request runs the
full set of checks and builds/smoke-tests the Docker image. This is the gate
that keeps the main branch healthy.

### 8. Built the CD pipeline
I created `.github/workflows/cd.yml` so that merging to `main` re-verifies the
code, builds and scans the production image, pushes it to **GHCR**, and deploys
it to a Linux server over **SSH**, ending with a health check. I also wrote
**deploy**, **rollback**, **backup**, and **smoke-test** scripts to support
real operations.

### 9. Wrote the documentation
I wrote this README plus a `docs/` folder explaining the architecture, the
pipeline, deployment, security, and troubleshooting — so someone can understand
the project without even running it.

### 10. Cleaned it up for GitHub
I removed the local virtual environment and all cache files from the repo (they
should never be committed), made sure the scripts use Linux line endings and are
executable, and double-checked that all tests and checks pass on a clean copy.

---

## Run it on your machine

You'll need **Python 3.12**.

```bash
# 1. clone and enter the project
git clone https://github.com/<your-username>/taskops-cicd.git
cd taskops-cicd

# 2. create a virtual environment and install the dev tools
python -m venv .venv
source .venv/bin/activate          # macOS / Linux
# .venv\Scripts\Activate.ps1        # Windows PowerShell
pip install -r requirements-dev.txt

# 3. run the tests
python -m pytest                   # 25 tests should pass

# 4. start the dev server
python wsgi.py                     # http://127.0.0.1:5000
```

Quick check that it's alive:

```bash
curl http://127.0.0.1:5000/health   # {"status":"ok","database":"ok"}
```

> Note: gunicorn is a Linux server used inside the container. On Windows, just
> use the dev server (`python wsgi.py`) or run it through Docker.

---

## Running with Docker

Build and run the image directly:

```bash
docker build -t taskops:test .
docker run -p 5000:5000 -e FLASK_SECRET_KEY=test taskops:test
curl http://localhost:5000/health
```

Or use the local dev stack (builds the image, keeps the database in a volume):

```bash
docker compose up --build           # http://localhost:5000
```

The production stack runs the image behind nginx:

```bash
docker compose -f docker-compose.prod.yml config        # validate first
IMAGE=ghcr.io/<owner>/taskops IMAGE_TAG=latest FLASK_SECRET_KEY=... \
  docker compose -f docker-compose.prod.yml up -d        # nginx on :80
```

---

## Tests, code quality & security checks

Run everything by hand:

```bash
python -m pytest          # tests
ruff check .              # lint
black --check .           # format check
isort --check-only .      # import order check
bandit -r app             # code security scan
pip-audit -r requirements.txt   # dependency vulnerability audit
```

Or use the `Makefile`:

```bash
make install   # create .venv and install dev requirements (run this first)
make help      # list all targets
make check     # lint + format-check + test + security + audit, all at once
make clean     # remove caches and build artifacts before committing
```

> The `Makefile` targets use the project's `.venv/`, so run `make install` once
> before `make test` or `make check`.

---

## How deployment works

In production the app runs the published GHCR image **behind nginx** using
`docker-compose.prod.yml`: nginx listens on port 80 and proxies to the app
(gunicorn on 5000), with SQLite stored on a persistent volume.

The scripts in `scripts/` handle the operational side:

- **`deploy.sh`** — logs in to GHCR if needed, writes a locked-down (`0600`)
  `.env` for compose, pulls and starts the stack, waits for `/health` to go
  green, and records the previous image tag so a rollback is possible.
- **`rollback.sh`** — switches back to the previously recorded tag and
  re-deploys, with its own health check.
- **`backup_db.sh`** — makes a consistent, timestamped backup of the SQLite
  database (it uses SQLite's online backup while the app is running).
- **`smoke_test.sh`** — checks that `/health` returns `status: ok`, retrying a
  few times so it works right after a deploy.

The full guide is in [docs/deployment.md](docs/deployment.md).

---

## Secrets and environment variables

No real secrets live in the repo. Locally you copy `.env.example` to `.env`. In
GitHub Actions, the deploy uses repository **secrets**:

| Secret             | Required | What it's for                                       |
| ------------------ | -------- | --------------------------------------------------- |
| `GITHUB_TOKEN`     | auto     | Log in and push to GHCR (provided by Actions)       |
| `DEPLOY_HOST`      | yes      | Server hostname / IP                                |
| `DEPLOY_USER`      | yes      | SSH username                                        |
| `DEPLOY_SSH_KEY`   | yes      | Private SSH key                                     |
| `DEPLOY_PORT`      | yes      | SSH port (e.g. 22)                                  |
| `FLASK_SECRET_KEY` | yes      | Flask session key for the production container      |

The app reads these environment variables:

| Variable           | Used by        | Default              | Purpose                          |
| ------------------ | -------------- | -------------------- | -------------------------------- |
| `FLASK_SECRET_KEY` | app            | dev fallback (warns) | Flask session signing key        |
| `DATABASE_PATH`    | app            | `taskops.db`         | Where the SQLite file lives      |
| `MAX_TITLE_LENGTH` | app            | `120`                | Max task-title length            |
| `APP_PORT`         | dev compose    | `5000`               | Host port for the dev stack      |
| `IMAGE`/`IMAGE_TAG`| prod compose   | placeholder/`latest` | Which image to run in production |
| `HTTP_PORT`        | prod compose   | `80`                 | Public nginx port                |

> **Tip:** turn on **branch protection** for `main` (require a PR + passing CI)
> so CD only ever deploys code that passed the checks.

---

## Screenshots

I haven't faked any screenshots. Once the project is on GitHub and the pipeline
has run, I'll capture real ones and add them here. The
[`docs/screenshots/`](docs/screenshots/) folder lists exactly which screenshots
to add and what to name them. Example of how they'll be embedded:

```markdown
![Task dashboard](docs/screenshots/tasks.png)
![CI pipeline passing](docs/screenshots/ci-success.png)
```

---

## What I learned

- How a real **CI/CD pipeline** is wired together, and why each stage exists.
- The difference between **CI** (checking every change) and **CD** (deploying
  from main), and why deployment should only happen after the checks pass.
- How to **containerize** an app properly — non-root user, healthcheck, small
  base image, cached layers.
- How to publish images to a **container registry** and pull them on a server.
- How to **deploy over SSH** automatically and verify it worked with a health
  check, plus how to **roll back** when something goes wrong.
- How to keep **secrets** out of a repo and manage them with GitHub Secrets and
  environment variables.
- How **security scanning** fits into a pipeline (code, dependencies, and image).

---

## Limitations (being honest)

I'd rather be upfront about the scope than oversell it:

- The Flask app is **intentionally simple** — it's a vehicle for the pipeline.
- **No authentication or authorization** — all routes are public.
- **No CSRF protection** on the POST forms.
- **SQLite** is great for a demo but isn't meant for high concurrency or
  multiple app replicas.
- **No HTTPS by default** — nginx serves plain HTTP on port 80.
- The **CD pipeline needs a real, prepared server** (Docker, SSH, open port 80,
  secrets configured) — it's written and validated, but it can only be fully
  proven once it's pointed at actual infrastructure.

---

## Future improvements

- CSRF protection (e.g. **Flask-WTF**).
- User accounts / login and per-user task lists.
- **HTTPS** via Let's Encrypt / Caddy / Traefik.
- A **PostgreSQL** backend for multi-instance deployments.
- **Dependabot** for automatic dependency updates.
- Monitoring with **Prometheus + Grafana**, and rate limiting.
- Infrastructure as Code (**Terraform / Ansible**) to provision the server.

---

## Deeper docs

If you want more detail on any part, the `docs/` folder goes deeper:

- [docs/architecture.md](docs/architecture.md) — how the app, database, and
  request flow fit together.
- [docs/ci-cd-pipeline.md](docs/ci-cd-pipeline.md) — every CI and CD stage
  explained.
- [docs/deployment.md](docs/deployment.md) — server setup and the full deploy
  process.
- [docs/security.md](docs/security.md) — how secrets and scanning are handled.
- [docs/troubleshooting.md](docs/troubleshooting.md) — common problems and fixes.

---

## Resume bullet points

- Built a **production-style CI/CD pipeline** for a Flask application using
  GitHub Actions, Docker, and automated testing.
- Implemented quality gates including formatting checks, linting, unit tests,
  security scanning (bandit), dependency auditing (pip-audit), Docker image
  builds, and **Trivy image scanning**.
- Containerized a Flask + SQLite app with Docker and Docker Compose, including a
  production-style **nginx reverse proxy** setup.
- Automated Docker image publishing to **GitHub Container Registry** and
  deployment to a Linux server over **SSH**, with a post-deploy health check.
- Added deployment, rollback, backup, and smoke-test scripts plus full technical
  documentation for production-style operations.

---

## License

[MIT](LICENSE) © 2026 Mehran Bayat