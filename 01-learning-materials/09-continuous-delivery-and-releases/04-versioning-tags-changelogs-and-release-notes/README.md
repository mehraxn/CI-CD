# Versioning, Tags, Changelogs, and Release Notes

## Release Identity

```text
v1.4.0
v1.4.1
v2.0.0
v2.0.0-rc.1
```

Semantic Versioning expresses compatibility:

```text
Major:
Breaking compatibility change.

Minor:
Backward-compatible functionality.

Patch:
Backward-compatible correction.
```

A pre-release suffix identifies candidates; build metadata can identify a build without changing precedence. SemVer only works when compatibility rules are understood. Other products legitimately use dates, revisions, or platform-specific schemes.

A Git tag names a source revision. Annotated tags carry author, date, and message; signed tags add authenticity evidence. A tag is not the built artifact. Package versions and image tags must connect to the exact artifact digest. Release branches can stabilize a version, but create coordination and drift costs.

## Changelog and Release Notes

A **changelog** is the historical record across releases. **Release notes** communicate one release to users and operators. Conventional Commits can support automated grouping, but human-curated notes must explain impact, breaking changes, migration and upgrade instructions, security notes, compatibility, deprecations, known issues, date, author, source, and artifact identity.

An annotated tag is preferable to a lightweight tag for an official source milestone because it has a message, tagger, and date. A signed tag can prove that a trusted signing identity created it, but signing policy, key protection, and verification still matter. Tags can be deleted or moved by sufficiently authorized users, so server policy and audit complement signatures.

Release identifiers should remain consistent across package metadata, image tags, charts, documentation, and monitoring. One authoritative source can generate secondary locations, while CI detects disagreement. The release date and author identify the human decision, whereas source revision and digest identify technical content.

Deprecation notes warn consumers before removal. Migration notes state required operator actions and ordering. Security notes balance usefulness with responsible disclosure. Known issues prevent repeated investigation, and upgrade instructions must state supported starting versions and rollback limitations. A bare commit list rarely answers those questions.

```markdown
# Release 1.4.0

## Highlights

## Added

## Changed

## Fixed

## Security

## Migration Notes

## Known Issues

## Artifact Identity

- Commit:
- Image digest:
- Package version:
```

## Existing Repository Evidence

[TaskOps pyproject](../../../Projects/1_project/taskops-cicd/pyproject.toml) and [KubeOps pyproject](../../../Projects/2_project/kubeops-gitops/pyproject.toml) both say `0.1.0`; [KubeOps Chart.yaml](../../../Projects/2_project/kubeops-gitops/helm/kubeops/Chart.yaml) has chart and application version `0.1.0`. Workflows do not publish those versions: images receive SHA and `latest`. Project 3 reports runtime `APP_VERSION` default `1.0.0` in [main.py](../../../Projects/3_project/app/main.py). These disconnected locations can drift. No changelog, tag release, signed tag, release notes, or GitHub Release exists.

## Common Mistakes

- Reusing a released version or tagging unverified source.
- Keeping inconsistent versions in several files.
- Shipping breaking changes as a patch.
- Listing only commit hashes in notes.
- Omitting migration instructions or exact artifact identity.
- Disconnecting mutable image tags from Git release tags.

## Practical Exercise

Inventory every version source above. Identify its consumer, authority, update mechanism, and drift risk. Draft—not publish—release notes for a hypothetical TaskOps `1.0.0`, leaving unavailable digest and date fields explicitly pending.

## Knowledge Check

1. What does a major version communicate?
2. How do a Git tag and image digest differ?
3. Changelog versus release notes?
4. Why can automated notes be insufficient?
5. Where can version drift occur here?

<details><summary>View answers</summary>

1. A breaking compatibility change under SemVer.
2. A Git tag names source; an image digest identifies exact image content.
3. The changelog spans history; notes explain one release.
4. Commit text may omit user impact, migrations, risks, and known issues.
5. Between pyproject, Helm chart/app version, runtime default, and image tags.

</details>

## Navigation

- [Back to Continuous Delivery and Releases](../README.md)
- [Previous: Build Once, Deploy Many, and Artifact Promotion](../03-build-once-deploy-many-and-artifact-promotion/)
- [Next: Approvals, Release Windows, and Change Controls](../05-approvals-release-windows-and-change-controls/)
- [Back to All Learning Materials](../../README.md)
