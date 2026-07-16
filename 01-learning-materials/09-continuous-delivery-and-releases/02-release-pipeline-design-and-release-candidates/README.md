# Release Pipeline Design and Release Candidates

## Candidate to Production

A **delivery pipeline** moves verified changes toward deployability. A **release pipeline** adds candidate selection, target progression, release evidence, and production decisions.

```text
Build candidate
      ↓
Automated quality checks
      ↓
Security checks
      ↓
Deploy candidate to staging
      ↓
Acceptance and smoke testing
      ↓
Approve or reject candidate
      ↓
Deploy the same candidate to production
```

A **release candidate** is an exact candidate artifact and version, not merely a branch. It should identify source revision, artifact/image digest, dependencies, test and security evidence, target compatibility, and deployment inputs.

| Evidence | Purpose |
|----------|---------|
| Commit SHA | Exact source identity |
| Artifact digest | Exact build identity |
| Test report | Verification evidence |
| Security report | Risk evidence |
| Release notes | Human-readable change summary |
| Deployment configuration | Target-environment context |

## Triggers, Stages, and Ownership

Candidates may come from mainline, a release branch, a Git tag, manual trigger, schedule, or **release train**. A release window permits deployment during a planned interval; a freeze period restricts ordinary change. These mechanisms select timing, not quality.

Verification stages commonly include unit and integration checks, security and compliance validation, staging deployment, acceptance tests, and smoke tests. A promotion gate evaluates evidence. Failure handling must name the pipeline owner, preserve diagnostics, reject the candidate clearly, and decide whether a corrected artifact becomes a new candidate. Reusing a failed identity hides history.

Environment progression should narrow risk: test → staging → production. Staging must be relevant enough for evidence to transfer, while environment-specific configuration remains outside the artifact.

The candidate version should be unique and stable. Candidate replacement means creating a new candidate identity after content changes; candidate rejection preserves the original evidence and failure reason. A pipeline may allow a retry when only a transient environment failed, but it must not quietly substitute new bytes under the old identity.

Deployment inputs deserve the same review as code: target environment, artifact reference, configuration revision, migration mode, and rollout strategy. Free-form manual inputs can select the wrong target or inject unsafe text, so constrained choices and validation are preferable. Scheduled releases and trains need a cutoff policy explaining which verified changes qualify.

Failure handling covers more than stopping. It preserves logs and reports, prevents downstream promotion, announces ownership, releases locks safely, and records whether the candidate remains valid. Pipeline ownership identifies who repairs the automation; product or service ownership identifies who accepts release risk. Compliance validation may add licensing, segregation, evidence retention, or change-record checks, but should reuse existing machine evidence rather than duplicate it manually.

## Existing Repository Evidence

[TaskOps CD](../../../Projects/1_project/taskops-cicd/.github/workflows/cd.yml) creates an informal candidate from a `main` commit, tags it with `github.sha`, scans before push, and deploys that SHA. It has no staging stage, digest record, acceptance report, manual release trigger, or candidate record. [KubeOps image release](../../../Projects/2_project/kubeops-gitops/.github/workflows/image-release.yml) supports `workflow_dispatch`, but defines no inputs and deploys nowhere. Neither is a formal release-candidate pipeline.

## Common Mistakes

- Rebuilding after staging validation.
- Using a branch name as the only identity.
- Giving different artifacts one version.
- Approving without evidence.
- Testing in an unrelated environment.
- Leaving rejected candidates ownerless.
- Reusing a failed candidate without diagnosis.
- Mixing unrelated changes into one candidate.

## Practical Exercise

Design a TaskOps release-candidate record containing commit, proposed version, SHA tag, possible digest, dependencies, verification run, scan result, target configuration, owner, status, and rejection reason. Mark unavailable fields as absent rather than inventing them. Do not release anything.

## Knowledge Check

1. Why is a branch not enough to identify a candidate?
2. What must remain the same after staging approval?
3. What does a promotion gate do?
4. What happens to a rejected candidate?
5. Which candidate evidence is absent from TaskOps today?

<details>
<summary>View answers</summary>

1. Branches move; they do not identify exact source or built content.
2. The exact artifact bytes and immutable identity.
3. It evaluates required evidence and permits or denies progression.
4. Preserve its evidence and reason, then create a new identity for corrected content.
5. A recorded digest, staging evidence, formal version, candidate record, and approval record.

</details>

## Navigation

- [Back to Continuous Delivery and Releases](../README.md)
- [Previous: Delivery, Deployment, and Release](../01-delivery-deployment-and-release/)
- [Next: Build Once, Deploy Many, and Artifact Promotion](../03-build-once-deploy-many-and-artifact-promotion/)
- [Back to All Learning Materials](../../README.md)
