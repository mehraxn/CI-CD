# Continuous Deployment

## Definition

Continuous deployment is the practice of allowing every eligible change that passes the automated delivery pipeline to reach production without a required manual release step. A team may deploy many times per day or less often; frequency alone does not define the practice. The deciding feature is that a qualifying change can progress automatically into production.

Continuous deployment depends on continuous integration. Changes must be integrated in small batches and verified quickly. It also uses the capabilities associated with continuous delivery: repeatable artifacts, controlled configuration, environment automation, and release evidence. Continuous deployment changes the last decision point by making production promotion automatic for changes that satisfy policy.

## Simplified Flow

```text
Small change merged
        |
        v
Automated CI checks pass
        |
        v
Immutable artifact is created
        |
        v
Delivery and quality gates pass
        |
        v
Automatic production deployment
        |
        v
Health checks and monitoring
        |
        +---- problem ----> rollback or roll-forward
```

"Automatic" does not mean uncontrolled. Eligibility rules, protected branches, tests, security checks, deployment policies, health checks, and monitoring determine whether a change proceeds.

## Trust and Quality Gates

Removing required manual release approval transfers more responsibility to automated evidence. Tests must cover the important behavior and remain stable. Static analysis, dependency checks, artifact scanning, policy checks, and deployment validation can add confidence. A quality gate should have a clear purpose and a reliable result; adding many noisy checks can reduce trust instead of increasing it.

No test suite can prove that production will be perfect. Deployment safety therefore combines prevention with limited exposure, detection, and recovery. Teams need meaningful service-level signals, alerts with responsible owners, and enough context to connect an incident to a version.

## Small Batches and Feature Flags

Small changes limit the amount of uncertainty in each deployment. They are easier to review, observe, and correct. Feature flags can separate deployment from feature release: code may reach production while behavior remains disabled or is enabled for a controlled group. Flags also introduce configuration and cleanup work; obsolete flags should not remain indefinitely.

Progressive techniques such as canary delivery can expose a new version to a small share of traffic before wider rollout. That is compatible with continuous deployment when automated policy evaluates health and controls expansion.

## Recovery: Rollback and Roll-Forward

A rollback restores a previous known-good application version. It can be fast when artifacts are immutable and data remains backward compatible. A roll-forward deploys a corrective change. Roll-forward may be safer when a database migration or external side effect cannot be reversed cleanly.

Teams should test recovery paths, not just document them. Database changes often need an expand-and-contract approach so old and new application versions can coexist during rollout and recovery. Monitoring must confirm whether the chosen response actually restores service.

## Benefits and Risks

Continuous deployment shortens the time between a verified change and user feedback. Small automated releases reduce large release events and can expose integration assumptions quickly. The process also encourages investment in repeatability and observability.

The risks are real. A flawed check, compromised pipeline, unsafe migration, or misleading health signal can send a problem directly to users. High deployment volume can overwhelm support or make changes hard to correlate if version tracking is weak. Automation must use least privilege and protect production credentials.

## When It Fits - and When It May Not

Continuous deployment can suit services with strong automated coverage, independent release paths, good observability, reversible changes, and teams able to respond quickly.

Full automatic production release may be difficult for:

- strictly regulated systems with required human authorization;
- high-risk changes whose consequences cannot be contained;
- hardware-dependent releases with limited test facilities;
- coordinated mobile-store releases controlled by external review;
- products requiring manual legal or compliance approval;
- systems with weak automated test coverage; or
- services with poor observability and untested recovery.

Continuous delivery is often the safer target in these cases. Continuous deployment is not automatically more mature or better; the release model should match risk and constraints.

## Common Mistakes

- Calling frequent manual deployments continuous deployment.
- Removing approvals before automated evidence is trustworthy.
- Deploying large batches that are hard to diagnose or reverse.
- Watching only whether a process is running instead of user-relevant health.
- Assuming every database change can be rolled back.
- Using feature flags without ownership or cleanup.
- Allowing the deployment identity more permission than it needs.

## Existing Project Example

The [TaskOps CD workflow](../../../Projects/1_project/taskops-cicd/.github/workflows/cd.yml) deploys after pushes to `main` pass its verification and image-scan work. It then runs a health smoke test. This demonstrates an automatic production path in repository configuration. Whether the surrounding organization operates full continuous deployment also depends on branch rules, environment configuration, credentials, and operational response that are not all visible here.

KubeOps publishes images automatically from `main`, but its workflow comments say Argo CD handles deployment. Image publication alone is not continuous deployment to production.

## Practical Exercise

Spend 20 minutes drawing the TaskOps automatic path. Mark one preventive gate, one detection mechanism, and one recovery file such as [the rollback script](../../../Projects/1_project/taskops-cicd/scripts/rollback.sh). Write two questions you would answer before enabling the path for a high-risk service. Do not deploy or run recovery commands.

## Knowledge Check

1. What distinguishes continuous deployment from deploying frequently?
2. Why does continuous deployment require strong observability?
3. When can roll-forward be safer than rollback?
4. Why is continuous delivery sometimes the better operating model?

<details>
<summary>View answers</summary>

1. Eligible changes can reach production without a required manual release step.
2. Automated release needs rapid, reliable evidence of production health and a way to identify regressions.
3. When data or external side effects cannot safely return to the previous state.
4. Risk, regulation, hardware, external stores, or mandatory business approvals may require a deliberate production decision.

</details>

## Navigation

- [Back to CI/CD Fundamentals](../README.md)
- [Previous: Continuous Delivery](../02-continuous-delivery/)
- [Next: CI vs. Delivery vs. Deployment](../04-ci-vs-delivery-vs-deployment/)
- [Back to All Learning Materials](../../README.md)
