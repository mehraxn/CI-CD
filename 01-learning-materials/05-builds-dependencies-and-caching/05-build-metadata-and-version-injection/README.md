# Build Metadata and Version Injection

## Why Builds Need Identity

When something misbehaves in production, the first questions are: *which version is this, which commit built it, and which pipeline run produced it?* **Build metadata** answers them. Useful identifiers include the **application/release version** (`1.4.0`), the **commit SHA** (full, immutable) and its **short SHA** (readable, mostly unique), **branch name**, **tag name**, **build number / pipeline run number**, **build timestamp**, **source repository**, and the **build environment**. Together they provide **traceability** (output → source), **debugging** (reproduce the exact code), and **rollback identification** (which previous identity was good).

Metadata is only trustworthy if generated automatically. A conceptual generation step:

```bash
VERSION="1.4.0"
COMMIT_SHA="$(git rev-parse HEAD)"
BUILD_TIME="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
```

Two cautions: a build from a **dirty working tree** produces a SHA that does not actually describe the built code (CI avoids this by building only committed source), and **timestamps reduce byte-for-byte reproducibility** — include them for humans, but do not make them the identity.

## Injecting Metadata into Outputs

Container images carry metadata as **labels** (standardized `org.opencontainers.image.*` keys) injected at build time:

```dockerfile
ARG VERSION
ARG COMMIT_SHA

LABEL org.opencontainers.image.version="$VERSION"
LABEL org.opencontainers.image.revision="$COMMIT_SHA"
```

Workflows commonly use the commit SHA as an **image tag**:

```yaml
env:
  IMAGE_TAG: ${{ github.sha }}
```

A SHA tag is perfectly **traceable but not user-friendly**: nobody says "we're running 9f3ab2c1d…" in a release announcement. Package ecosystems have their own metadata slot (Python's `version` in `pyproject.toml`, npm's `package.json`), and applications can expose a **runtime version endpoint** so operators can ask a live service what it is.

## Combining Identifiers

No single identifier serves every purpose, so mature setups combine them:

```text
Human-facing release:
v1.4.0

Immutable source identity:
full commit SHA

CI run identity:
workflow run number
```

A **semantic version** communicates intent to humans (with **pre-release versions** like `1.5.0-rc.1` for candidates); the SHA pins the source; the run number distinguishes rebuilds of the same source. **Metadata validation** — checking the version matches the tag, the SHA matches the checkout — belongs in the pipeline, because wrong metadata is worse than none. Two principles guard the whole scheme: avoid **mutable identifiers** as the only reference (a `latest` tag points somewhere else tomorrow), and avoid **environment-specific rebuilds** — build once, deploy the same identified output everywhere, rather than rebuilding "the same version" per environment and hoping.

## Common Mistakes

- Manually typing versions in multiple files that drift apart.
- Reusing one mutable tag (`latest`) as the only identifier.
- Exposing sensitive metadata (internal hostnames, tokens) in labels or endpoints.
- Rebuilding the same version number from different source.
- Using branch names as permanent release versions.
- Depending only on timestamps to distinguish builds.
- Failing to include the source revision in diagnostics.

## Existing Repository Evidence

- [KubeOps image release](../../../Projects/2_project/kubeops-gitops/.github/workflows/image-release.yml) tags every image twice: `:latest` *and* `:${{ github.sha }}` — a mutable convenience tag plus an immutable source-linked tag, exactly the combination this lesson recommends.
- [TaskOps CD](../../../Projects/1_project/taskops-cicd/.github/workflows/cd.yml) does the same (`${{ env.IMAGE }}:${{ github.sha }}` and `:latest`) and deploys by passing `IMAGE_TAG: ${{ github.sha }}` to the server — the deployment references the immutable identity, not `latest`.
- [Project 3's application](../../../Projects/3_project/app/) defines an `APP_VERSION` and serves it from a `/version` endpoint (verified by its [test](../../../Projects/3_project/app/tests/test_app.py)) — a real runtime version endpoint.
- [TaskOps pyproject.toml](../../../Projects/1_project/taskops-cicd/pyproject.toml) carries `version = "0.1.0"` as package metadata; note that it is not currently wired into image tags — a small real example of potentially drifting identifiers.
- OCI image labels, build numbers in tags, and pre-release versioning are not currently demonstrated; they remain conceptual and could be added in a later enhancement phase.

## Practical Exercise

Trace image identity end to end for one project. For KubeOps: from the [image-release workflow](../../../Projects/2_project/kubeops-gitops/.github/workflows/image-release.yml), record which tags each build pushes, which of them is immutable, and how you would find the exact source for an image seen in production. Then answer: what breaks if only `:latest` existed? Rate the setup's traceability strengths and weaknesses in three bullet points. Do not modify tagging behavior. Target 15–25 minutes.

## Knowledge Check

1. Why is a commit SHA a good identifier and a bad release name?
2. Why do timestamps conflict with byte-for-byte reproducibility?
3. What is wrong with `latest` as the only identifier?
4. Why should the same version never be rebuilt from different source?
5. Which real project exposes its version at runtime, and why is that useful?

<details>
<summary>View answers</summary>

1. It is immutable and points to exact source, but it is unreadable and communicates nothing about compatibility or intent to humans.
2. Two otherwise identical builds embed different times, so their outputs differ byte-for-byte even though the code is identical.
3. It is mutable — it points to different content over time, so it identifies nothing permanently and makes rollback and diagnosis guesswork.
4. The version stops identifying anything; two deployments of "1.4.0" could behave differently, destroying traceability and trust in rollbacks.
5. Project 3, via its `/version` endpoint — operators can ask a running instance what it is instead of inferring from deployment records.

</details>

## Navigation

- [Back to Builds, Dependencies, and Caching](../README.md)
- [Previous: Build Caching](../04-build-caching/)
- [Next: Cross-Platform and Multi-Architecture Builds](../06-cross-platform-and-multi-architecture-builds/)
- [Back to All Learning Materials](../../README.md)
