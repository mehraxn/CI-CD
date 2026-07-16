# Container, Kubernetes, and IaC Security Scanning

## Scanning What You Ship and What You Declare

Application code is one scan target; the *packaging and platform* around it are others. Container images carry an operating system's worth of packages; Kubernetes manifests declare privilege and exposure; Terraform declares networks, storage, and encryption. Each layer has its own misconfiguration classes and its own scanners:

| Scan target | Example findings |
|-------------|------------------|
| Container image | Vulnerable OS package or dependency |
| Dockerfile | Root user or unsafe instruction |
| Kubernetes manifest | Privileged Pod or missing controls |
| Terraform | Public network or missing encryption |
| Repository filesystem | Dependencies, secrets, or configuration issues |

## Container-Image Scanning

An image scan inventories the image's contents — **OS packages** (from the base image) and **language dependencies** (installed by your Dockerfile) — and matches them against vulnerability databases. **Base-image risk** dominates in practice: most findings come from the `FROM` line, which is why slim bases and regular rebuilds matter more than any scanner setting. Scanners also check **image configuration**: running as **root**, exposed **secrets in image history or layers**, and (via adjacent tools) runtime posture like **privileged containers**, **Docker socket exposure**, added **Linux capabilities**, and missing **read-only root filesystems**.

**Trivy** — the repository's real scanner — supports several modes:

```text
Image scan
Filesystem scan
Repository scan
Configuration scan
SBOM scan
```

Actual behavior depends entirely on workflow configuration; this repository uses image scanning only. Conceptual invocations:

```bash
trivy image example/application:sha-a1b2c3d
```

```bash
trivy config .
```

## Kubernetes and IaC Misconfiguration

Kubernetes scanners (Trivy's config mode, Kubescape, kube-linter — none configured here) flag **privileged Pods**, **host networking/paths**, missing **resource limits**, insecure **security contexts**, and **plaintext Secrets in manifests**. IaC scanners (Checkov, tfsec — also absent) flag Terraform patterns: **public storage**, **open network rules** (`0.0.0.0/0` where it shouldn't be), missing **encryption**, **logging**, or **backup**. All are policy engines at heart: rules, **severities**, **ignore rules**, and inevitable **false positives** — a "public bucket" finding is correct behavior for a website's assets, which is why ignores must be narrow, justified, and reviewed, and **blocking thresholds** deliberate.

## Scanner Limitations

- Results depend on scanner version and database freshness — yesterday's clean scan can fail today with zero changes.
- Misconfiguration checks cannot understand every architecture decision.
- A fixed package may not yet exist (this repository's `ignore-unfixed: true` is precisely that risk decision, made explicit).
- Severity does not equal project-specific risk.
- A clean scan does not prove runtime security.
- Scanning does not replace secure base images or runtime controls — it observes; it does not harden.

## Common Mistakes

- Scanning only after deployment.
- Scanning an image tag different from the deployed artifact.
- Ignoring scanner exit codes.
- Broad ignore files nobody reviews.
- No owner for findings.
- Never rebuilding when the base image updates — the scan told you; nobody rebuilt.
- Treating private images as trusted.
- Scanning source but never the built image (or vice versa).
- Security threshold changed merely to pass CI.
- Reports not retained for release evidence.

## Existing Repository Evidence

Trivy image scanning is the repository's most consistently applied gate — four workflows, all blocking, all pinned to `aquasecurity/trivy-action@0.28.0`, all `severity: HIGH,CRITICAL` with `exit-code: "1"` and `ignore-unfixed: true`:

- [TaskOps CI](../../../Projects/1_project/taskops-cicd/.github/workflows/ci.yml) scans the locally built `taskops:ci` image before the smoke test — and its Dockerfile comment shows scan-aware *design*: the health probe uses Python's stdlib "so the image needs no apt packages at all (smaller and fewer CVEs for Trivy to flag)".
- [TaskOps CD](../../../Projects/1_project/taskops-cicd/.github/workflows/cd.yml) builds with `push: false`, scans, and **only then pushes** — the scan-before-publish placement this lesson recommends.
- [KubeOps image release](../../../Projects/2_project/kubeops-gitops/.github/workflows/image-release.yml) pushes first and scans the pushed image — the real contrast case: a failing scan still fails the workflow, but the vulnerable image already sits in GHCR.
- [KubeOps CI](../../../Projects/2_project/kubeops-gitops/.github/workflows/ci.yml) scans the locally built image on every push and PR.
- Hardening that reduces findings at the source: both Dockerfiles use `python:3.12-slim`, non-root users, and `PIP_NO_CACHE_DIR`; the [KubeOps Helm chart](../../../Projects/2_project/kubeops-gitops/helm/kubeops/values.yaml) declares the secure Pod `securityContext`.
- **Absent**: Dockerfile linting (Hadolint), Kubernetes manifest scanning, Terraform scanning (Checkov/tfsec) — notable because Project 3 has real Terraform to scan — plus scan-report retention. All conceptual; candidates for later enhancement.

## Practical Exercise

Trace the complete real scanning flow for the KubeOps image, from CI to release:

```text
Scan tool
Target
Artifact identity
Severity rule
Blocking behavior
Report
Exception mechanism
Main limitation
```

Fill this once for [KubeOps CI](../../../Projects/2_project/kubeops-gitops/.github/workflows/ci.yml) and once for [image-release](../../../Projects/2_project/kubeops-gitops/.github/workflows/image-release.yml), then answer: what exact window of exposure does the release workflow's scan-after-push ordering create, and which TaskOps workflow shows the fix? Finally, name the one unscanned IaC surface in Project 3. Do not run any scanner. Target 25–35 minutes.

## Knowledge Check

1. Why can a scan fail today when nothing in the repository changed?
2. What risk decision does `ignore-unfixed: true` encode?
3. Why is scan-before-push stronger than scan-after-push?
4. What does image scanning not prove even when clean?
5. How does the TaskOps Dockerfile reduce findings by design?
6. Which real IaC in this repository has no security scanning?

<details>
<summary>View answers</summary>

1. Scanner databases update continuously; a newly published CVE in an existing package changes the result without any code change.
2. Vulnerabilities with no available fix do not block the build — accepting temporary exposure in exchange for an actionable gate.
3. A failing scan never publishes the vulnerable image; scan-after-push fails the workflow but leaves the image in the registry.
4. Runtime security: configuration, secrets handling, access control, and application logic are outside an inventory-based scan.
5. It avoids installing apt packages entirely (stdlib health probe) and uses a slim base and non-root user, shrinking the CVE surface Trivy can flag.
6. Project 3's Terraform (and Ansible) — no Checkov, tfsec, or equivalent runs anywhere.

</details>

## Navigation

- [Back to DevSecOps and Supply-Chain Security](../README.md)
- [Previous: Dependency, License, and Software Composition Analysis](../03-dependency-license-and-software-composition-analysis/)
- [Next: SBOM, Signing, Provenance, and Attestations](../05-sbom-signing-provenance-and-attestations/)
- [Back to All Learning Materials](../../README.md)
