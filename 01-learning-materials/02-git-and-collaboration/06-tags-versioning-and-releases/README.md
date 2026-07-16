# Tags, Versioning, and Releases

## Git Tags

A Git tag is a named reference typically used to identify a specific commit that should not move, such as a release. A branch name advances as commits are added; a release tag should remain attached to the commit it originally identified.

A **lightweight tag** is primarily a name pointing to an object. An **annotated tag** is a separate Git object with a tagger, date, message, and target. Annotated tags are generally better release markers because they carry intent. A **signed tag** adds cryptographic verification by a key or supported identity mechanism; a valid signature confirms signing identity, not software quality.

## Basic Commands

```bash
git tag
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
git show v1.0.0
```

- `git tag` lists local tags.
- `git tag -a ...` creates an annotated tag at `HEAD` unless another commit is supplied.
- `git push origin v1.0.0` publishes that one tag. Tags are not always pushed with normal branches.
- `git show v1.0.0` displays the tag information and referenced commit.

Confirm the commit and run required release checks before tagging. Do not push a practice tag to this repository. Moving a published release tag damages traceability and should be avoided.

## Tags as Pipeline Triggers

CI/CD platforms can start a workflow when a matching tag is pushed. A pattern such as `v*` can initiate packaging or release publication. The pipeline should still validate that the tag matches project policy and that the referenced commit is eligible.

The existing project workflows do not use a version-tag trigger. TaskOps and KubeOps release work starts from `main`, and KubeOps also permits manual dispatch. A tag-triggered release remains a later implementation exercise.

## Semantic Versioning

Semantic Versioning uses `MAJOR.MINOR.PATCH` for a public interface:

- increase **MAJOR** for incompatible changes;
- increase **MINOR** for backward-compatible functionality; and
- increase **PATCH** for backward-compatible fixes.

Examples:

```text
v1.0.0       first stable 1.x release
v1.1.0       backward-compatible feature after 1.0.0
v1.1.1       backward-compatible fix after 1.1.0
v2.0.0       incompatible interface change
v2.0.0-rc.1  first release candidate for 2.0.0
```

The leading `v` is a tag convention and is not part of the semantic version itself. Pre-release identifiers such as `-rc.1` have lower precedence than the associated normal version. Build metadata, such as `1.1.1+build.42`, can identify a build but does not change version precedence.

Semantic Versioning requires a defined public interface. For an internal service, the team must decide whether that interface includes APIs, events, configuration, or deployment contracts. Version numbers should communicate compatibility rather than marketing importance.

## Changelogs, Release Notes, and Hosted Releases

A changelog is a maintained record of notable changes across versions. Release notes describe one release for users, operators, or developers and may include upgrades, known issues, and migration actions. Automatically generated commit lists can help, but raw messages often need curation.

A GitHub release is hosting-platform metadata associated with a Git tag. It can contain notes and release artifacts. The Git tag identifies source history; the hosted release provides a distribution and communication page. Other platforms offer related features under different names.

## Release Artifacts and Immutable References

A release should connect source tag, commit, build evidence, and artifacts. A container image tagged with the commit SHA or addressed by digest is traceable. A mutable convenience tag such as `latest` can point to different content tomorrow, so it should not be the only production reference.

The [TaskOps CD workflow](../../../Projects/1_project/taskops-cicd/.github/workflows/cd.yml) and [KubeOps image release](../../../Projects/2_project/kubeops-gitops/.github/workflows/image-release.yml) publish both `latest` and `${{ github.sha }}` tags. The SHA tag supplies the stronger historical connection. For stricter immutability, a deployment can record the image digest returned by the registry.

## Basic Release Workflow

1. Confirm the intended commit is reviewed and required checks pass.
2. Decide the next version from compatibility impact.
3. Prepare and review release notes and migrations.
4. Create an annotated tag at the eligible commit.
5. Push the tag to start or associate release automation.
6. Build or locate the immutable artifact according to the pipeline design.
7. Publish notes and artifacts.
8. Record deployment and monitor results.

If the pipeline follows build-once promotion, the tag should identify the already verified source and artifact relationship rather than cause inconsistent rebuilds for each environment.

## Common Mistakes

- Reusing or moving a published release tag.
- Using `latest` as the only production identity.
- Increasing versions without a defined compatibility policy.
- Publishing a tag before its commit passes required evidence.
- Treating a hosted release page as the artifact itself.
- Generating release notes that omit user-visible risks or migrations.

## Practical Exercise

In a disposable local repository, create and inspect an annotated tag such as `v0.1.0`. Do not push it. Compare `git show v0.1.0` with the branch log, then explain why the tag should remain fixed.

## Knowledge Check

1. How does a tag differ from a branch?
2. Why are annotated tags useful for releases?
3. What changes normally require major, minor, and patch increments?
4. Why should `latest` not be the only production reference?

<details>
<summary>View answers</summary>

1. A branch normally moves as work advances; a release tag should permanently name one commit.
2. They record tagger, date, message, and target, and can also be signed.
3. Incompatible, backward-compatible feature, and backward-compatible fix changes respectively.
4. It is mutable and cannot reliably identify the exact historical artifact deployed.

</details>

## Navigation

- [Back to Git and Collaboration](../README.md)
- [Previous: Branching Strategies](../05-branching-strategies/)
- [Next: Protected Branches and Merge Rules](../07-protected-branches-and-merge-rules/)
- [Back to All Learning Materials](../../README.md)
