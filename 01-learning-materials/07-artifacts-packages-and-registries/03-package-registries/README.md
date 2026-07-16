# Package Registries

## What a Registry Does

A **package registry** stores published package versions, serves their metadata to **dependency resolution**, and controls who may read, publish, or delete. (The terms *registry*, *package repository*, and *package index* overlap; a **repository manager** like Artifactory or Nexus hosts many repositories of different formats.) Registries come in three postures: **public** (PyPI, the npm registry, Maven Central — open to the world), **private** (organization-internal packages), and **proxy / dependency-proxy** (a controlled mirror between your builds and upstream, adding caching, filtering, and **availability** independence from upstream outages).

Structure inside a registry: a **namespace or organization scope** (`@org/package`, `ghcr.io/owner/...`) that anchors ownership, package names within it, and **versions** within each package — including **pre-release versions** and, crucially, versions that should be **immutable** once published.

The registry also stores package **metadata** that a resolver can query: dependencies, compatibility constraints, checksums, publication time, and deprecation state. During **dependency resolution**, an installer selects a permitted version, verifies its integrity data, downloads it, and records or installs the result. Registry availability therefore affects both builds and consumers; pinning an exact version does not help if that version cannot be retrieved. Proxies, controlled mirrors, and tested replication can reduce this dependency without changing the package identity.

Hosted examples, conceptually: PyPI, npm registry, Maven Central, GitHub Packages, GitLab Package Registry, Azure Artifacts, AWS CodeArtifact, JFrog Artifactory, Sonatype Nexus. The mechanics below apply to all of them.

## The Publishing Path

```text
Build pipeline
     ↓
Authenticate with least privilege
     ↓
Publish immutable package version
     ↓
Registry stores package and metadata
     ↓
Consumers install the exact version
```

**Authentication** proves who is publishing; **authorization** limits what that identity may do. Permissions split at least into **read**, **publish**, and **delete** — and CI publishing identities should be **service accounts** or platform tokens with publish-only scope, never a human's personal token. **Short-lived credentials** beat stored long-lived **access tokens** wherever supported. In GitHub Actions, the platform token's registry rights are declared in the workflow:

```yaml
permissions:
  contents: read
  packages: write
```

Permission syntax differs by platform and ecosystem, but the least-privilege shape is universal: read for consumers, write for the one publishing pipeline, delete for almost nobody.

## Version Lifecycle

Published versions age. Registries offer graduated responses: **deprecation** (version stays installable, consumers see a warning), **yanking** (version is hidden from new resolution but remains for those who pinned it — Python's model), and **deletion** (gone — which breaks every consumer whose lockfile references it, which is why released versions used by anyone should effectively never be deleted). **Retention** policies automate cleanup for snapshot/pre-release versions while protecting releases. **Promotion** between repositories (snapshot → release repo) and **replication** across regions or registries belong to lesson 06 and 07 patterns.

Replication improves distribution and outage tolerance, but it does not replace a backup: an accidental deletion may replicate too. Promotion should preserve the package bytes, version, checksum, signature, and provenance rather than rebuilding the package in the destination repository.

## Registry Security

The registry is a supply-chain control point:

- **Namespace ownership** — verify you install from *your* namespace; **dependency confusion** attacks publish public packages named like internal ones.
- **Typosquatting** — malicious names one keystroke from popular packages.
- **Token scope and rotation** — publish tokens scoped to one package/namespace, rotated, and never committed to configuration files.
- **Integrity and provenance** — checksums (automatic in most ecosystems), **package signing**, and provenance attestations connecting a package to the build that produced it.
- **Two-factor authentication** for human publishers; restricted, auditable CI identities for automated publishing — ideally from protected branches only.
- Consumers: pull only from controlled sources (your proxy or the verified public registry), never from arbitrary URLs.

## Common Mistakes

- Publishing with a personal token.
- Reusing long-lived credentials indefinitely.
- Allowing every branch (or every contributor) to publish.
- Overwriting released versions.
- Mixing snapshot and production packages in one channel.
- Deleting versions old releases still depend on.
- Trusting package names without namespace verification.
- Pulling dependencies from uncontrolled sources.

## Existing Repository Evidence

The projects **publish no language packages** — there is no PyPI, npm, or chart publishing anywhere. The only registry in use is GHCR for container images (next lesson), and its permission pattern is the real illustration of this lesson's least-privilege shape: [TaskOps CD](../../../Projects/1_project/taskops-cicd/.github/workflows/cd.yml) grants `packages: write` only to its `deploy` job, and [KubeOps image release](../../../Projects/2_project/kubeops-gitops/.github/workflows/image-release.yml) grants it at the workflow level with `contents: read` — both authenticating with the ephemeral, automatically scoped `GITHUB_TOKEN` rather than a stored personal token. Consumption side: TaskOps and KubeOps *install* their Python dependencies from public PyPI with no proxy registry — normal for small projects, and worth naming as an uncontrolled-source trade-off.

## Practical Exercise

Answer with evidence from the repository:

1. Do any projects publish application packages, or only container images? Cite the workflows.
2. Which identity publishes, and what scopes does it hold? Compare the two workflows' `permissions` placements and argue which is tighter.
3. Where do dependencies come from at build time, and what registry-security concepts from this lesson are unmitigated on that path?
4. If TaskOps later published a Python package, propose: the registry, the namespace, the publishing trigger (which branch/tag), and the credential type.

Do not publish anything. Target 20–30 minutes.

## Knowledge Check

1. What is the difference between deprecating, yanking, and deleting a version?
2. Why should CI publish with a service identity rather than a personal token?
3. What is dependency confusion, and what defends against it?
4. Why should released versions be immutable?
5. What is a proxy registry for?
6. Which registry does this repository actually use, and with what credential?

<details>
<summary>View answers</summary>

1. Deprecation warns but stays installable; yanking hides from new resolution while preserving pinned installs; deletion removes it and breaks consumers referencing it.
2. Personal tokens carry a human's broad rights, outlive their purpose, and vanish when the person leaves; service identities are scoped, auditable, and rotatable.
3. An attacker publishes a public package matching an internal name hoping resolvers prefer it; defenses include namespace verification, scoped registries/proxies, and resolver configuration.
4. Consumers pin them in lockfiles and audits reference them; changed content under a fixed version destroys reproducibility and trust.
5. A controlled mirror between builds and upstream registries — caching, filtering, and availability independence.
6. GitHub Container Registry (GHCR), authenticated with the ephemeral `GITHUB_TOKEN` scoped by `permissions: packages: write`.

</details>

## Navigation

- [Back to Artifacts, Packages, and Registries](../README.md)
- [Previous: Package Formats and Release Assets](../02-package-formats-and-release-assets/)
- [Next: Container and OCI Registries](../04-container-and-oci-registries/)
- [Back to All Learning Materials](../../README.md)
