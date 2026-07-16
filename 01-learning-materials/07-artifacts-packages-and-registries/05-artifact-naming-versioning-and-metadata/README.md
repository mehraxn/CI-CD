# Artifact Naming, Versioning, and Metadata

## Names Are the First Metadata

An artifact's name is what humans and machines search, sort, and trust. A good name answers *what, which version, and for what platform* without opening the file:

```text
application-1.4.0-linux-amd64.tar.gz
application-1.4.0-sbom.spdx.json
application-1.4.0-checksums.txt
```

The container equivalent stacks identities on one repository:

```text
ghcr.io/example/application:1.4.0
ghcr.io/example/application:sha-a1b2c3d
ghcr.io/example/application@sha256:<digest>
```

Naming ingredients: package/image **name**, **version** (semantic, with pre-release markers), **build/run number**, **commit SHA** or **tag**, **branch name**, **timestamp**, **platform/architecture**. Two rules govern their use. First, names must be **collision-free**: two different contents must never share a name (which is why "reusing one artifact name for different content" heads the mistake list). Second, **environment names generally do not belong in a reusable artifact** — `application-1.4.0-staging.tar.gz` implies a staging-specific build, which contradicts build-once-deploy-many; environment specifics belong in configuration (Topic 08), not in the artifact.

**Branch names need sanitization** before entering names: branches may contain `/`, uppercase, or arbitrary user input, which breaks tags, DNS labels, and paths — and unsanitized interpolation of a branch name into a shell command is an injection vector, not just a formatting bug.

A written **naming convention** should define field order, separators, case, allowed characters, and maximum length. Validate those rules before publication and reject an empty version, unsupported platform, or duplicate identity. Stable conventions improve **searchability**: humans can find a release by version while automation can parse the same fields without guessing. A pipeline run number prevents collisions among internal builds, but the source revision and content checksum are still needed to explain what the run produced.

## Metadata Beyond the Name

| Metadata | Purpose |
|----------|---------|
| Version | Human release identity |
| Commit SHA | Exact source revision |
| Digest or checksum | Content integrity |
| Build run | CI traceability |
| Platform | Compatibility |
| Creation time | Operational context |

Rich metadata lives *attached to* the artifact rather than crammed into its name: package manifests, and for images, **OCI labels** (`org.opencontainers.image.revision`, `.version`, `.source`) recording **source repository**, **revision**, **build workflow/URL**, and **toolchain/runtime versions**. Metadata should be **machine-readable** (automation queries it), **human-readable** (operators read it at 3 a.m.), and **validated** in the pipeline — wrong metadata is worse than none, because people trust it. One caution: labels on public images are public; do not embed confidential repository details or internal hostnames in them.

A release manifest can connect several files to one release identity. For example, it can list the archive, SBOM, checksum file, supported operating system and architecture, producing workflow run, and creation timestamp. Consumers then verify both compatibility and lineage instead of trusting a filename alone.

## Common Mistakes

- Ambiguous names such as `output.zip`.
- Using branch names without sanitization.
- Timestamps as the only version — sortable but meaningless.
- Reusing one artifact name for different content.
- Rebuilding the same version differently.
- Mixing staging and production binaries in one naming scheme.
- Omitting the source revision.
- Exposing confidential repository information in public metadata.

## Existing Repository Evidence

- Both publishers use the **commit SHA plus `latest`** naming scheme: [TaskOps CD](../../../Projects/1_project/taskops-cicd/.github/workflows/cd.yml) pushes `${IMAGE}:${{ github.sha }}` and `:latest`; [KubeOps image release](../../../Projects/2_project/kubeops-gitops/.github/workflows/image-release.yml) does the same. Source-revision traceability is therefore *in the tag itself* — no OCI labels are set, so the SHA tag is currently the only image-to-source link.
- Both workflows **sanitize the namespace**: they lowercase `github.repository_owner` (`${OWNER,,}`) because GHCR requires lowercase paths — a real, small example of name sanitization.
- The semantic-version slot is empty: [TaskOps `pyproject.toml`](../../../Projects/1_project/taskops-cicd/pyproject.toml) declares `version = "0.1.0"` but no workflow injects it into image tags, so there is no `:1.4.0`-style human release identity — only SHAs and `latest`.
- `docker/metadata-action` (which generates tags and OCI labels systematically), checksums files, and SBOM naming are not currently demonstrated.

## Practical Exercise

Audit and propose. First, list every identifier the repository currently attaches to its images (tags, and note the absence of labels and version tags). Then draft a naming proposal for TaskOps release artifacts if a versioned release process were added:

1. An image tagging scheme combining semantic version, SHA, and `latest` — state what each tag is *for*.
2. Names for three release assets (archive, checksums, SBOM) following the scheme at the top of this lesson.
3. The three OCI labels you would add first, and their sources in the workflow context.

Do not modify anything. Target 15–25 minutes.

## Knowledge Check

1. What three questions should an artifact name answer at a glance?
2. Why should environment names stay out of reusable artifacts?
3. Why do branch names need sanitization before entering artifact names?
4. Where should rich metadata live, and why not in the name?
5. What is currently the only link between this repository's images and their source?
6. Why are timestamps insufficient as the only version?

<details>
<summary>View answers</summary>

1. What the artifact is, which version, and which platform/architecture it targets.
2. They imply environment-specific builds, contradicting build-once-deploy-many; environment specifics belong in configuration applied at deployment.
3. Branches can contain characters invalid in tags, DNS, and paths, and are user-controlled input — unsanitized use breaks references and invites injection.
4. Attached metadata (manifests, OCI labels) — names must stay short and stable, while metadata can be rich, structured, and machine-queryable.
5. The commit-SHA image tag — no OCI labels or version tags are currently set.
6. They order builds but identify nothing: no source revision, no compatibility meaning, and two rebuilds of identical source get different "versions."

</details>

## Navigation

- [Back to Artifacts, Packages, and Registries](../README.md)
- [Previous: Container and OCI Registries](../04-container-and-oci-registries/)
- [Next: Immutability, Promotion, and Release Bundles](../06-immutability-promotion-and-release-bundles/)
- [Back to All Learning Materials](../../README.md)
