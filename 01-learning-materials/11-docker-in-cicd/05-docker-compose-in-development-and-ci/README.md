# Docker Compose in Development and CI

Compose defines a project of services, images/builds, ports, networks, volumes, environment, dependencies, restart rules, and health checks. Bind mounts expose host paths; named volumes persist runtime data. `.env`, environment files, overrides, profiles, and project names change configuration and isolation.

```text
Build services → start stack → wait for health → test → collect failure logs → remove volumes/orphans
```

`depends_on` ordering alone is not readiness. Health conditions help, while applications still need retries. CI stacks require unique project names, deterministic cleanup, logs on failure, and removal of orphan containers. Compose improves local parity but is not Kubernetes and lacks its controllers/policies.

TaskOps dev Compose builds one app and persists SQLite; production Compose pulls a published image, adds nginx, waits on app health, and uses a named data volume. KubeOps Compose runs the local API. Project 3 Compose runs application, Prometheus, and Grafana.

## Compose Building Blocks

A Compose project groups resources under one project name. Each service describes an image to pull or build, ports, environment, storage, dependencies, restart behavior, and health. Compose creates a default network so services can resolve each other by service name. Explicit networks can separate traffic.

A port mapping publishes a host port to a container port. A bind mount exposes a host path and may hide files already in the image. A named volume is runtime-managed and survives container replacement until removed. Restart policies do not prove readiness or correctness. Compose interpolates values from the shell and project `.env`; `env_file` supplies container variables. Neither is automatically a secret store. Override files merge settings, profiles conditionally enable services, and project names isolate resources. Operators must know which inputs are active.

## Educational Stack

This is conceptual; `example` credentials are placeholders, never production secrets:

```yaml
services:
  app:
    build:
      context: .
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgres://app:example@database:5432/app
    depends_on:
      database:
        condition: service_healthy
  database:
    image: postgres:16
    environment:
      POSTGRES_USER: app
      POSTGRES_PASSWORD: example
      POSTGRES_DB: app
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app"]
      interval: 5s
      timeout: 3s
      retries: 10
```

The app reaches `database` through the project network. A health condition is stronger than creation order, but it is not complete readiness for every operation. Applications still need retry behavior and tests should poll meaningful functionality. Plain `depends_on` only orders startup.

```text
Application service
      | project network
Database service
      |
Shared test stack
```

## CI Integration Flow

```text
Build services
    | start stack
Wait for health
    | run integration and smoke tests
Collect failure logs
    | destroy stack, volumes, and orphans
```

Parallel jobs need unique project names and non-colliding host ports. Cleanup should run after failure. Persisted test data can make later results misleading, so test volumes are normally removed. Capture logs and exit codes before teardown. Bind mounts can undermine image testing by replacing packaged files with a checkout. Production Compose can suit a small host but lacks Kubernetes scheduling, policy, and reconciliation.

## Repository Evidence

TaskOps [development Compose](../../../Projects/1_project/taskops-cicd/docker-compose.yml) builds one app, names it `taskops:latest`, publishes a configurable port, injects environment, persists `/data`, and repeats its health check. [Production Compose](../../../Projects/1_project/taskops-cicd/docker-compose.prod.yml) pulls a configurable GHCR image, exposes the app only to nginx, requires `FLASK_SECRET_KEY`, waits for app health, and persists SQLite.

KubeOps [Compose](../../../Projects/2_project/kubeops-gitops/docker-compose.yml) builds one API and injects `APP_ENV` and `LOG_LEVEL`; it has no volume or Compose health check. [Project 3](../../../Projects/3_project/docker-compose.yml) builds the app and pulls versioned Prometheus and Grafana images. It bind-mounts Prometheus configuration, persists Grafana data, and uses list-form dependencies that provide order only. No repository workflow invokes `docker compose`, so Compose-based CI integration is conceptual.

Common mistakes are leaked stacks, fixed project names, shared ports, committed secrets, readiness assumptions, stale volumes, missing failure logs, orphan services, and mounts that hide image content. Local and production definitions should share intentional concepts without pretending the environments are identical.

## Operational Review

Render the effective Compose configuration conceptually from base files, overrides, shell variables, `.env`, and profiles. For each service, record image/build source, command, ports, health, networks, storage, configuration, dependency conditions, and restart policy. Separate placeholders from protected values and local convenience from production intent.

For CI, assign a unique project name, avoid fixed ports where possible, wait on behavior rather than sleep, collect logs before teardown, and remove volumes/orphans in an always-run cleanup step. Verify that bind mounts do not hide packaged image content. A repeat run should start without stale state. These checks distinguish a repeatable integration stack from a developer machine that happens to work.

## Configuration Precedence and Parity

Effective Compose behavior can differ from the visible base file because shell variables, `.env`, environment files, overrides, profiles, and command-line selection combine. Document precedence and render the effective model in real work before relying on it. Never assume a value came from the file currently open.

Parity means preserving important interfaces—image, ports, service names, configuration contracts, health semantics, and dependency versions—not copying production credentials or infrastructure onto laptops. CI should resemble the integration boundary it validates while remaining isolated and disposable. Production differences such as TLS, managed databases, scheduling, and secret providers should be explicit.

Troubleshooting begins by identifying the service that first became unhealthy, its resolved configuration, network name, mounted paths, and logs. A downstream connection error may be readiness, DNS, credentials, or schema state; blindly adding `depends_on` will not solve all four.

## Practical Exercise

Map services, ports, networks, volumes, health dependencies, configuration, and cleanup needs in one real Compose file.

## Knowledge Check

1. Does `depends_on` prove ready? 2. Bind versus named volume? 3. Why project names in CI? 4. Compose versus Kubernetes?

<details><summary>Answers</summary>

1. No. 2. Host path versus runtime-managed storage. 3. Isolation. 4. Compose runs related containers; Kubernetes continuously reconciles cluster resources.

</details>

## Navigation
- [Back to Docker in CI/CD](../README.md)
- [Previous: Image Tagging, Versioning, and Metadata](../04-image-tagging-versioning-and-metadata/)
- [Next: Container Testing, Health Checks, and Scanning](../06-container-testing-health-checks-and-scanning/)
- [Back to All Learning Materials](../../README.md)
