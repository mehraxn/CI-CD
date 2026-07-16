# Immutability, Promotion, and Release Bundles

## Build Once, Deploy Many

The core discipline of trustworthy delivery:

```text
Build once
    ↓
Create immutable artifact
    ↓
Test the exact artifact
    ↓
Promote the same artifact to staging
    ↓
Approve
    ↓
Promote the same artifact to production
```

Contrast the alternative — build separately for test, build again for staging, build again for production. Every rebuild is a chance for variation: a floating base image rebuilt, a transitive dependency resolved differently, a toolchain patch released overnight. Then staging validated one set of bytes and production runs another, and the whole verification chain silently proved nothing. **Promotion** — moving the *same* immutable artifact forward — is what makes staging results transfer to production.

An **immutable artifact** never changes after creation; **content-addressed identity** (a digest) makes immutability verifiable rather than promised. A **mutable tag** (`latest`, or even a re-pushable version tag) is a pointer, not an identity — useful for humans, insufficient alone for promotion decisions.

## How Promotion Is Implemented

Promotion is a status change, and there are several mechanical forms:

- **Metadata / release-status promotion** — the registry or release system marks a version as promoted; bytes never move.
- **Tag promotion** — add an environment or approval tag (`:staging-approved`, `:v1.4.0`) to the existing image. Adding a tag that points to the same digest **does not change the content** — it is a new pointer to the same bytes.
- **Repository or registry copy** — copy the artifact from a snapshot repo to a release repo, or between registry accounts (dev registry → prod registry); the digest should verify the copy.
- **Digest reference** — the deployment manifest simply pins the approved digest; nothing is copied at all.
- **Release-bundle promotion** — promote a bundle (below) as one auditable unit.

A **release candidate** is exactly this pattern applied to versioning: the RC *is* the release if validation passes — promoted, not rebuilt.

After **staging validation**, the candidate becomes an **approved artifact** through a recorded release-status or approval change. **Production promotion** must bind that decision to the candidate's digest or checksum. **Metadata promotion** may add the approval state, destination, and time without changing the artifact; a **release manifest** records the identities of every component being promoted. This distinction keeps changing process data separate from immutable application bytes.

## Release Bundles: The Artifact Plus Its Evidence

An artifact alone answers "what runs"; audits and rollbacks also ask "what proved it was fit?" A release bundle keeps the evidence with the release:

```text
Release 1.4.0
├── Application package
├── Container-image digest
├── Checksums
├── SBOM
├── Test report
├── Security-scan report
├── Provenance statement
└── Release notes
```

The **SBOM** (bill of materials) lists what is inside; **provenance** states how and from what it was built; **test and scan evidence** show what was verified; the **approval record** shows who authorized promotion — kept *alongside* the artifact, not baked into it (approval status changes; artifact bytes must not). The bundle also names the **rollback identity**: rolling back means redeploying a previous immutable identity, which only works if that identity still exists (retention, next lesson). A **roll-forward identity** names the corrective artifact, while recording the failed identity preserves the evidence needed for diagnosis.

## Common Mistakes

- Rebuilding for production.
- Promoting untested output.
- Using a mutable tag as the only identity.
- Losing test and scan evidence after the run expires.
- Promoting an artifact without its dependency metadata.
- Deleting the rollback artifact.
- Mixing approval metadata into artifact content.
- Treating promotion as copying source code — promotion moves *outputs*, not source.

## Existing Repository Evidence

- The repository practices a compact build-once pattern within each delivery: [TaskOps CD](../../../Projects/1_project/taskops-cicd/.github/workflows/cd.yml) builds one image, scans *that* image, pushes *that* image, and deploys *that* image by SHA tag — the tested bytes are the deployed bytes. There is no multi-environment promotion (no staging), so promotion across environments remains conceptual here.
- A real **rollback identity** mechanism exists: TaskOps' [deploy script](../../../Projects/1_project/taskops-cicd/scripts/deploy.sh) records the previously deployed tag in a state file so `rollback.sh` can revert to it — exactly the "keep the previous immutable identity" principle in shell form.
- [KubeOps](../../../Projects/2_project/kubeops-gitops/helm/kubeops/values-prod.yaml) consumes `latest` in its production values — the mutable-tag-as-only-identity risk this lesson warns about, flagged by the file's own comment.
- Release bundles, SBOMs, provenance, staged promotion, and approval records are not currently demonstrated and may arrive in a later enhancement phase.

## Practical Exercise

Design a promotion path for KubeOps without modifying anything. Produce a short document with:

1. The immutable identity to promote (which tag/digest scheme, given what `image-release.yml` produces today).
2. Three stages (e.g., dev → staging → prod) and the promotion mechanism between each (tag, values-file change, digest pin) — remember Argo CD deploys from Git, so state *which file changes* at each promotion.
3. The evidence bundle each promotion should carry.
4. The rollback procedure at each stage, referencing the identity from step 1.

Target 25–35 minutes.

## Knowledge Check

1. Why does rebuilding per environment invalidate staging results?
2. Does adding a new tag to an image change the image?
3. What makes immutability *verifiable* rather than promised?
4. What belongs in a release bundle beyond the artifact itself?
5. Why must approval metadata stay outside artifact content?
6. What real rollback-identity mechanism exists in this repository?

<details>
<summary>View answers</summary>

1. Production runs different bytes than staging validated — floating inputs can differ between builds, so verification does not transfer.
2. No — a tag pointing at the same digest is a new pointer to identical bytes; content is unchanged.
3. Content-addressed identity: a digest is computed from the bytes, so any change produces a different identity.
4. Checksums, SBOM, test and security-scan evidence, provenance, approval record, and release notes — the proof of fitness.
5. Approval status changes over time, and artifact bytes must never change; mixing them would force mutation or re-creation of the artifact.
6. TaskOps' deploy script records the previously deployed image tag in a state file, which the rollback script redeploys.

</details>

## Navigation

- [Back to Artifacts, Packages, and Registries](../README.md)
- [Previous: Artifact Naming, Versioning, and Metadata](../05-artifact-naming-versioning-and-metadata/)
- [Next: Retention, Cleanup, Access, and Replication](../07-retention-cleanup-access-and-replication/)
- [Back to All Learning Materials](../../README.md)
