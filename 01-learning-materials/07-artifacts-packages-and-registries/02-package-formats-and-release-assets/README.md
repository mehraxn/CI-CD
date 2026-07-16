# Package Formats and Release Assets

## Software Ships in Ecosystem-Shaped Boxes

Every ecosystem defines how software is bundled for distribution:

```text
Application source
    ↓
Build or packaging process
    ↓
Distributable package
    ↓
Package registry or release page
    ↓
Consumer installation or deployment
```

The common forms: **application packages** (a deployable service), **library packages** (code for other projects to import), **binary archives** (compiled executables and **shared libraries**, often as ZIP or TAR), and **source archives** (the code itself, buildable by the consumer). Ecosystem specifics, at overview level: Python ships **wheels** (built) and **source distributions**; the JVM world ships **JARs** and web-app **WARs**; Node.js ships **npm packages**; .NET ships **NuGet packages**; **Go modules** are distributed as versioned source; Kubernetes applications ship **Helm charts**; and containers ship OCI images (next lessons). Adjacent outputs matter too: **debug symbols** and **source maps** let production errors map back to readable code without shipping debug builds to users.

| Output | Typical consumer | Typical storage |
|--------|------------------|-----------------|
| Python wheel | Python installer | Python package registry |
| npm package | Node.js project | npm-compatible registry |
| JAR | JVM application | Maven-compatible repository |
| Helm chart | Kubernetes operator | OCI or chart registry |
| ZIP/TAR release asset | Human or automation | Release page or artifact repository |
| Container image | Container runtime | OCI registry |

## What Makes a Package More Than a File

A package carries **metadata**: name, version, declared **dependencies**, **runtime and platform compatibility**, and **installation metadata** the ecosystem's installer understands. Distribution adds integrity and context: **checksums** (consumers verify the download matches what was published), **signatures** (consumers verify *who* published), a **release manifest** listing exactly what a release contains, and human context — **release notes** and a **changelog** explaining what changed and why.

## Tags, Releases, and Assets

A **Git tag** marks a source revision. A **GitHub release** wraps a tag with notes and **release assets** — downloadable files attached to it. The distinction the whole lesson hinges on: **a Git tag alone is not a distributable artifact.** A tag points at source; consumers of a release need the *built, tested output* — which is also why a source archive is not equivalent to a tested binary: anyone can build from source, but nobody verified *their* build. Release outputs should be produced by automation from the tagged revision, not assembled by hand: a human-built asset is unreproducible, unauditable, and one laptop compromise away from a supply-chain incident.

Version maturity has vocabulary: a **release candidate** (`1.4.0-rc.1`) is a build that *becomes* the release if validation passes; **pre-release packages** signal "not yet stable" to installers that respect the convention.

## Common Mistakes

- Publishing from a developer laptop.
- Publishing without tests.
- Reusing a released version number for different content.
- Omitting checksums.
- Mixing debug and production packages.
- Baking environment-specific configuration into a reusable package.
- Treating a source archive as equivalent to a tested binary.
- Publishing packages without release notes or traceability.

## Existing Repository Evidence

The repository's projects distribute exclusively as **container images** — no wheels, npm packages, GitHub releases, or release assets are produced anywhere. Specifics worth confirming yourself:

- [TaskOps](../../../Projects/1_project/taskops-cicd/) has a `pyproject.toml` with package metadata (`name = "taskops"`, `version = "0.1.0"`), but nothing builds or publishes a Python package; the deliverable is the GHCR image from [cd.yml](../../../Projects/1_project/taskops-cicd/.github/workflows/cd.yml).
- [KubeOps](../../../Projects/2_project/kubeops-gitops/) has a real [Helm chart](../../../Projects/2_project/kubeops-gitops/helm/kubeops/Chart.yaml) — but it is consumed *from Git* by Argo CD, not packaged (`helm package`) or pushed to a chart registry. The chart-as-package path is a natural later enhancement.
- No Git-tag-driven release workflow exists; images are published per commit to `main`, not per tagged release.

## Practical Exercise

For each practical project, identify the appropriate distributable format(s) and justify the choice:

1. TaskOps — is a Python wheel useful, or is the container image the right sole deliverable? What would a GitHub release with assets add (think: checksums, compose file, release notes)?
2. KubeOps — the image plus what? Sketch what packaging and publishing the Helm chart would involve and who would consume it.
3. Project 3 — its deliverable is infrastructure and configuration; what, if anything, is its "package"?

Write one short paragraph per project. Do not create real releases or packages. Target 15–25 minutes.

## Knowledge Check

1. Why is a Git tag not a distributable artifact?
2. What do checksums and signatures each verify?
3. Why should release assets be built by automation rather than a person?
4. What is a release candidate?
5. Why is a source archive not equivalent to a tested binary?
6. What is this repository's only real distributable format?

<details>
<summary>View answers</summary>

1. A tag marks source; consumers need built, tested output — the tag identifies what to build, not the thing to run.
2. Checksums verify the download's integrity (content matches what was published); signatures verify the publisher's identity.
3. Automated builds are reproducible, auditable, and tied to a verified revision; a laptop build is none of those and is a supply-chain risk.
4. A build published as `x.y.z-rc.N` that becomes the actual release if validation passes — same bytes, promoted status.
5. Nobody verified the consumer's build of it; the tested artifact is the specific output that passed verification.
6. Container images pushed to GitHub Container Registry.

</details>

## Navigation

- [Back to Artifacts, Packages, and Registries](../README.md)
- [Previous: Artifacts, Caches, and Job Outputs](../01-artifacts-caches-and-job-outputs/)
- [Next: Package Registries](../03-package-registries/)
- [Back to All Learning Materials](../../README.md)
