# Build Once, Deploy Many, and Artifact Promotion

## One Build, One Chain of Custody

```text
One source revision
        ↓
One verified build
        ↓
One immutable artifact
        ↓
Test environment
        ↓
Staging
        ↓
Production
```

**Build once, deploy many** means every environment receives the same immutable artifact. Environment-specific configuration is injected separately. Artifact identity may be a checksum, signed package identity, or image digest. A digest is content-addressed; a tag such as `latest` is movable.

Contrast this with:

```text
Build for test
Build again for staging
Build again for production
```

Separate builds can differ because dependencies, toolchains, base images, network responses, generated timestamps, or environment inputs change. This creates **artifact drift** even when source has not changed; rebuilding different source also creates source drift.

| Approach | Traceability | Risk |
|----------|--------------|------|
| Rebuild per environment | Lower | Different content may reach each environment |
| Promote one immutable artifact | Higher | Requires strong artifact storage and configuration separation |

## Promotion Forms

Promotion can change release metadata, add a protected tag pointing to the same digest, copy content repository-to-repository or account-to-account, or update deployment configuration to reference an approved digest. The bytes, checksum, signatures, and provenance must remain intact. A release status and approval record belong beside the artifact, not inside it.

The chain of custody records source, build run, integrity identity, test evidence, each promotion, actor, environment, and result. Promotion failure must not silently rebuild. Preserve the failed record, correct the cause, and retry the same artifact or create a new candidate. Retain a known-good rollback artifact.

Registry promotion can copy a manifest and layers between repositories or accounts, while repository promotion can move a package from snapshot to release storage. The destination must verify checksums or digests after copying. Tag promotion adds a readable pointer to existing content; it is safe only when the underlying digest is recorded and protected. Metadata promotion changes approval or release status without changing bytes.

Signatures offer publisher authenticity and checksums offer integrity; neither proves that tests passed. The audit trail connects those identities to evidence. Environment promotion should change configuration and authorization, not rebuild the application. Secrets must be injected at the destination and never embedded to make an artifact “production ready.”

A rollback artifact is part of retention planning. Before promotion, verify that the destination can pull it, that its dependencies remain available, and that old configuration/schema compatibility still holds. An expired or vulnerable old image may be an unacceptable rollback even when technically retrievable.

## Existing Repository Evidence

[TaskOps CD](../../../Projects/1_project/taskops-cicd/.github/workflows/cd.yml) builds once inside its deploy job, scans that local image, pushes SHA and `latest`, then deploys the SHA tag. This is a good single-flow build-once shape, but no digest is recorded and there is no test/staging/production promotion chain. [KubeOps image release](../../../Projects/2_project/kubeops-gitops/.github/workflows/image-release.yml) publishes SHA and `latest`; [production values](../../../Projects/2_project/kubeops-gitops/helm/kubeops/values-prod.yaml) use `latest`, so digest-based deployment is absent.

## Common Mistakes

- Promoting only `latest`.
- Rebuilding after approval.
- Embedding environment secrets in the artifact.
- Changing content without changing version.
- Losing staging identity or rollback output.
- Promoting unverified output.
- Treating source-code movement as artifact promotion.

## Practical Exercise

Draw TaskOps from commit through build, scan, GHCR, SSH deployment, and rollback record. Mark identities at every edge and where a digest or staging step is absent. Identify whether any rebuild occurs after scan. Do not change the workflow.

## Knowledge Check

1. Why can equal source produce different rebuilds?
2. What is promoted in build-once-deploy-many?
3. Is a SHA tag inherently immutable?
4. Where does environment configuration belong?
5. What promotion limitation exists in KubeOps production values?

<details><summary>View answers</summary>

1. External inputs, time, toolchains, dependencies, and base images may change.
2. The exact verified artifact and its evidence.
3. No. Registry policy must prevent overwriting; a digest is content-addressed.
4. Outside the reusable artifact, supplied at deployment or runtime.
5. It references mutable `latest` and has no staged digest promotion.

</details>

## Navigation

- [Back to Continuous Delivery and Releases](../README.md)
- [Previous: Release Pipeline Design and Release Candidates](../02-release-pipeline-design-and-release-candidates/)
- [Next: Versioning, Tags, Changelogs, and Release Notes](../04-versioning-tags-changelogs-and-release-notes/)
- [Back to All Learning Materials](../../README.md)
