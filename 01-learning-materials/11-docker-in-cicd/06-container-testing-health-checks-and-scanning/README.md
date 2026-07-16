# Container Testing, Health Checks, and Scanning

Test the image, not only source: build, start, wait, smoke/integration test, collect logs, and clean up even after failure. Docker `HEALTHCHECK` informs the container runtime; Kubernetes readiness controls traffic and is a different system.

Image scanners inspect OS/package vulnerability databases and sometimes secrets/misconfiguration. Results depend on database freshness, package visibility, severity policy, ignored/unfixed findings, and false positives/negatives. A clean scan is not proof of security; combine dependency, source, runtime, provenance, and configuration controls.

TaskOps CI builds with Buildx, loads locally, Trivy-scans before running `/health`, then removes the container with `if: always()`. TaskOps CD scans before publishing. KubeOps CI scans local; image-release pushes then scans, so a failing image can already exist in GHCR.

## Testing the Packaged Result

Source tests cannot detect every packaging error. A build test proves that the Dockerfile and context can produce an image. Configuration inspection can check user, command, labels, ports, and environment defaults. A runtime smoke test starts the image and exercises a small critical behavior. Integration tests may add real dependencies. Exit codes must make failure visible, and logs should be collected before cleanup.

```text
Build image
    | inspect configuration
Start container
    | wait for health
Run smoke tests
    | scan image
Publish only when accepted
```

A health endpoint should be inexpensive and meaningful. A Docker `HEALTHCHECK` reports container-level status to Docker. Kubernetes readiness controls whether a Pod receives Service traffic; liveness may trigger restarts; startup delays the other probes for slow initialization. A smoke test actively checks an expected behavior from a client perspective. These mechanisms overlap in endpoints but serve different control systems.

Image history and inspection can expose unexpected commands, environment defaults, user selection, and layer size. Configuration tests can enforce non-root execution or a declared health check. Image size is useful evidence of accidental content, but size alone does not measure security.

## Scanning Scope and Policy

Vulnerability scanners correlate detected operating-system packages and language dependencies with advisory databases. Filesystem, secret, and misconfiguration scanning are related modes, not necessarily included in an image-vulnerability invocation. An SBOM lists components and can improve inventory; it does not itself prove safety. Runtime protection addresses behavior after startup and cannot be replaced by build-time scanning.

Results depend on database freshness, package detection, severity scoring, base-image contents, and available fixes. False positives and false negatives occur. `ignore-unfixed` reduces noise from findings without an available patch but also accepts known exposure. A severity threshold expresses risk policy, not universal truth. Teams need ownership, exceptions with expiry, base refresh, and evidence retention. A clean report is never proof of security.

A blocking gate fails the pipeline when policy is breached. A non-blocking report preserves visibility while allowing progress. Placement matters: scanning before push prevents a rejected image from being published, while scanning after push can evaluate the registry copy but may leave rejected content present. Signing, provenance, SBOM publication, capabilities testing, and read-only-runtime tests are useful conceptual controls but are not implemented by these workflows.

## Repository Evidence

TaskOps [CI](../../../Projects/1_project/taskops-cicd/.github/workflows/ci.yml) builds with Buildx, loads `taskops:ci`, and runs Trivy with `HIGH,CRITICAL`, `exit-code: "1"`, and `ignore-unfixed: true`. It then starts the container, retries `/health`, prints logs on failure, and removes the container under `if: always()`. Its [Dockerfile](../../../Projects/1_project/taskops-cicd/Dockerfile) also defines a Python-based health check and non-root user. TaskOps [CD](../../../Projects/1_project/taskops-cicd/.github/workflows/cd.yml) scans the SHA-tagged local image before either tag is pushed and performs a post-deployment smoke test.

KubeOps [CI](../../../Projects/2_project/kubeops-gitops/.github/workflows/ci.yml) builds `kubeops:ci` and applies the same blocking Trivy policy, but it does not start or smoke-test the image. Its [image-release workflow](../../../Projects/2_project/kubeops-gitops/.github/workflows/image-release.yml) pushes SHA and `latest` before scanning the pushed SHA. Thus a scan failure happens after publication. The [Kubernetes Deployment](../../../Projects/2_project/kubeops-gitops/k8s/deployment.yaml) separately defines liveness `/health`, readiness `/ready`, non-root execution, and a read-only root filesystem. No startup probe exists.

Common failures include testing only source, fixed sleeps instead of polling, no logs, cleanup that runs only on success, confusing Docker health with Kubernetes readiness, stale vulnerability databases, unexplained exceptions, and treating one scanner as full security coverage.

## Gate Design and Triage

Define what each gate proves: build success proves packaging syntax and inputs; inspection proves selected metadata; runtime smoke tests prove a narrow behavior; vulnerability scans compare detectable components with current advisories. None proves the others. Record image digest, scanner/database version, policy, ignored findings, test endpoint, exit result, and retained logs so a decision can be reproduced.

When a health check fails, inspect startup logs, process exit, port binding, configuration, timing, and dependency readiness before increasing delays. When a scan fails, identify component origin, fix availability, reachability context, and approved exception process. Refreshing a base may fix OS findings but can also change behavior and must be rebuilt and retested. Exceptions should have owner and expiry.

Additional hardening questions include non-root identity, unexpected capabilities, writable filesystem needs, embedded secrets, SBOM completeness, and signature/provenance verification. These are defense layers; no single green check establishes security.

## Acceptance Matrix

Write an acceptance matrix with check, subject, evidence, failure action, owner, and expiry for exceptions. Source dependency audit, image vulnerability scan, configuration inspection, runtime smoke test, and post-deploy verification inspect different subjects. Running all under one “security” label hides gaps.

Scan findings should link to the precise image digest. Rebuilding a tag after remediation produces different content and requires a new decision. Database updates can change results for unchanged images; retain the database/version timestamp when auditability matters. If `ignore-unfixed` is used, schedule base refresh and reassessment rather than forgetting accepted findings.

Health endpoints should expose no secrets and avoid destructive work. Test both expected success and clean failure behavior, including termination signals and non-root permissions. Cleanup failure is itself a test-infrastructure defect because it contaminates later jobs.

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
