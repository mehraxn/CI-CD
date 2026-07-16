# Manual Approvals and Quality Gates

## Two Different Controls

A **quality gate** is any required condition that must be satisfied before a pipeline continues. Gates come in two fundamentally different forms:

```text
Automated quality gate:
A machine-evaluated rule that passes or fails based on measurable results.

Manual approval:
A human decision that allows or rejects the next pipeline action.
```

Automated gates are fast, consistent, and available at any hour, but they can only evaluate what is measurable. Manual approvals can weigh context a machine cannot see — business timing, customer commitments, incident status — but they are slow, inconsistent, and vulnerable to habit. A well-designed pipeline uses automated gates for everything measurable and reserves human decisions for judgment that genuinely requires a person.

## Where Gates Sit in a Pipeline

```text
Build
  ↓
Unit tests
  ↓
Integration tests
  ↓
Security scan
  ↓
Deploy to staging
  ↓
Smoke tests
  ↓
Manual production approval
  ↓
Deploy to production
```

Every arrow is a potential gate: the next action starts only if the previous evidence is acceptable. In continuous delivery, the final production step commonly waits for a human decision. In continuous deployment, that decision is replaced by strong automated gates, and every change that passes them reaches production without a person in the loop.

## Common Automated Gates

- All required tests pass.
- Code coverage is above an agreed threshold.
- No disallowed critical vulnerability is detected.
- The artifact signature is valid.
- The infrastructure plan passes policy checks.
- Staging smoke tests succeed.

Related gate families include **test gates**, **coverage gates**, **security gates**, **policy gates** (rules about configuration or infrastructure), **compliance gates** (regulatory evidence), **artifact-verification gates** (checksums, signatures, provenance), and **release-readiness gates** (changelog present, version tagged, migration reviewed).

Each gate should have a clear purpose tied to a real risk. A gate that exists only because "the company has always done it that way" adds delay without adding safety, and teams quickly learn to work around it.

## Common Human Controls

- **Code-review approvals** gate the merge, before any deployment pipeline runs.
- **Environment approvals** gate a deployment job until designated reviewers accept it.
- **Required reviewers** and **deployment protection rules** are platform settings that enforce who may approve which environment.
- **Approval separation** (separation of duties) requires that the person who wrote a change is not the only person who approves its release. This matters for both error-catching and audit requirements.

Good approval systems leave an **audit trail**: who approved, when, and for which exact commit or artifact. They also define an **approval timeout** (what happens if nobody responds), the effect of a **rejection** (the run fails or is cancelled, not silently skipped), and an **emergency bypass** or **break-glass procedure** — a documented, logged way to ship an urgent fix when normal approvers are unavailable. A bypass that is undocumented will be improvised badly during an incident.

## Conceptual Example

In GitHub Actions, a manual approval is not written as a step. A job references a named environment, and reviewer requirements attached to that environment pause the job until approval:

```yaml
jobs:
  deploy-production:
    needs:
      - test
      - security-scan
    environment: production
    runs-on: ubuntu-latest

    steps:
      - name: Deploy
        run: echo "Deploy after environment approval"
```

The reviewers themselves are configured in repository or environment settings, not in the YAML. This lesson does not change any repository settings; the example is conceptual. GitLab CI/CD uses `when: manual` jobs and protected environments, Jenkins uses an `input` step, and Azure Pipelines uses environment checks and approvals — the concept is the same, the syntax differs.

## Limitations of Simplistic Gates

- A coverage percentage does not prove test quality; it proves lines were executed.
- A vulnerability severity score may need context — an unreachable code path with a critical CVE may matter less than a medium issue on the login path.
- A green pipeline does not prove the software has no defects; it proves the encoded checks passed.
- A manual approval does not automatically make a deployment safe; an uninformed click adds delay, not protection.
- Too many approvals delay feedback and encourage careless rubber-stamping — **approval fatigue** turns a control into a ritual.

A useful counter to approval fatigue is **risk-based approval**: routine, low-risk changes flow through automated gates alone, while schema migrations, security-sensitive changes, or first deployments of a new service get human review. When approvals block everything equally, they protect nothing well.

## When to Use Which

Manual approvals are appropriate when a release has business timing constraints, when regulation demands a recorded human decision, or when automated verification is still too weak to trust alone. They become unnecessary bottlenecks when they merely restate what automation already verified. Many teams begin with a production approval and remove it as their automated gates earn trust — that is the practical road from continuous delivery to continuous deployment.

## Existing Workflow Evidence

- [TaskOps CI](../../../Projects/1_project/taskops-cicd/.github/workflows/ci.yml) implements automated gates: lint and format checks, `pytest`, Bandit, `pip-audit`, and a Trivy image scan configured with `exit-code: "1"` on HIGH/CRITICAL findings — a security gate that fails the job, plus a smoke-test gate against the running container.
- [TaskOps CD](../../../Projects/1_project/taskops-cicd/.github/workflows/cd.yml) re-runs the quality gates in a `verify` job that the `deploy` job `needs`, and scans the image again before pushing — a gate between build and publication.
- [KubeOps CI](../../../Projects/2_project/kubeops-gitops/.github/workflows/ci.yml) applies the same style of automated test and scan gates in one job.

The repository does not currently demonstrate manual environment approvals, coverage thresholds, or policy-as-code gates. Those are shown conceptually above and may be added during a later practical enhancement; do not change workflow files or repository settings now.

## Common Mistakes

- Adding approvals to compensate for missing automated tests.
- Letting one person both author and approve every release.
- Keeping gates whose purpose nobody can state.
- Treating an approval click as evidence of safety.
- Having no documented break-glass path for emergencies.
- Measuring gate strictness instead of outcome quality.

## Practical Exercise

Design a gate list for the TaskOps project (do not change any settings or workflows). Produce two columns: automated gates (name each check and the exact evidence it evaluates, using the real CI/CD files) and proposed manual approvals (state who should approve, for which action, and why a machine cannot decide it). Mark any current gate you believe is missing or redundant, with one sentence of justification. Target 20–30 minutes.

## Knowledge Check

1. What is the difference between an automated quality gate and a manual approval?
2. Why does a high coverage percentage not guarantee good tests?
3. What is separation of duties in a release process?
4. What is approval fatigue and why is it dangerous?
5. When does a manual production approval stop being useful?

<details>
<summary>View answers</summary>

1. An automated gate is a machine-evaluated pass/fail rule based on measurable results; a manual approval is a human decision to allow or reject the next action.
2. Coverage proves lines were executed, not that assertions were meaningful or edge cases were tested.
3. The person who authored a change is not the only person who approves releasing it, improving error-catching and auditability.
4. Frequent low-value approval requests train reviewers to click through without evaluating, turning the control into a ritual.
5. When it merely restates what automated gates already verified, adding delay without adding judgment.

</details>

## Navigation

- [Back to Pipeline Architecture](../README.md)
- [Previous: Matrix Builds and Parallelism](../05-matrix-builds-and-parallelism/)
- [Next: Retries, Timeouts, Cancellation, and Failures](../07-retries-timeouts-cancellation-and-failures/)
- [Back to All Learning Materials](../../README.md)
