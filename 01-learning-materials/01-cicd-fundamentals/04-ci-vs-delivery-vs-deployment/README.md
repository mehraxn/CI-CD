# CI vs. Continuous Delivery vs. Continuous Deployment

## Why the Distinction Matters

Continuous integration, continuous delivery, and continuous deployment describe connected but different scopes. Using the terms precisely helps a team understand what is automated, what evidence exists, and who or what decides that a change reaches production.

CI focuses mainly on integrating and verifying source changes. Continuous delivery extends the automated path so a candidate remains ready to release. Continuous deployment allows a qualifying candidate to enter production without a required manual release action.

## Comparison

| Area | Continuous Integration | Continuous Delivery | Continuous Deployment |
|------|------------------------|---------------------|-----------------------|
| Main goal | Integrate and verify changes frequently | Keep verified software releasable | Release every eligible change automatically |
| Typical endpoint | A verified shared branch or build | A production-ready candidate | A monitored production deployment |
| Production release | Outside CI's required scope | Available on demand | Part of the automatic path |
| Manual approval | May govern merges, not defined by CI | Commonly allowed before production | No required manual production-release step |
| Required automation | Build and change verification | CI plus packaging, promotion, and environment validation | Delivery automation plus automatic production promotion and response controls |
| Feedback focus | Code, build, and integration problems | Release readiness and environment behavior | Production behavior and user impact as well as earlier feedback |

Terminology differs among organizations. Some use "CD" without saying whether they mean delivery or deployment. Ask where the automated path ends and whether a person must authorize production.

## How the Practices Build on One Another

```text
Continuous integration
  integrate + verify
          |
          v
Continuous delivery
  package + validate + remain releasable
          |
          v
Continuous deployment
  automatically release eligible changes
```

An organization can practice CI without mature continuous delivery. It might validate every pull request but package releases by hand once a month. That is still useful CI, but the manual and infrequent release process limits delivery capability.

Continuous deployment normally depends on strong CI and delivery practices. Automatically deploying poorly integrated source or rebuilding unverified artifacts would make failure faster, not delivery safer. Continuous deployment also needs production monitoring and recovery because no pre-production evidence is complete.

## Three Decision Boundaries

Think about three questions:

1. **Has the source change integrated safely?** CI provides automated evidence about the shared codebase.
2. **Could this exact candidate be released now?** Continuous delivery provides a versioned artifact, environment evidence, and a repeatable production path.
3. **Does it proceed without required manual release approval?** If yes, the organization may be practicing continuous deployment for that path.

A pipeline can contain all three scopes. The labels describe practices and decision boundaries, not necessarily three separate files.

## Project-Based Illustration

The [TaskOps CI workflow](../../../Projects/1_project/taskops-cicd/.github/workflows/ci.yml) verifies pull requests and `main` pushes. Its [CD workflow](../../../Projects/1_project/taskops-cicd/.github/workflows/cd.yml) verifies again, produces and scans an image, publishes it, deploys it, and smoke-tests the result after a push to `main`. The repository therefore provides examples of integration checks and an automatic deployment path.

The [KubeOps CI workflow](../../../Projects/2_project/kubeops-gitops/.github/workflows/ci.yml) explicitly does not deploy. The [image-release workflow](../../../Projects/2_project/kubeops-gitops/.github/workflows/image-release.yml) publishes images from `main` or a manual dispatch. Argo CD configuration exists separately. This demonstrates why artifact publication and production deployment should not be treated as synonyms.

## Practical Scenarios

Identify the main practice represented by each scenario. A real system can practice more than one, but choose the most specific description supported by the text.

1. Every pull request runs linting, unit tests, and a build. After merge, a release engineer manually packages and deploys the application.
2. Every merge produces one versioned package, automatically validates it in test and staging, and leaves a production approval button ready for the product owner.
3. Every eligible merge passes automated gates, enters production without a required approval, and is monitored for automatic rollback criteria.

<details>
<summary>View answers</summary>

1. **Continuous integration.** The change is integrated and verified, but release preparation remains manual.
2. **Continuous delivery.** The software is kept releasable, while production remains an explicit business decision.
3. **Continuous deployment.** Qualifying changes progress automatically into production.

</details>

## Common Classification Errors

- A nightly build is not necessarily CI if changes remain separate for long periods.
- A test pipeline is not automatically continuous delivery if it produces no releasable candidate.
- Publishing an artifact is not the same as deploying it to production.
- A scheduled automatic production rollout can be deployment automation, but it is not necessarily continuous deployment if each candidate requires manual selection.
- Continuous deployment does not remove gates; it makes the qualifying and release decision executable by policy.

## Practical Exercise

In 15 minutes, select one existing project workflow and mark its endpoint: verified source, published candidate, or deployed service. Cite the exact job or step that supports your conclusion. Record anything that cannot be known from repository files instead of guessing.

## Knowledge Check

1. Can an organization practice CI without continuous delivery?
2. What manual step is compatible with continuous delivery but not full continuous deployment?
3. Why does continuous deployment normally depend on delivery practices?
4. Is automatic image publication proof of production deployment?

<details>
<summary>View answers</summary>

1. Yes. It may integrate and verify frequently while packaging or deployment remains manual.
2. Required manual authorization of the production release.
3. It needs the repeatable artifacts, environment validation, and release controls that make automatic promotion trustworthy.
4. No. Publication stores an artifact; a separate mechanism must change the production environment.

</details>

## Navigation

- [Back to CI/CD Fundamentals](../README.md)
- [Previous: Continuous Deployment](../03-continuous-deployment/)
- [Next: Pipeline Anatomy](../05-pipeline-anatomy/)
- [Back to All Learning Materials](../../README.md)
