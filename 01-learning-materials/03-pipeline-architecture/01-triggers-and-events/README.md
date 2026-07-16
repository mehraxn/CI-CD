# Triggers and Events

## Three Related Concepts

```text
Event:
Something that happened.

Trigger configuration:
A rule deciding whether that event should start a pipeline.

Pipeline run:
The actual execution created after a trigger matches.
```

A repository can receive many events without starting every workflow. For example, a push to a feature branch is an event. A workflow configured only for pushes to `main` does not match it, so no run is created for that workflow.

## Common Trigger Types

| Trigger type | Typical use | Main risk |
|--------------|-------------|-----------|
| Push | Validate committed changes | Running too often |
| Pull request | Validate changes before merge | Untrusted code |
| Tag | Create a release | Incorrect tag patterns |
| Schedule | Maintenance or periodic checks | Silent failures |
| Manual | Controlled operation | Human error |
| API or webhook | External automation | Authentication and replay risks |

Repository events include pushes, pull or merge requests, tag updates, releases, issue activity, and changes to other hosted objects. CI normally reacts to source-related events. Branch-specific triggers can restrict work to `main`, `develop`, or release branches. Tag filters can select version-shaped tags such as `v*`, but the pipeline must still validate eligibility.

A **release trigger** can respond to hosted release activity, which is not necessarily identical to pushing a Git tag. A **manual trigger** allows an authorized user or API client to request a run, often with inputs. It remains subject to input validation, permissions, and safe pipeline design.

Scheduled triggers support periodic security scans, dependency checks, cleanup, or maintenance. Cron schedules commonly use UTC unless the platform states otherwise. A schedule needs monitoring because no developer may be watching when it fails.

API triggers, webhooks, and repository-dispatch or custom events connect external systems. They require authentication, replay protection where supported, input validation, and least privilege. A custom event name is not a trust guarantee.

## Pull-Request Example

```yaml
name: Pull Request CI

on:
  pull_request:
    branches:
      - main
    paths:
      - "app/**"
      - "tests/**"
      - ".github/workflows/ci.yml"

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Run tests
        run: echo "Run project tests"
```

`pull_request` selects pull-request events. In this context, `branches` filters the target branch, so the workflow matches proposals into `main`. `paths` requires a relevant changed path. Documentation-only changes can sometimes skip expensive application checks, reducing queue time and cost.

Path filtering must reflect real dependencies. A documentation file might feed a published build, or a shared configuration change might affect code outside the listed paths. Careless filters can skip required validation. Critical checks also need predictable reporting; if a required workflow is skipped, repository merge rules must handle that state correctly.

## Manual and Scheduled Example

```yaml
on:
  workflow_dispatch:

  schedule:
    - cron: "0 6 * * 1"
```

`workflow_dispatch` allows manual GitHub Actions execution. The cron expression requests a Monday run at 06:00, normally interpreted in UTC by GitHub Actions. Equivalent capabilities use different syntax on other platforms.

## Filters and Payloads

Branch, tag, and path filters narrow trigger matching. Ignored-path rules invert path selection. Avoid mixing include and ignore rules without understanding platform precedence. A broad trigger followed by a job condition still creates a run; an event filter can prevent the run entirely.

An event payload contains context such as repository, actor, reference, commit, pull-request number, and changed object data. The exact fields depend on the event. Treat payload values as input, especially when branch names, titles, or API fields can be influenced by untrusted users.

## Chaining and Duplicate Runs

Workflow chaining starts a downstream workflow after an upstream workflow or pipeline completes. Parent/child or downstream pipelines can split large systems by responsibility. Preserve source identity and pass only necessary, validated metadata.

One change can accidentally start duplicate work. A branch push may run a broad `push` workflow while its open pull request also runs `pull_request`. TaskOps avoids branch-push duplication by limiting pushes to `main`, while still validating pull requests. Other valid solutions depend on desired coverage.

Avoid unnecessary runs with focused event selection, safe path filters, concurrency cancellation, and separate lightweight versus expensive validation. Optimization must not remove evidence required for merge or release.

## Trigger Security

Forked pull requests run code proposed by someone who may not be trusted. Platforms commonly restrict secrets for these events. Do not change to a more privileged event merely to make a secret available. Be especially careful with mechanisms that run trusted-base workflow code while checking out untrusted source.

A manual trigger is not automatically safe: a user can select the wrong reference or input. A webhook can be forged if authentication is weak. A tag can be pushed by an overly privileged identity. Secure triggers require restricted permissions, validated inputs, protected references, and minimal job credentials.

## Common Mistakes

- Running deployments for every branch.
- Triggering the same validation twice for one change.
- Applying broad or incorrect path filters.
- Forgetting that tag and branch filters have different reference forms.
- Giving untrusted pull-request code access to secrets.
- Assuming a manual request is inherently safe.
- Running expensive pipelines for irrelevant changes.
- Scheduling work without alerting on failure.
- Chaining pipelines without preserving exact source identity.

## Existing Workflow Evidence

[TaskOps CI](../../../Projects/1_project/taskops-cicd/.github/workflows/ci.yml) runs on pull requests and pushes to `main`. [TaskOps CD](../../../Projects/1_project/taskops-cicd/.github/workflows/cd.yml) runs only on pushes to `main`. [KubeOps CI](../../../Projects/2_project/kubeops-gitops/.github/workflows/ci.yml) uses broad push and pull-request events. [KubeOps image release](../../../Projects/2_project/kubeops-gitops/.github/workflows/image-release.yml) combines `main` pushes with `workflow_dispatch`.

The repository does not currently demonstrate schedule, path, tag, release, API, custom-event, or workflow-chain triggers.

## Practical Exercise

In 20 minutes, inspect the four workflows. For each, record the event, branch filter, and whether it can be started manually. Note absent path and schedule filters. Identify one security-sensitive trigger and one possible duplicate-run scenario. Do not edit or execute a workflow.

## Knowledge Check

1. What is the difference between an event and trigger configuration?
2. Why can path filtering be unsafe when dependencies are incomplete?
3. Why are forked pull-request events security-sensitive?
4. Does a manual trigger guarantee a safe operation?
5. How can one change cause duplicate validation?

<details>
<summary>View answers</summary>

1. An event happened; trigger configuration decides whether it creates a run.
2. A change outside the selected paths may still affect the build, so required checks can be skipped.
3. They may execute untrusted proposed code, which must not receive privileged secrets or tokens.
4. No. Reference choice, inputs, permissions, and workflow behavior still require controls.
5. A branch push and its pull-request event can both match broad workflow triggers.

</details>

## Navigation

- [Back to Pipeline Architecture](../README.md)
- [Next: Stages, Jobs, Steps, and Tasks](../02-stages-jobs-steps-and-tasks/)
- [Back to All Learning Materials](../../README.md)
