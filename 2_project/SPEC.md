# Project 2 Task Description — KubeOps GitOps Kubernetes Platform

You are acting as a senior DevOps engineer, Kubernetes engineer, and portfolio project architect.

I want you to build a complete DevOps portfolio project called:

# KubeOps — GitOps-Based Kubernetes Deployment Platform

This project is for a junior DevOps / CI-CD / Cloud / Platform Engineering portfolio.

The goal is to demonstrate Kubernetes, Docker, Helm, GitHub Actions, GitOps, Argo CD, monitoring documentation, security basics, and operational troubleshooting.

Important:
Do NOT make the business application complicated.
The app should be intentionally simple.
The main focus is Kubernetes and DevOps operations.

Correct positioning:

> This is a production-style Kubernetes and GitOps portfolio project built around a simple containerized API.

Do NOT claim:

> This is a fully production-ready enterprise SaaS platform.

The project should be realistic, clean, and recruiter-friendly.

==================================================
CURRENT LOCAL ENVIRONMENT
=========================

My Windows laptop is ready for Kubernetes development.

Installed and verified:

* Docker Desktop
* kubectl
* kind
* Helm
* local kind cluster named `dev`
* current kubectl context: `kind-dev`

The cluster has one node:

* dev-control-plane

Do not reinstall Docker, kubectl, kind, or Helm.

Use my existing local kind cluster for Kubernetes testing.

==================================================
PROJECT SUMMARY
===============

Build a simple API application and deploy it to Kubernetes using:

* Docker
* Kubernetes manifests
* Helm chart
* GitHub Actions
* GitHub Container Registry
* Argo CD GitOps configuration
* Kubernetes health checks
* resource requests/limits
* ConfigMap
* Secret example
* Ingress
* operational scripts
* monitoring documentation
* security documentation
* troubleshooting documentation

The app can be a simple FastAPI service called **KubeNotes API**.

The app should expose:

```text
GET /health
GET /ready
GET /notes
POST /notes
GET /notes/{id}
PUT /notes/{id}
DELETE /notes/{id}
```

The app can use in-memory storage to keep the Kubernetes part simple.

Do not use a complex database at the beginning.

If needed, document that storage is in-memory and resets when the pod restarts.

This is acceptable because the project focus is Kubernetes/GitOps, not database design.

==================================================
TECH STACK
==========

Use this stack:

Application:

* Python 3.12
* FastAPI
* Uvicorn
* Pydantic
* pytest
* httpx
* ruff
* black
* isort
* bandit
* pip-audit

Container:

* Docker
* Docker Compose for local development
* non-root container user
* healthcheck

Kubernetes:

* kind local cluster
* kubectl
* namespace
* Deployment
* Service
* Ingress
* ConfigMap
* Secret example
* readinessProbe
* livenessProbe
* resource requests and limits
* securityContext

Helm:

* Helm chart
* values.yaml
* values-dev.yaml
* values-prod.yaml
* configurable image repository
* configurable image tag
* configurable replicas
* configurable ingress host
* configurable resources

GitOps:

* Argo CD Application manifest
* manual sync instructions
* optional automated sync documented
* rollback documentation

CI/CD:

* GitHub Actions
* tests
* linting
* formatting check
* security scanning
* Docker build
* Trivy image scan
* push to GHCR

Monitoring:

* /health and /ready endpoints
* Kubernetes probes
* kubectl logs documentation
* Prometheus/Grafana documentation
* optional future /metrics endpoint

==================================================
REPOSITORY STRUCTURE
====================

Create this structure:

```text
kubeops-gitops/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   └── settings.py
│
├── tests/
│   ├── test_health.py
│   ├── test_notes.py
│   └── test_validation.py
│
├── k8s/
│   ├── namespace.yaml
│   ├── configmap.yaml
│   ├── secret.example.yaml
│   ├── deployment.yaml
│   ├── service.yaml
│   └── ingress.yaml
│
├── helm/
│   └── kubeops/
│       ├── Chart.yaml
│       ├── values.yaml
│       ├── values-dev.yaml
│       ├── values-prod.yaml
│       └── templates/
│           ├── _helpers.tpl
│           ├── deployment.yaml
│           ├── service.yaml
│           ├── ingress.yaml
│           ├── configmap.yaml
│           ├── secret.yaml
│           └── serviceaccount.yaml
│
├── argocd/
│   └── application.yaml
│
├── monitoring/
│   ├── README.md
│   └── grafana-dashboard-notes.md
│
├── scripts/
│   ├── check-tools.ps1
│   ├── create-kind-cluster.ps1
│   ├── deploy-k8s.ps1
│   ├── deploy-helm.ps1
│   ├── check-health.ps1
│   ├── port-forward.ps1
│   └── cleanup.ps1
│
├── docs/
│   ├── architecture.md
│   ├── kubernetes.md
│   ├── helm.md
│   ├── gitops.md
│   ├── monitoring.md
│   ├── security.md
│   └── troubleshooting.md
│
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── image-release.yml
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── requirements-dev.txt
├── pyproject.toml
├── Makefile
├── .gitignore
├── .dockerignore
├── .env.example
├── LICENSE
└── README.md
```

Because I am on Windows, include PowerShell scripts in `scripts/`.

If you also want to add Bash scripts, that is okay, but PowerShell scripts are more important for my current environment.

==================================================
APPLICATION REQUIREMENTS
========================

Build a FastAPI app.

Endpoints:

1. Health endpoint

```text
GET /health
```

Response:

```json
{
  "status": "ok"
}
```

2. Readiness endpoint

```text
GET /ready
```

Response:

```json
{
  "status": "ready"
}
```

3. List notes

```text
GET /notes
```

Response example:

```json
[
  {
    "id": 1,
    "title": "First note",
    "content": "Example content"
  }
]
```

4. Create note

```text
POST /notes
```

Input:

```json
{
  "title": "My note",
  "content": "Some content"
}
```

Validation:

* title is required
* title cannot be empty
* title max length 100
* content max length 1000

5. Get note by ID

```text
GET /notes/{id}
```

Return 404 if not found.

6. Update note

```text
PUT /notes/{id}
```

Return 404 if not found.

7. Delete note

```text
DELETE /notes/{id}
```

Return success or 404 if not found.

Keep storage simple:

* in-memory Python dictionary/list
* thread-safe enough for demo if simple
* document that data resets on restart

Application must:

* log to stdout
* read config from environment variables
* not require a database
* be easy to test

==================================================
TEST REQUIREMENTS
=================

Use pytest.

Tests should cover:

* `/health`
* `/ready`
* list notes initially empty
* create note
* create note with empty title rejected
* create note with too long title rejected
* create note with too long content rejected
* get existing note
* get missing note returns 404
* update existing note
* update missing note returns 404
* delete existing note
* delete missing note returns 404

Run:

```bash
python -m pytest
```

All tests must pass.

==================================================
PYTHON QUALITY REQUIREMENTS
===========================

Add:

* ruff
* black
* isort
* bandit
* pip-audit

Create `pyproject.toml`.

Commands should work:

```bash
python -m pytest
ruff check .
black --check .
isort --check-only .
bandit -r app
pip-audit -r requirements.txt
```

If formatting is needed:

```bash
black .
isort .
```

==================================================
DOCKER REQUIREMENTS
===================

Create a production-style Dockerfile.

Dockerfile should:

* use `python:3.12-slim`
* install only production dependencies from `requirements.txt`
* copy app code
* use non-root user
* expose port 8000
* run uvicorn
* include healthcheck if reasonable
* not copy `.venv`, cache files, `.env`, `.git`, tests, or docs unless needed

Container command should run something like:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Create `.dockerignore`.

It should ignore:

```text
.venv
venv
env
.git
.github
__pycache__
*.pyc
.pytest_cache
.ruff_cache
.mypy_cache
.coverage
htmlcov
.env
*.log
docs/screenshots
```

Create `docker-compose.yml` for local development.

It should allow:

```bash
docker compose up --build
```

and expose:

```text
http://localhost:8000/health
```

==================================================
KUBERNETES RAW YAML REQUIREMENTS
================================

Create raw Kubernetes manifests in `k8s/`.

Namespace:

```text
kubeops-dev
```

Deployment:

* app name: kubeops
* replicas: 2
* image configurable but default to local/demo image
* container port: 8000
* livenessProbe: `/health`
* readinessProbe: `/ready`
* resource requests and limits
* securityContext
* env from ConfigMap
* secret from Secret

Service:

* ClusterIP
* service port 80
* targetPort 8000

Ingress:

* host: `kubeops.local`
* path `/`
* service kubeops
* port 80

ConfigMap:

* APP_ENV
* LOG_LEVEL

Secret example:

* APP_SECRET_KEY placeholder
* must be an example only
* no real secrets

SecurityContext:
Use safe defaults where possible:

```yaml
runAsNonRoot: true
runAsUser: 1000
allowPrivilegeEscalation: false
```

If `readOnlyRootFilesystem` works, include it.
If not, document why.

==================================================
HELM REQUIREMENTS
=================

Create a Helm chart at:

```text
helm/kubeops/
```

Chart should support:

* configurable replica count
* configurable image repository
* configurable image tag
* configurable pull policy
* configurable service port
* configurable ingress host
* configurable resources
* configurable environment variables
* configurable secret values or secret name
* probes
* securityContext

Files:

```text
Chart.yaml
values.yaml
values-dev.yaml
values-prod.yaml
templates/deployment.yaml
templates/service.yaml
templates/ingress.yaml
templates/configmap.yaml
templates/secret.yaml
templates/serviceaccount.yaml
templates/_helpers.tpl
```

Add Helm commands to README:

```bash
helm lint ./helm/kubeops
helm template kubeops ./helm/kubeops -f helm/kubeops/values-dev.yaml
helm install kubeops ./helm/kubeops -n kubeops-dev --create-namespace -f helm/kubeops/values-dev.yaml
helm upgrade kubeops ./helm/kubeops -n kubeops-dev -f helm/kubeops/values-dev.yaml
helm uninstall kubeops -n kubeops-dev
```

==================================================
ARGO CD REQUIREMENTS
====================

Create:

```text
argocd/application.yaml
```

It should define an Argo CD Application that deploys the Helm chart from this GitHub repository.

Use placeholder repo URL:

```text
https://github.com/YOUR_USERNAME/kubeops-gitops.git
```

Document clearly that the user must replace this with the real repo URL.

Application should target:

* namespace: kubeops-dev
* path: helm/kubeops
* targetRevision: main
* destination server: https://kubernetes.default.svc

Sync policy:
Use manual sync by default or automated sync with comments.

Recommended:
Manual sync by default for safety.
Document how to enable automated sync later.

Do not install Argo CD automatically in this project yet.
Only provide manifests and docs.

==================================================
GITHUB ACTIONS REQUIREMENTS
===========================

Create CI workflow:

```text
.github/workflows/ci.yml
```

Runs on:

* push
* pull_request

Steps:

* checkout
* setup Python 3.12
* install dev dependencies
* ruff check
* black --check
* isort --check-only
* pytest
* bandit
* pip-audit
* Docker build
* Trivy image scan

Create image release workflow:

```text
.github/workflows/image-release.yml
```

Runs on:

* push to main
* optionally workflow_dispatch

Steps:

* checkout
* login to GHCR
* build Docker image
* tag image with latest and commit SHA
* push image to GHCR
* scan pushed/built image with Trivy

Use:

```yaml
permissions:
  contents: read
  packages: write
```

Use image format:

```text
ghcr.io/${{ github.repository_owner }}/kubeops
```

Make sure image name is lowercase if needed.

Do not fake deployment to a cloud cluster.
This project uses GitOps/Argo CD for deployment.

==================================================
SCRIPT REQUIREMENTS
===================

Create PowerShell scripts.

1. `scripts/check-tools.ps1`

Checks:

```powershell
docker --version
docker ps
kubectl version --client
kind version
helm version
kubectl config current-context
kubectl get nodes
```

2. `scripts/create-kind-cluster.ps1`

Should:

* check if kind cluster `dev` already exists
* create it if missing
* set context
* show nodes

3. `scripts/deploy-k8s.ps1`

Should:

* apply raw Kubernetes manifests from `k8s/`
* show pods, svc, ingress

4. `scripts/deploy-helm.ps1`

Should:

* run helm lint
* install or upgrade chart
* show pods and service

5. `scripts/check-health.ps1`

Should:

* port-forward service
* curl or Invoke-WebRequest `/health`
* show clear success/failure

6. `scripts/port-forward.ps1`

Should:

* port-forward service/kubeops to localhost

7. `scripts/cleanup.ps1`

Should:

* uninstall Helm release if exists
* delete raw resources if needed
* optionally delete namespace
* do not delete the kind cluster unless clearly requested

Scripts must be safe and beginner-friendly.

==================================================
DOCUMENTATION REQUIREMENTS
==========================

Create strong documentation.

README.md should include:

* project title
* badges
* project overview
* why this project exists
* architecture diagram
* tech stack
* app endpoints
* local Python setup
* Docker setup
* Kubernetes setup
* raw YAML deployment
* Helm deployment
* Argo CD GitOps setup
* CI/CD explanation
* monitoring section
* security section
* troubleshooting link
* limitations
* future improvements
* resume bullet points

Docs:

1. `docs/architecture.md`

Explain:

* app architecture
* Docker flow
* Kubernetes flow
* Helm flow
* GitOps flow

2. `docs/kubernetes.md`

Explain:

* namespace
* deployment
* service
* ingress
* configmap
* secret
* probes
* resources
* useful kubectl commands

3. `docs/helm.md`

Explain:

* chart structure
* values files
* install
* upgrade
* rollback
* uninstall

4. `docs/gitops.md`

Explain:

* what GitOps means
* how Argo CD watches Git
* how to install Argo CD later
* how to apply application manifest
* how to sync
* how to rollback
* manual vs automated sync

5. `docs/monitoring.md`

Explain:

* `/health`
* `/ready`
* Kubernetes probes
* kubectl logs
* kubectl describe
* kubectl get events
* Prometheus/Grafana as future/optional
* what screenshots to add later

6. `docs/security.md`

Explain implemented security:

* no committed secrets
* secret.example.yaml
* non-root Docker user
* Kubernetes securityContext
* resource limits
* Bandit
* pip-audit
* Trivy
* GitHub Secrets/GHCR

Explain limitations:

* no authentication
* in-memory data
* local kind cluster is not real cloud production
* no HTTPS by default
* no external secrets operator
* no network policies initially

7. `docs/troubleshooting.md`

Include fixes for:

* Docker not running
* kind cluster missing
* kubectl context wrong
* ImagePullBackOff
* CrashLoopBackOff
* pod not Ready
* service not reachable
* port-forward fails
* ingress not working
* Helm install fails
* Argo CD OutOfSync
* GHCR image pull problems

==================================================
README LIMITATIONS SECTION
==========================

Include honest limitations:

```text
The API is intentionally simple.
Data is stored in memory and resets on pod restart.
The project focuses on Kubernetes/GitOps, not application complexity.
The local kind cluster is not the same as managed cloud Kubernetes.
No authentication is implemented.
No HTTPS is configured by default.
Argo CD manifests are provided, but Argo CD installation is done later.
Monitoring is documented at a basic level and can be expanded.
```

==================================================
FUTURE IMPROVEMENTS
===================

Add future improvements:

```text
Add PostgreSQL with StatefulSet or external managed database.
Add persistent storage.
Add Prometheus metrics endpoint.
Add Grafana dashboard JSON.
Add Argo CD Image Updater.
Add cert-manager for HTTPS.
Add External Secrets Operator.
Add Horizontal Pod Autoscaler.
Add NetworkPolicies.
Add Terraform for cloud Kubernetes.
Add Loki for logs.
Add Cosign image signing.
Add Dependabot.
Add Kubernetes policy checks with kube-score or kube-linter.
```

==================================================
RESUME BULLET POINTS
====================

Add these to README:

```text
Built a GitOps-based Kubernetes deployment platform for a containerized FastAPI application using Docker, Helm, Argo CD manifests, and GitHub Actions.

Created Kubernetes manifests and Helm charts with configurable image tags, environment variables, health probes, resource limits, ConfigMaps, Secrets, Services, and Ingress.

Implemented CI workflows for testing, linting, formatting checks, Python security scanning, Docker image building, Trivy image scanning, and GHCR image publishing.

Documented Kubernetes operations including local kind setup, Helm deployment, GitOps synchronization, health checks, logs, troubleshooting, security practices, and future production improvements.
```

==================================================
ACCEPTANCE CRITERIA
===================

The project is complete only when:

Application:

* app runs locally
* tests pass
* health endpoint works
* ready endpoint works
* CRUD endpoints work

Docker:

* Docker image builds
* container runs
* `/health` works in container
* non-root user is used
* `.dockerignore` is clean

Kubernetes:

* raw YAML deploys to kind
* pods become Running
* pods become Ready
* service works through port-forward
* livenessProbe and readinessProbe are configured
* resources are configured

Helm:

* helm lint passes
* helm template works
* helm install works
* helm upgrade works
* helm uninstall works

CI/CD:

* GitHub Actions CI is defined
* image-release workflow is defined
* GHCR image push workflow is defined
* Trivy scan is included

Docs:

* README is complete and honest
* docs folder is complete
* limitations are clear
* no fake screenshots

==================================================
FINAL COMMANDS TO RUN LOCALLY
=============================

After building the project, run these checks:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
python -m pytest
ruff check .
black --check .
isort --check-only .
bandit -r app
pip-audit -r requirements.txt
docker build -t kubeops:local .
docker run -d --name kubeops-test -p 8000:8000 kubeops:local
curl http://localhost:8000/health
docker rm -f kubeops-test
helm lint ./helm/kubeops
helm template kubeops ./helm/kubeops -f helm/kubeops/values-dev.yaml
kubectl get nodes
```

Then deploy to Kubernetes using raw YAML:

```powershell
kubectl apply -f k8s/
kubectl get pods -n kubeops-dev
kubectl port-forward svc/kubeops 8000:80 -n kubeops-dev
curl http://localhost:8000/health
```

Then deploy with Helm:

```powershell
kubectl delete namespace kubeops-dev
helm install kubeops ./helm/kubeops -n kubeops-dev --create-namespace -f helm/kubeops/values-dev.yaml
kubectl get pods -n kubeops-dev
kubectl port-forward svc/kubeops 8000:80 -n kubeops-dev
curl http://localhost:8000/health
```

==================================================
FINAL REPORT
============

At the end, give me a final report with:

1. Project summary
2. Files created
3. How to run locally
4. How to run Docker
5. How to deploy raw Kubernetes YAML
6. How to deploy with Helm
7. How GitHub Actions works
8. How Argo CD will be used later
9. Tests/checks run and results
10. Bugs or limitations
11. What I should do next
12. Final score out of 10 as a junior DevOps/Kubernetes portfolio project

Be strict and honest.
Do not fake test results, Docker results, Kubernetes results, screenshots, or GitHub Actions results.
