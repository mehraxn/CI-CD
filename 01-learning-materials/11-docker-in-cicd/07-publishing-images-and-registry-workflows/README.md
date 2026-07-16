# Publishing Images and Registry Workflows

Publication authenticates to a registry with least privilege, builds verified content, assigns traceable tags, pushes manifest/layers, records digest, and retains evidence. Pull needs read access; push needs write; ordinary publishing should not need delete/admin.

TaskOps CD and KubeOps image-release use `docker/login-action@v3`, Buildx, `GITHUB_TOKEN`, and `packages: write` to GHCR. Both lowercase the owner and push SHA plus `latest`. No QEMU, multi-architecture index, digest capture, signing, SBOM, or provenance exists. TaskOps scans before push; KubeOps after.

Private images still need scanning and controlled deployment credentials. Never print tokens or put them in command arguments. Protect release tags and publish only from trusted triggers.

## Registry Publication Flow

An image reference combines registry, namespace, repository, and tag or digest. Publication uploads missing layers and a manifest, then associates the chosen tag. Authentication proves an identity; authorization limits what it can do. A publisher generally needs read and scoped package write access, not package deletion, repository administration, or unrelated credentials. A deployment consumer normally needs only pull access.

```text
Trusted source event
    | authenticate with scoped credential
Build and verify image
    | assign traceable tags
Push layers and manifest
    | record digest and evidence
Deployment pulls approved identity
```

Registry tokens must not be printed, embedded in images, passed through ordinary build arguments, or stored in committed configuration. Short-lived CI credentials are preferable to long-lived personal tokens. For private images, the target also needs a protected pull identity. Private storage reduces public visibility but does not remove vulnerability, supply-chain, or access-control risk.

Multiple tags can point to one image. A human-facing version and a commit-SHA tag are useful only if protected against unexpected overwrite. The returned digest should be recorded for exact identity. Retention rules should distinguish releases from temporary branch and PR images. Trusted triggers matter because a workflow with package-write permission must not publish arbitrary unreviewed code.

## GHCR Evidence

TaskOps [CD](../../../Projects/1_project/taskops-cicd/.github/workflows/cd.yml) declares `contents: read` and `packages: write`. `packages: write` is required because `GITHUB_TOKEN` pushes to GitHub Container Registry. The workflow lowercases the repository owner because GHCR paths must be lowercase, logs in with `docker/login-action@v3`, sets up Buildx, builds SHA and `latest` tags locally, scans the SHA image, and pushes both with `docker push`. It later passes the SHA tag to deployment. Login credentials are referenced by expression; their values are not documented.

KubeOps [image release](../../../Projects/2_project/kubeops-gitops/.github/workflows/image-release.yml) uses the same minimal permissions, login action, lowercase owner logic, Buildx, GHCR, and dual tags. Its `docker/build-push-action@v6` builds and pushes directly, after which Trivy scans the SHA image from the registry. That ordering means rejected content may already have been published. This is a factual contrast, not a workflow change.

Neither workflow uses `docker/setup-qemu-action`, multi-platform `platforms`, an OCI image index strategy, `docker/metadata-action`, digest capture, cosign-style signing, attestation, SBOM publication, or provenance output. No registry retention or immutable-tag policy is visible in files. External package visibility and repository settings cannot be inferred.

## Designing a Trustworthy Workflow

A robust conceptual sequence verifies source and dependencies, builds once, tests the exact image, scans under policy, logs in only when publication is needed, pushes traceable tags, records the registry digest, and hands that identity to deployment. Separate credentials for pull and push reduce blast radius. Release publication should be serialized or collision-safe, and failures must not silently move stable tags.

Multi-architecture publishing needs builders for each target platform or emulation such as QEMU, then a manifest index joining platform manifests. Every platform variant should be tested; success on `amd64` does not prove `arm64`. This repository does not implement that flow.

Common mistakes include broad personal tokens, login before untrusted build steps, publishing before required gates, only using `latest`, failing to normalize names, omitting digest evidence, assuming private equals secure, and leaving rejected temporary images indefinitely.

## Publication Evidence

For each publication, retain the trusted trigger, source revision, workflow run, builder/platform, tests and scan policy, repository, tags, returned digest, and actor. Verify that deployment references content from that event. Package-write credentials should exist only in the publishing job and be unavailable to untrusted code paths. Pull consumers need separate read-only access where possible.

Failure handling must define whether partially published tags are removed or quarantined, who can move stable tags, and how rejected temporary content expires. Registry settings are external state; workflow YAML alone cannot prove package visibility, immutability, or retention. Report those properties as unknown unless configuration evidence exists.

## Promotion and Recovery

Publication and promotion are different. Publication makes an image available; promotion approves its identity for an environment. A stable release should promote already verified content, not rebuild or retag unknown bytes on an operator laptop. Record the digest at publication and carry it into desired-state review.

If a push partially fails, determine which tags and manifests became visible before retrying. Retrying mutable tags concurrently can create races. Serialize stable releases or use unique immutable tags first, then move convenience tags only after success. Recovery procedures need a known prior digest and retention policy that keeps it available.

Registry audit should review package writers, readers, deletion rights, token lifetime, tag protection, retention, and access logs. Those settings are outside workflow files, so they remain validation questions here rather than implementation claims.

## Practical Exercise

Annotate one workflow: trigger, permissions, login, image name, tags, scan point, cache, digest gap, and consumer.

## Knowledge Check

1. Minimum publisher right? 2. Why record digest? 3. Private means safe? 4. Is multi-arch present?

<details><summary>Answers</summary>

1. Scoped write. 2. Exact content identity. 3. No. 4. No.

</details>

## Navigation
- [Back to Docker in CI/CD](../README.md)
- [Previous: Container Testing, Health Checks, and Scanning](../06-container-testing-health-checks-and-scanning/)
- [Next: Deploying Container Images](../08-deploying-container-images/)
- [Back to All Learning Materials](../../README.md)
