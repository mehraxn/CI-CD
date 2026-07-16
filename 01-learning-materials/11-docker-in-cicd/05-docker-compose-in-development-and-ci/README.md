# Docker Compose in Development and CI

Compose defines a project of services, images/builds, ports, networks, volumes, environment, dependencies, restart rules, and health checks. Bind mounts expose host paths; named volumes persist runtime data. `.env`, environment files, overrides, profiles, and project names change configuration and isolation.

```text
Build services → start stack → wait for health → test → collect failure logs → remove volumes/orphans
```

`depends_on` ordering alone is not readiness. Health conditions help, while applications still need retries. CI stacks require unique project names, deterministic cleanup, logs on failure, and removal of orphan containers. Compose improves local parity but is not Kubernetes and lacks its controllers/policies.

TaskOps dev Compose builds one app and persists SQLite; production Compose pulls a published image, adds nginx, waits on app health, and uses a named data volume. KubeOps Compose runs the local API. Project 3 Compose runs application, Prometheus, and Grafana.

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
