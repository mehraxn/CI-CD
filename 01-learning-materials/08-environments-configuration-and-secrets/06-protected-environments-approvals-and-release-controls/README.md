# Protected Environments, Approvals, and Release Controls

## Gating the Path to Production

A **protected environment** is a named deployment target with rules attached: **required reviewers** (manual approval before the job runs), **wait timers**, **deployment branch policies** (only `main`, or only release tags may deploy here), and **environment-specific secrets and variables** released only to approved runs. The controls compose into a release path:

```text
Verified release candidate
          ↓
Protected production environment
          ↓
Required checks
          ↓
Optional required approval
          ↓
Serialized deployment
          ↓
Post-deployment verification
```

In GitHub Actions terms, conceptually:

```yaml
jobs:
  deploy-production:
    needs:
      - test
      - security-scan
    environment: production
    concurrency:
      group: production-deployment
      cancel-in-progress: false
    runs-on: ubuntu-latest

    steps:
      - name: Deploy
        run: echo "Deploy the approved artifact"
```

Reading it honestly: `environment: production` *names* the environment and attaches the job to its rules — but the rules themselves (reviewers, branch policies, wait timers) are **configured in repository settings, outside the workflow file**; this YAML alone proves nothing about whether approval is required. The `concurrency` block serializes production deployments (`cancel-in-progress: false` queues rather than kills — killing a half-finished deployment is how half-updated systems happen; see [failure handling](../../03-pipeline-architecture/07-retries-timeouts-cancellation-and-failures/)). A **deployment lock** is the same idea by another name.

## The Control Vocabulary

- **Approval record and audit trail** — who approved which run of which artifact, kept as evidence; **deployment history** and **environment URLs** make the current state inspectable.
- **Separation of duties** — author ≠ sole approver; a **change-management control** in regulated settings.
- **Release windows and deployment freezes** — times when deployments may or must not happen.
- **Emergency deployment / break-glass** — a documented, logged bypass path; **bypass permissions** must be narrow, because an unrestricted bypass makes every other control decorative.
- **Approval timeout** (what happens when nobody responds) and **rejected deployments** (the run fails visibly, not silently).
- **Rollback control** — production rules apply to rollbacks too; a rollback is a deployment.

## When Approvals Help and When They Harm

Useful: regulated releases, high-risk production changes, business launch coordination, exceptional database changes, emergency or destructive operations — cases where a human weighs context no gate encodes ([Topic 03's gates lesson](../../03-pipeline-architecture/06-manual-approvals-and-quality-gates/) covers the automated/manual split).

Harmful: approval on every low-risk deployment, approvals with no criteria, rubber-stamping, duplicate approvals, approvers without context or evidence, and approval queues that push teams into big risky batches. **Approval fatigue** is the failure mode; **risk-based control** — automation for routine changes, humans for genuinely risky ones — is the remedy.

## Common Mistakes

- Treating approval as proof of correctness.
- Giving approvers no deployment evidence to judge.
- Allowing unrestricted bypass.
- Production secrets available to the job *before* approval.
- Parallel production deployments.
- Manual approval with no audit trail.
- Approving a mutable tag rather than an immutable artifact.
- No rollback identity recorded.
- No emergency policy until the emergency.

## Existing Repository Evidence

No workflow declares `environment:`, so **GitHub protected environments are not currently used** — required reviewers, wait timers, and environment-scoped secrets are all absent, and nothing here claims otherwise. What the repository *does* implement are the surrounding controls:

- **Serialized production deployment**: [TaskOps CD](../../../Projects/1_project/taskops-cicd/.github/workflows/cd.yml) uses a workflow-wide concurrency group with `cancel-in-progress: false` — the deployment lock from the example, real.
- **Branch-limited deployment**: CD triggers only on `push` to `main`, a trigger-level cousin of a deployment branch policy (enforced by the file, not by settings).
- **Required checks before deploy**: the `deploy` job `needs: verify`, which re-runs the full gate suite.
- **Post-deployment verification**: the CD smoke test against the live `/health`.
- **Rollback identity**: the [deploy script](../../../Projects/1_project/taskops-cicd/scripts/deploy.sh) records the previous tag for `rollback.sh`.
- On the GitOps side, [KubeOps' Argo CD Application](../../../Projects/2_project/kubeops-gitops/argocd/application.yaml) uses **manual sync by default** — its comments explain that nothing deploys until a human syncs, which is a manual approval implemented in the delivery tool rather than the CI platform.

Protected GitHub environments with required reviewers may be introduced in a later enhancement phase.

## Practical Exercise

Design production-environment rules for TaskOps on paper (change no settings):

1. Which jobs would attach to a `production` environment, and which secrets would move to environment scope (name them from CD)?
2. Deployment branch policy, reviewer count, and who may review given separation of duties in a small team.
3. The evidence an approver should see before approving (think: which run artifacts and checks).
4. The break-glass procedure: who, how logged, and what follow-up.
5. What the Argo CD manual-sync model already provides for KubeOps, and what it lacks compared to your design (hint: audit trail, reviewer requirements).

Target 25–35 minutes.

## Knowledge Check

1. What does `environment: production` in a workflow actually prove about approvals?
2. Why serialize production deployments instead of cancelling superseded ones?
3. Why should production secrets be unavailable before approval?
4. Why is approving a mutable tag a mistake?
5. What real manual-approval mechanism exists in this repository, and where does it live?
6. What turns approvals from control into ritual?

<details>
<summary>View answers</summary>

1. Only that the job references an environment name; reviewer and branch rules live in repository settings, invisible in the YAML.
2. Cancelling mid-deployment can leave the system half-updated; queueing lets each deployment finish atomically.
3. If the job holds them pre-approval, the approval gates nothing — the code that runs before the gate already had production access.
4. The tag can point at different bytes by deploy time; approval should bind to a digest, or to a SHA tag that registry policy makes non-overwritable, to identify the approved bytes.
5. Argo CD's manual sync for KubeOps — deployment happens only when a human syncs, a manual approval implemented in the GitOps tool.
6. Fatigue: approving everything regardless of risk, without criteria or evidence, until reviewers click through automatically.

</details>

## Navigation

- [Back to Environments, Configuration, and Secrets](../README.md)
- [Previous: OIDC, Workload Identity, and Short-Lived Credentials](../05-oidc-workload-identity-and-short-lived-credentials/)
- [Next: Configuration Validation, Drift, and Cleanup](../07-configuration-validation-drift-and-cleanup/)
- [Back to All Learning Materials](../../README.md)
