# Image Tagging, Versioning, and Metadata

```text
ghcr.io/example/task-api:1.4.0
ghcr.io/example/task-api:sha-a1b2c3d
ghcr.io/example/task-api:latest
ghcr.io/example/task-api@sha256:<digest>
```

The parts are registry, namespace, repository, tag, or content-addressed digest. Tags are movable unless policy protects them. Normalize branch/PR tags to avoid invalid characters and collisions.

| Reference | Strength | Main limitation |
|-----------|----------|-----------------|
| `latest` | Easy | Mutable/weak alone |
| Semantic version | Clear release | Must prevent overwrite |
| Commit SHA | Source traceability | Less friendly |
| Digest | Exact content | Harder manually |

OCI labels can record title, description, source, revision, version, build date, license, docs URL, and build run. `docker/metadata-action` can generate normalized tags/labels but is absent here. TaskOps and KubeOps publish SHA plus `latest`; neither records digest or OCI labels. KubeOps production values use mutable `latest`.

## Reading an Image Reference

In `ghcr.io/example/task-api:1.4.0`, `ghcr.io` is the registry hostname, `example` is the namespace or owner, `task-api` is the repository, and `1.4.0` is a tag. A digest reference replaces the movable tag pointer with content-addressed identity. If any manifest content changes, its digest changes. Multi-platform images add a manifest index, so teams must record whether they mean the index digest or a selected platform manifest.

`latest` has no built-in meaning beyond being a tag name. A registry client may apply it when no tag is written, and publishers may move it at any time. Semantic versions are human-readable releases; commit-SHA tags tie content to a source revision; branch and pull-request tags support temporary testing; and release-candidate tags communicate pre-release intent. Branch and PR strings need normalization because slashes, uppercase policy, length, and collisions can make invalid or ambiguous tags.

An immutable policy prevents overwriting protected tags, but the registry must enforce it. A digest remains the strongest exact content reference. A deployment can use a readable tag for communication while recording or pinning the resolved digest for audit and rollback. Rollback identity means knowing precisely which prior image was accepted, not merely typing `latest` again.

## Metadata for Traceability

OCI annotations can record image title, description, source repository, source revision, version, creation date, license, documentation URL, and build-run information. The following is conceptual; the URL is an intentionally invalid placeholder:

```dockerfile
ARG VERSION
ARG COMMIT_SHA

LABEL org.opencontainers.image.version="$VERSION"
LABEL org.opencontainers.image.revision="$COMMIT_SHA"
LABEL org.opencontainers.image.source="https://example.invalid/repository"
```

Build arguments used for public metadata are acceptable, but never place secrets in them. Tools such as `docker/metadata-action` can generate normalized multi-tag and label sets from Git events. That action is not used in this repository. Metadata should agree with application versioning and source; conflicting labels and tags make incident response harder.

## Repository Tag Audit

TaskOps [CD](../../../Projects/1_project/taskops-cicd/.github/workflows/cd.yml) computes a lowercase GHCR name and builds the same local image with `${{ github.sha }}` and `latest`. It scans the SHA tag, pushes both references, and deploys the SHA through `IMAGE_TAG`. KubeOps [image release](../../../Projects/2_project/kubeops-gitops/.github/workflows/image-release.yml) likewise publishes SHA and `latest`, then scans the pushed SHA. This is real dual-tag behavior.

Neither workflow creates semantic-version, branch, pull-request, or release-candidate tags. Neither uses `docker/metadata-action`, adds OCI labels, captures a pushed digest, signs the image, or publishes provenance. KubeOps [production values](../../../Projects/2_project/kubeops-gitops/helm/kubeops/values-prod.yaml) reference `latest` and explicitly advise immutable identity for real deployment. No claim can be made that registry tag immutability is enabled.

A stronger conceptual policy would publish a protected release tag plus a commit-SHA tag, record the digest from the push, and update deployment configuration to the accepted tag or digest through review. PR images would use normalized, non-production names and retention. Tags should be created only after required verification, never changed manually, and mapped to build evidence. This is a proposal, not current workflow behavior.

Common failures include reusing release tags, deploying `latest` without recording content, tagging before tests, unsanitized branch names, missing source revision, version disagreement, manual retagging, and no temporary-image policy. A tag is a pointer, not the image bytes.

## Policy Decisions

A policy should define who creates or overwrites release tags, how temporary names are normalized, when `latest` moves, which tags expire, and where digests are recorded. It connects application version, source commit, build run, OCI revision label, and registry digest without treating them as identical. Several tags may point to one digest; a protected release tag should not point to several digests over time.

During an incident, operators need the running digest, producing revision, verifying workflow, and compatible prior identity. `latest` alone cannot reliably answer these questions. Readable tags aid communication; digest evidence provides exactness. Both belong in release and deployment records.

## Practical Exercise

Audit real tags and propose semantic, SHA, PR, candidate, digest, and rollback identities without changing workflows.

## Knowledge Check

1. Are tags content? 2. Strongest exact identity? 3. Why sanitize branches? 4. What metadata is absent?

<details><summary>Answers</summary>

1. No, pointers. 2. Digest. 3. Validity/collision/security. 4. OCI labels and recorded digest.

</details>

## Navigation
- [Back to Docker in CI/CD](../README.md)
- [Previous: Layers, Caching, and Multi-Stage Builds](../03-layers-caching-and-multi-stage-builds/)
- [Next: Docker Compose in Development and CI](../05-docker-compose-in-development-and-ci/)
- [Back to All Learning Materials](../../README.md)
