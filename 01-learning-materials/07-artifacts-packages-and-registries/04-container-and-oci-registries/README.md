# Container and OCI Registries

## Images and Their Anatomy

A **container image** in the **OCI** (Open Container Initiative) format is a stack of **layers** (filesystem diffs), an **image configuration** (environment, entrypoint, labels), and an **image manifest** tying them together by digest. An **image index** (manifest list) maps platforms to variants for **multi-architecture images**. Because the objects are content-addressed, every image has a **digest** — `sha256:...` — that identifies its exact content. The identity does not change, although a registry can later delete the content and make it unavailable.

A full image reference decomposes as:

```text
ghcr.io / mehraxn / kubeops : latest
registry   namespace  repository  tag
```

**Tags** are human-named pointers that can move; **digests** are content-addressed and cannot. That single fact drives most registry policy.

A registry groups image **repositories** inside namespaces. A client **pushes** manifests and missing layers to publish, then a runtime **pulls** the selected manifest and layers to run it. Authentication proves the client identity; authorization decides whether that identity may pull a private image, push a new manifest, overwrite a tag, or delete content. Public images normally permit anonymous pulls, not anonymous pushes.

## The Publishing Path

```text
Dockerfile
    ↓
Container build
    ↓
Image scan
    ↓
Registry authentication
    ↓
Push image tag and digest
    ↓
Deployment pulls immutable image identity
```

A conceptual login-and-publish workflow (closely matching, but simplified from, this repository's real ones):

```yaml
permissions:
  contents: read
  packages: write

steps:
  - name: Log in to the registry
    uses: docker/login-action@v3
    with:
      registry: ghcr.io
      username: ${{ github.actor }}
      password: ${{ secrets.GITHUB_TOKEN }}

  - name: Build and push
    uses: docker/build-push-action@v6
    with:
      context: .
      push: true
      tags: ghcr.io/example/application:${{ github.sha }}
```

Reading it: the **registry hostname** (`ghcr.io`) selects the service; `packages: write` grants the ephemeral token push rights; the login action receives the token as an input — it is never echoed, and printing it would defeat masking; the tag embeds the **commit SHA**, linking image to source. Registries in the same conceptual family: GitHub Container Registry, Docker Hub, GitLab Container Registry, AWS ECR, Azure Container Registry, Google Artifact Registry, and self-hosted Harbor. This repository uses **GHCR** exclusively.

## Identity Strength

| Identifier | Human readability | Mutability risk | Traceability |
|------------|-------------------|-----------------|--------------|
| `latest` | High | High | Weak alone |
| Semantic version | High | Should be immutable by policy | Strong |
| Commit SHA tag | Medium | Should be immutable by policy | Strong |
| Image digest | Low | Content-addressed | Strongest identity |

Tags — even version tags — are *policy-immutable at best*: nothing in the protocol stops a re-push, though registries can protect tags by configuration. A **digest is stronger than any tag for deployment identity** because it cannot point anywhere else. Deploying by digest (or at minimum by SHA tag) makes "what is running?" answerable with certainty.

## Registry Operations and Extras

Registries govern more than storage: **authentication/authorization** and public/private visibility; **retention** and **garbage collection** (deleting manifests leaves **orphaned layers** until GC runs); **replication** across regions; **rate limits** (Docker Hub's pull limits famously break CI) and **pull-through caches** to absorb them; **air-gapped registries** for isolated networks; and **scanning** integrated at the registry. Beyond images, OCI registries increasingly store **OCI artifacts** — Helm charts, SBOMs, signatures, provenance — attached to or alongside images (**content trust** and signing are Topic 14 territory; here it is enough to know signatures and SBOM/provenance attachments live in the registry next to the image).

## Common Mistakes

- Using only `latest`.
- Publishing from untrusted branches.
- Logging registry passwords.
- Granting unnecessary package permissions.
- Deploying by mutable tag only.
- Deleting images still used by deployments.
- Scanning after deployment instead of before publishing.
- Failing to connect an image to its source revision.
- Assuming a private registry makes images safe — it controls access, not content.

## Existing Repository Evidence

- [TaskOps CD](../../../Projects/1_project/taskops-cicd/.github/workflows/cd.yml) is the fullest real example: computes a lowercase image name, logs in to `ghcr.io` with `docker/login-action@v3` and `secrets.GITHUB_TOKEN`, Trivy-scans the image **before pushing** (gate placement done right), pushes both `:${{ github.sha }}` and `:latest`, and deploys the **SHA tag** to the server (`IMAGE_TAG: ${{ github.sha }}`) — mutable-tag convenience for humans, immutable-ish identity for deployment.
- [KubeOps image release](../../../Projects/2_project/kubeops-gitops/.github/workflows/image-release.yml) pushes the same dual tags but scans **after** pushing — a real, instructive gate-placement contrast with TaskOps.
- [values-prod.yaml](../../../Projects/2_project/kubeops-gitops/helm/kubeops/values-prod.yaml) consumes `ghcr.io/mehraxn/kubeops` with `tag: "latest"` — and its own comment says it: *"pin to an immutable version/digest in real deployments."* The repository documents its own trade-off.
- Digest-based deployment, multi-arch indexes, OCI labels, retention policies, and signing are not currently demonstrated.

## Practical Exercise

Map the KubeOps production image reference end to end:

```text
Registry
Namespace
Repository
Tag
Possible digest
Source revision
Publishing workflow
Deployment consumer
```

Use `values-prod.yaml` and `image-release.yml` as sources. Then answer: given a running production pod, could you determine today the exact commit it was built from? Which one change (from the identity table) would make that answer certain, and what does the values-prod comment already say about it? Do not change publishing behavior. Target 20–30 minutes.

## Knowledge Check

1. Decompose `ghcr.io/mehraxn/kubeops:latest` into its four parts.
2. Why is a digest stronger than any tag?
3. Why does the login action receive the token as an input instead of a command argument?
4. What is the gate-placement difference between the two publishing workflows here?
5. Why does a private registry not make images safe?
6. What does the KubeOps values-prod file admit about its own tag choice?

<details>
<summary>View answers</summary>

1. Registry `ghcr.io`, namespace `mehraxn`, repository `kubeops`, tag `latest`.
2. It is content-addressed — it identifies exact bytes and cannot be re-pointed, while tags are movable pointers.
3. Command arguments can appear in process lists and logs; action inputs keep the credential out of printable surfaces.
4. TaskOps CD scans before pushing (a bad image never reaches the registry); KubeOps image-release scans after pushing (a bad image is published, then flagged).
5. Privacy controls who can pull, not whether the content is vulnerable or malicious — scanning and provenance address content.
6. That `latest` should be replaced with an immutable version or digest in real deployments — the comment in the file says so explicitly.

</details>

## Navigation

- [Back to Artifacts, Packages, and Registries](../README.md)
- [Previous: Package Registries](../03-package-registries/)
- [Next: Artifact Naming, Versioning, and Metadata](../05-artifact-naming-versioning-and-metadata/)
- [Back to All Learning Materials](../../README.md)
