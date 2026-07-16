# Reusable Workflows, Templates, and Components

## Why Reuse Matters

As soon as a team maintains more than a handful of repositories — or more than a couple of workflows in one repository — the same steps appear everywhere: check out, set up a runtime, install dependencies, run checks. Copy-pasted **workflow duplication** drifts: one copy gets a security fix, five do not. Reuse mechanisms exist to give that shared logic one home.

Reuse is a tradeoff, not a free win. Every layer of abstraction moves logic away from the file the reader is looking at, and **over-abstraction** can make a one-line failure take an hour to locate.

## The Four Main Mechanisms

```text
Reusable workflow:
A workflow called by another workflow, usually at the job level.

Composite action:
A reusable collection of steps executed inside a job.

Workflow template:
A starting file copied into a repository and maintained separately afterward.

Shared library:
Reusable pipeline code, commonly associated with Jenkins.
```

The critical distinctions: a reusable workflow replaces a **job** (it brings its own runner and jobs); a composite action replaces a group of **steps** (it runs inside the caller's job on the caller's runner). A template is **copied once** — after copying, the repository owns its version and receives no updates. A Jenkins Shared Library is versioned Groovy code imported by `Jenkinsfile`s. GitLab's equivalents are `include:`, CI/CD components, and parent-child pipelines (a pipeline that triggers a child pipeline from a generated or included definition — useful in monorepos).

## Reusable Workflow Example

The called workflow declares a `workflow_call` trigger with typed inputs:

```yaml
name: Reusable Tests

on:
  workflow_call:
    inputs:
      python-version:
        required: true
        type: string

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: ${{ inputs.python-version }}

      - name: Run tests
        run: echo "Run tests here"
```

The caller uses it as a job:

```yaml
name: Application CI

on:
  pull_request:

jobs:
  tests:
    uses: ./.github/workflows/reusable-tests.yml
    with:
      python-version: "3.12"
```

Both examples are conceptual and live only in this lesson — this repository does not currently define reusable workflows, and none should be created now.

Reusable workflows can also declare outputs (returned to the caller) and receive **secrets** — either explicitly listed or via `secrets: inherit`. Explicit forwarding is safer: `inherit` hands every secret to the called workflow whether it needs them or not. **Permissions** matter the same way: the called workflow runs with permissions bounded by what the caller grants.

## Composite Action Example

A composite action packages steps under a repository path (conventionally `.github/actions/<name>/action.yml`) and is consumed with `uses:` inside any job:

```yaml
name: Project Setup
description: Install project dependencies

runs:
  using: composite
  steps:
    - name: Install dependencies
      shell: bash
      run: echo "Install dependencies"
```

Because composite actions run inside the caller's job, they are the right tool for shared *setup sequences* (install, configure, authenticate) where the surrounding job still controls the runner, services, and remaining steps. **Local actions** live in the same repository and are referenced by path; published actions live in their own repositories and are referenced by owner, name, and version.

## Versioning and the Supply Chain

Anything reused is a dependency, and dependencies need versioning:

- **Commit-SHA pinning** (`uses: owner/action@<full-sha>`) is the strongest guarantee — the referenced code cannot change under you.
- **Tag pinning** (`@v4`, `@0.28.0`) is readable and common, but tags can be moved by the publisher; trust in the publisher is part of the decision.
- **Floating references** (`@main`) accept whatever the publisher pushes next — behavior can change without any commit in your repository, which is exactly the reproducibility hole Pipeline as Code tries to close.

Third-party actions are **supply-chain risk**: they run with your job's token, environment, and (if forwarded) secrets. Prefer trusted publishers (`actions/*`, well-known vendors), read the source of small actions, and pin appropriately. The same logic applies to your own shared workflows: consumers should reference a version, and maintainers must treat **breaking changes** deliberately — version the workflow, keep **backward compatibility** where possible, and test changes against consumers before releasing them.

Shared components also need what any software needs: an **owner**, **documentation** of inputs and outputs, **tests** (even a consumer repository that exercises them), and **discoverability** — a shared workflow nobody can find gets reimplemented.

## Common Mistakes

- Abstracting one trivial command into a component (`run: make test` did not need wrapping).
- The opposite failure: duplicating complicated multi-step workflows across repositories.
- Forwarding every secret with `secrets: inherit` out of convenience.
- Undocumented inputs that force consumers to read the implementation.
- Changing a shared workflow in place and breaking every consumer at once.
- Unsafe third-party references — floating tags, unknown publishers, no pinning policy.
- Hidden logic: a caller that looks like three lines but performs deployment via layers of indirection.
- Circular dependencies between reusable workflows.
- Excessively centralized designs where one team bottlenecks every pipeline change.
- Reuse that makes debugging harder than the duplication it replaced.

## Existing Workflow Evidence

The repository's four workflows consume **published third-party actions** with tag pinning — [TaskOps CI](../../../Projects/1_project/taskops-cicd/.github/workflows/ci.yml) uses `actions/checkout@v4`, `actions/setup-python@v5`, `docker/build-push-action@v6`, and pins `aquasecurity/trivy-action@0.28.0` to an exact release tag. [TaskOps CD](../../../Projects/1_project/taskops-cicd/.github/workflows/cd.yml) additionally uses `appleboy/scp-action` and `appleboy/ssh-action` — third-party publishers worth examining through a supply-chain lens.

There is visible duplication worth noticing: the quality checks in TaskOps CI's `quality` job and TaskOps CD's `verify` job are nearly identical, and [KubeOps CI](../../../Projects/2_project/kubeops-gitops/.github/workflows/ci.yml) repeats the same Python setup-and-check sequence. The repository does not currently define reusable workflows, composite actions, or workflow templates; implementing one is a candidate for a later practical enhancement, not for this lesson.

## Practical Exercise

Compare the `quality` job in [TaskOps CI](../../../Projects/1_project/taskops-cicd/.github/workflows/ci.yml) with the `verify` job in [TaskOps CD](../../../Projects/1_project/taskops-cicd/.github/workflows/cd.yml). Propose — on paper only — one reusable unit:

1. Would you extract a reusable workflow or a composite action? Justify using the job-vs-steps distinction.
2. List the inputs it would need (with types and defaults) and any outputs.
3. State which secrets, if any, it requires — and which it must *not* receive.
4. Describe how you would version it and roll out a breaking change.

Do not modify or create any workflow or action file. Target 25–35 minutes.

## Knowledge Check

1. What is the structural difference between a reusable workflow and a composite action?
2. Why does a workflow template not solve long-term drift?
3. Rank commit-SHA pinning, tag pinning, and floating references by supply-chain safety.
4. Why is `secrets: inherit` convenient but risky?
5. When does reuse make a pipeline *worse*?

<details>
<summary>View answers</summary>

1. A reusable workflow is called at the job level and brings its own jobs and runners; a composite action is a bundle of steps that runs inside the caller's job on the caller's runner.
2. A template is copied once and then owned by each repository; copies receive no updates and drift independently.
3. SHA pinning is safest (immutable), tag pinning is next (tags can be moved by the publisher), floating references are weakest (code changes without any commit on your side).
4. It forwards every secret to the called workflow regardless of need, widening the blast radius if that workflow is compromised or buggy.
5. When the abstraction hides logic needed for debugging, wraps trivial commands, or centralizes changes behind a bottleneck — costs that exceed the duplication saved.

</details>

## Navigation

- [Back to Pipeline as Code and Platforms](../README.md)
- [Previous: Variables, Contexts, Expressions, and Outputs](../03-variables-contexts-expressions-and-outputs/)
- [Next: Runners and Execution Environments](../05-runners-and-execution-environments/)
- [Back to All Learning Materials](../../README.md)
