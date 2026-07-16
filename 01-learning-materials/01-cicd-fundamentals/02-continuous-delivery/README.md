# Continuous Delivery

## Definition

Continuous delivery is the practice of keeping software in a verified, releasable state through automated build, test, packaging, and environment-deployment steps. The team can release an eligible version to production at any time, but the final production action may require a person to approve it or a business to choose the release time.

Continuous delivery builds on continuous integration. CI provides confidence in integrated source changes. Delivery extends the path so the software is packaged consistently, deployed to representative environments, and evaluated as a release candidate. Merely running tests after a commit is useful CI, but it is not a complete delivery process.

## A Simplified Delivery Pipeline

```text
Commit
  |
  v
Continuous integration checks
  |
  v
Create versioned artifact
  |
  v
Deploy automatically to test
  |
  v
Deploy automatically to staging
  |
  v
Validate release candidate
  |
  v
Manual production approval
  |
  v
Production deployment
```

Some organizations use fewer environments; others add security, performance, compliance, or change-management gates. The essential point is that the candidate is ready and the remaining production decision is explicit.

## Releasable State

Releasable software has passed agreed checks and has a known deployment path. Documentation, configuration, migration compatibility, security findings, and operational readiness may all affect that state. A green unit-test job alone is insufficient if packaging is broken or the application cannot run with production-like configuration.

A release candidate is a specific artifact considered for release. It should be identifiable by an immutable version, commit hash, or digest. If staging validation succeeds, that same artifact should move to production. This is the **build once, deploy many** principle. Rebuilding from source for production can resolve different dependencies or introduce a different binary, weakening the evidence collected in staging.

## Artifact and Environment Promotion

Artifact promotion advances one verified output through environments instead of rebuilding it. Environment-specific values - endpoints, capacity, feature settings, and secrets - are supplied separately. Promotion records should answer what version moved, where it moved, which checks passed, and who or what authorized the move.

A staging environment should be similar enough to production to reveal meaningful deployment and integration problems. Exact duplication is not always economical, but important runtime versions, interfaces, and deployment mechanics should be representative. Temporary preview environments can add earlier feedback without replacing staging controls.

## Approvals and Business Decisions

A manual production approval is not evidence that delivery is incomplete. It can represent a planned launch, support staffing, a customer commitment, a maintenance window, or a regulated authorization. The technical system should keep the approved candidate ready and make the action repeatable.

Approvals should not compensate for an unreliable pipeline. If a person must manually repeat every automated check or repair every deployment, the software is not continuously deliverable in a meaningful sense.

## Benefits and Limitations

Continuous delivery reduces release surprises, makes smaller releases practical, and turns deployment into a routine operation. Versioned candidates improve auditability and rollback planning. Teams can choose release timing without waiting for a special stabilization project.

It requires investment in test reliability, environment automation, configuration management, artifact storage, and operational readiness. Environment differences can still hide failures. Manual approval queues may become bottlenecks. Delivery also does not guarantee that a released feature creates user value.

## Common Mistakes

- Rebuilding the application separately in each environment.
- Using mutable names as the only artifact reference.
- Calling test execution "delivery" without packaging or deployment readiness.
- Treating staging as an unrelated configuration that provides weak evidence.
- Allowing manual, undocumented repair steps in every release.
- Promoting an artifact when required evidence has failed or expired.
- Confusing an approval decision with a manual technical deployment procedure.

## Existing Project Example

The [TaskOps CD workflow](../../../Projects/1_project/taskops-cicd/.github/workflows/cd.yml) rechecks quality, builds and scans an image, pushes tags based on the commit SHA and `latest`, deploys over SSH, and runs a post-deployment health test. It demonstrates several delivery mechanisms, but it currently deploys automatically after a push to `main`; it does not show a staging environment or a production approval gate.

The [KubeOps image-release workflow](../../../Projects/2_project/kubeops-gitops/.github/workflows/image-release.yml) publishes a commit-SHA image plus `latest`. The project separates image creation from GitOps deployment. A later practical exercise can add a documented promotion model; this lesson does not claim one already exists.

## Practical Exercise

In 20 minutes, trace the immutable and mutable image tags in either release workflow. Draft a five-row promotion record containing commit, artifact reference, environment, evidence, and approval. Do not publish an image or deploy anything.

## Knowledge Check

1. How does continuous delivery extend CI?
2. Why should staging and production receive the same artifact?
3. Can continuous delivery include manual production approval?
4. Why is a successful test job not enough to prove release readiness?

<details>
<summary>View answers</summary>

1. It adds repeatable packaging, environment deployment, release-candidate validation, and release readiness.
2. Rebuilding could produce different contents and invalidate earlier evidence.
3. Yes. The candidate remains releasable while the final release timing can be a human or business decision.
4. Packaging, configuration, deployment, security, migration, and operational concerns may remain unverified.

</details>

## Navigation

- [Back to CI/CD Fundamentals](../README.md)
- [Previous: Continuous Integration](../01-continuous-integration/)
- [Next: Continuous Deployment](../03-continuous-deployment/)
- [Back to All Learning Materials](../../README.md)
