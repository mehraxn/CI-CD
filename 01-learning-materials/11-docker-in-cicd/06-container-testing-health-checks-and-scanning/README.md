# Container Testing, Health Checks, and Scanning

Test the image, not only source: build, start, wait, smoke/integration test, collect logs, and clean up even after failure. Docker `HEALTHCHECK` informs the container runtime; Kubernetes readiness controls traffic and is a different system.

Image scanners inspect OS/package vulnerability databases and sometimes secrets/misconfiguration. Results depend on database freshness, package visibility, severity policy, ignored/unfixed findings, and false positives/negatives. A clean scan is not proof of security; combine dependency, source, runtime, provenance, and configuration controls.

TaskOps CI builds with Buildx, loads locally, Trivy-scans before running `/health`, then removes the container with `if: always()`. TaskOps CD scans before publishing. KubeOps CI scans local; image-release pushes then scans, so a failing image can already exist in GHCR.

## Practical Exercise

Classify repository checks as build, smoke, Docker health, Kubernetes liveness/readiness, scan, and post-deploy verification. Note timing and failure behavior.

## Knowledge Check

1. Why test built image? 2. Clean scan means secure? 3. Why always cleanup? 4. Gate-placement contrast?

<details><summary>Answers</summary>

1. Packaging/runtime can fail. 2. No. 3. Prevent leaked resources. 4. TaskOps scans before push; KubeOps release scans after push.

</details>

## Navigation
- [Back to Docker in CI/CD](../README.md)
- [Previous: Docker Compose in Development and CI](../05-docker-compose-in-development-and-ci/)
- [Next: Publishing Images and Registry Workflows](../07-publishing-images-and-registry-workflows/)
- [Back to All Learning Materials](../../README.md)
