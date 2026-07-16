# Conditions and Filters

## Why Conditional Behavior Exists

Pipelines serve several events, branches, environments, and outcomes. Conditions prevent irrelevant work and protect sensitive actions. They must remain readable: a pipeline full of nested expressions becomes difficult to test and unsafe to change.

**Trigger filters** decide whether an event creates a workflow run. **Runtime conditions** decide whether a workflow, job, or step inside an existing run executes. Filtering a push to `main` through `on` can avoid a run entirely. A job-level `if` allows the run to exist but skips that job when its expression is false.

## Conditional Inputs

Conditions can examine:

- branch or tag references;
- event type and event payload;
- manual inputs;
- environment or repository context;
- earlier step or job outputs;
- success, failure, or cancellation status;
- boolean or string values.

Boolean expressions use comparisons, logical AND/OR, and negation. Operator precedence can be easy to misread, so use parentheses where supported or split complicated logic into named jobs or outputs. Strings are not booleans: an input containing the text `false` may still be a non-empty string unless converted according to platform rules.

Do not expose secrets merely to evaluate ordinary branch logic. Some platforms restrict secrets in expression contexts. More importantly, a condition based on attacker-controlled data must not unlock privileged credentials.

## Branch-Based Example

```yaml
name: Conditional Pipeline

on:
  push:
    branches:
      - main
      - develop

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Run tests"

  deploy-staging:
    needs: test
    if: github.ref == 'refs/heads/develop'
    runs-on: ubuntu-latest
    steps:
      - run: echo "Deploy to staging"

  deploy-production:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - run: echo "Deploy to production"
```

The trigger admits only pushes to two branches. Once a run exists, the job conditions select one deployment path. GitHub branch context uses the full reference shown here; comparing only `main` would be incorrect for `github.ref`. Equivalent platforms use different reference fields and syntax.

A step-level condition can select one command inside a job. An output-based condition can wait for an upstream decision, such as whether a package changed. Outputs must be declared and absent-output behavior understood.

## Status Conditions

```yaml
if: success()
```

Runs when required earlier work is successful. This is close to normal default behavior.

```yaml
if: failure()
```

Runs when relevant earlier work failed, useful for diagnostic collection or failure notification.

```yaml
if: always()
```

Requests execution regardless of success or failure, and requires careful cancellation analysis.

```yaml
if: cancelled()
```

Targets cancellation behavior.

```yaml
cleanup:
  needs:
    - test
  if: always()
  runs-on: ubuntu-latest
  steps:
    - run: echo "Clean temporary resources"
```

The cleanup job can run after a failed test because `always()` changes ordinary dependency status behavior. It must tolerate missing outputs and partially created resources. An always-running operation can still be harmful if it deploys, publishes, or deletes based on assumptions that failed work never established.

## Skips and Dependencies

A false condition produces a skipped job or step, not proof of successful verification. Downstream dependency behavior around skipped jobs varies with conditions. If a required quality job is conditional, the fan-in design must say what a skip means.

Default execution generally stops later steps after failure and skips downstream jobs after failed needs. Explicit status functions override parts of that behavior. Test rare paths: feature branch, tag, manual input, failure, cancellation, and absent output.

## Deployment Safety

Use multiple layers for sensitive deployments: narrow triggers, protected source references, explicit job conditions, required evidence, environment protection, and least-privilege credentials. A branch-name expression alone is not authorization. Forks or user-controlled references can use convincing names.

## Existing Workflow Evidence

[TaskOps CI](../../../Projects/1_project/taskops-cicd/.github/workflows/ci.yml) uses `if: always()` for its container-stop step so cleanup is attempted after smoke-test failure. It also uses `needs: quality`, showing how status and dependency behavior interact. TaskOps CD shell scripts use failure controls, but its jobs do not have branch expressions because the workflow trigger already filters `main`.

The workflows do not currently demonstrate separate staging/production job conditions or output-based conditions.

## Common Mistakes

- Replacing clear architecture with unreadable expressions.
- Deploying from a feature branch due to an incorrect reference comparison.
- Treating a skipped gate as a passed gate.
- Confusing an event filter with a job condition.
- Using secrets in unsupported or unsafe expression contexts.
- Assuming upstream outputs exist after failure or skip.
- Failing to test rare condition branches.
- Applying `always()` without considering cancellation and side effects.

## Practical Exercise

Write a non-executed Markdown YAML example that runs tests on pull requests, deploys staging only from `develop`, and deploys production only from `main`. Label which rules are trigger filters and which are job conditions. Do not add it to `.github/workflows`.

## Knowledge Check

1. How does trigger filtering differ from a job condition?
2. What does a false job condition produce?
3. Why must cleanup tolerate missing outputs?
4. Is checking a branch name sufficient production authorization?
5. Why can `always()` be dangerous?

<details>
<summary>View answers</summary>

1. A filter can prevent a run; a job condition acts inside a created run.
2. A skipped job, not a successfully verified job.
3. Earlier work may fail or be cancelled before creating them.
4. No. Protected references, permissions, gates, and environment controls are also needed.
5. It can run side-effecting work after failure or during cancellation unless designed carefully.

</details>

## Navigation

- [Back to Pipeline Architecture](../README.md)
- [Previous: Job Dependencies and DAG Pipelines](../03-job-dependencies-and-dag-pipelines/)
- [Next: Matrix Builds and Parallelism](../05-matrix-builds-and-parallelism/)
- [Back to All Learning Materials](../../README.md)
