# GitHub Actions

## The Platform in One Paragraph

GitHub Actions is GitHub's built-in automation platform. Workflow files — YAML documents under `.github/workflows/` in each repository — declare which **events** start a **workflow run**, which **jobs** the run contains, and which **steps** each job executes on a **runner**. Steps either run shell commands (`run:`) or invoke packaged **actions** (`uses:`) from the Marketplace, another repository, or a local path. Because this is the platform the repository's projects actually use, this lesson goes deepest, and every concept links to a real file you can open.

## Anatomy of a Workflow

The following workflow is **educational** — it demonstrates structure and is not automatically suitable for this repository's real dependency or test commands:

```yaml
name: Application CI

on:
  pull_request:
    branches:
      - main

  push:
    branches:
      - main

permissions:
  contents: read

concurrency:
  group: ci-${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  test:
    name: Test on Python ${{ matrix.python-version }}
    runs-on: ubuntu-latest

    strategy:
      fail-fast: false
      matrix:
        python-version:
          - "3.11"
          - "3.12"

    steps:
      - name: Check out source code
        uses: actions/checkout@v4

      - name: Configure Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: pip

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          echo "Install project dependencies here"

      - name: Run tests
        run: echo "Run project tests here"
```

Reading it top to bottom:

- **`name`** — the display name shown in the Actions tab and on status checks.
- **`on`** — the trigger rules. Here the workflow runs for pull requests targeting `main` and pushes to `main` (see [Triggers and Events](../../03-pipeline-architecture/01-triggers-and-events/) for the full treatment).
- **`permissions`** — the rights granted to the run's automatic token; more below.
- **`concurrency`** — the expression-built group name means "one live run per workflow per ref"; a newer run cancels an older one.
- **`jobs`** — a mapping of **job IDs** (`test` — the key, used by `needs`) to job definitions. The optional job **`name`** is the human label, here made dynamic with a matrix expression.
- **`runs-on`** — runner selection (hosted `ubuntu-latest` here; self-hosted labels also work).
- **`strategy` / `matrix`** — expands the one job definition into one job per combination; `fail-fast: false` lets siblings finish when one fails.
- **`steps`** — the ordered work. **`uses`** invokes an action, **`with`** passes its inputs, **`run`** executes shell commands (the `|` literal block holds a multi-line script).

Everything else in the platform hangs off this skeleton: conditions (`if:`), dependencies (`needs:`), services (`services:`), environment variables (`env:`), and outputs, all covered in this section's earlier lessons and in [Pipeline Architecture](../../03-pipeline-architecture/).

## Permissions and GITHUB_TOKEN

Every run receives an automatic, short-lived **`GITHUB_TOKEN`** whose rights are set by `permissions`:

```yaml
permissions:
  contents: read
  packages: write
```

**Least privilege** is the rule: grant only what the jobs need. A CI workflow that only checks out code needs `contents: read` and nothing else; a workflow pushing images to GitHub Container Registry adds `packages: write`. Both real patterns exist in this repository: [KubeOps CI](../../../Projects/2_project/kubeops-gitops/.github/workflows/ci.yml) sets workflow-level `contents: read` with an explicit comment ("Read-only token is all CI needs"), and [TaskOps CD](../../../Projects/1_project/taskops-cicd/.github/workflows/cd.yml) grants `packages: write` only at the `deploy` job level — the neighboring `verify` job never holds write rights. Beyond `GITHUB_TOKEN`, workflows that talk to cloud providers should prefer **OIDC**: the run requests a short-lived cloud credential proving its identity, instead of storing long-lived cloud keys as secrets. The repository does not currently use OIDC.

## Environments and Approvals

A job can target a named **environment**:

```yaml
jobs:
  deploy:
    needs: test
    environment: staging
    runs-on: ubuntu-latest

    steps:
      - name: Deploy
        run: echo "Deploy to staging"
```

Environments carry their own secrets and **protection rules** (required reviewers, wait timers) configured in repository settings — the manual-approval mechanism from [Manual Approvals and Quality Gates](../../03-pipeline-architecture/06-manual-approvals-and-quality-gates/). The repository's workflows do not currently declare environments; deployment gating in TaskOps CD is achieved through `needs: verify` and branch-limited triggers instead. Workflow syntax alone cannot tell you what settings exist — settings live outside the file.

## Manual and Scheduled Workflows

`workflow_dispatch` adds a "Run workflow" button, optionally with typed, validated inputs:

```yaml
on:
  workflow_dispatch:
    inputs:
      environment:
        description: Target environment
        required: true
        type: choice
        options:
          - staging
          - production
```

[KubeOps image release](../../../Projects/2_project/kubeops-gitops/.github/workflows/image-release.yml) demonstrates the real (input-less) form: `workflow_dispatch` alongside its push trigger, so an operator can rebuild and republish the image on demand. `schedule:` with cron syntax runs workflows on a timer (UTC); no repository workflow currently uses it.

## Repository Layout

```text
.github/
├── workflows/
│   ├── ci.yml
│   ├── release.yml
│   └── deploy.yml
└── actions/
    └── project-setup/
        ├── action.yml
        └── scripts/
```

Only `.github/workflows/` is mandatory for workflows; the `actions/` directory appears only when a repository defines local actions. Not every repository needs this full structure — this repository's projects each carry just a `workflows/` directory with two files. Note that GitHub discovers workflows **only** at the repository root's `.github/workflows/`; the project folders here each represent what would be a standalone repository root.

## Reading an Existing Workflow

When you open an unfamiliar workflow, read in this order:

1. Workflow name — what does it claim to do?
2. Events — when does it run, and for whom (forks? tags? schedules?)
3. Permissions — what can its token touch?
4. Concurrency — what happens when runs overlap?
5. Jobs — how many, and what does each own?
6. Dependencies — the `needs` graph and its critical path.
7. Runners — hosted or self-hosted, and what that implies.
8. Steps — actions first (what third-party code runs?), then scripts.
9. Variables and secrets — what data flows in, and how sensitive is it?
10. Artifacts or deployment behavior — what leaves the run?

Applied to [TaskOps CI](../../../Projects/1_project/taskops-cicd/.github/workflows/ci.yml), this order surfaces the design in about two minutes: push-to-main plus pull requests (with a comment explaining why push is branch-restricted), no explicit permissions block (a finding worth noting), cancel-in-progress concurrency, a two-job `needs` chain (`quality` → `docker`), hosted runners, tag-pinned actions including Trivy at `@0.28.0`, pip caching via `setup-python`, Docker layer caching with `cache-from`/`cache-to: type=gha`, and an `if: always()` cleanup step.

## Debugging GitHub Actions

- Read the **first meaningful failure**, not the last red line — later errors are often consequences.
- Expand the failed step's log; check the exact command and its exit code.
- Check shell behavior: each `run:` block is one script; with the default bash options, a failing middle command may not stop the block unless the script is written to fail fast.
- Check the working directory — each step starts at the workspace root, not where the previous step ended with `cd`.
- Check the event context: did this run come from the event you assumed? A `pull_request` run sees a merge ref, not the branch head.
- Check variable scope and secret availability for this event type (fork PRs receive restricted secrets).
- Check permissions — a 403 from an API or registry usually means the token lacks a scope.
- Reproduce the command locally with the same versions where possible.
- Add safe temporary debug output (`env | sort`, tool versions) — but **never print secrets**, directly or transformed.
- Compare a failing run with the last successful one: what changed — code, workflow, action version, or runner image?
- Annotations (the errors and warnings surfaced on the run summary and diff) often point to the exact file and line before you open any log.

## GitHub Actions Security Checklist

- Minimal `GITHUB_TOKEN` permissions, set explicitly at workflow or job level.
- Careful third-party action selection — trusted publishers, source review for small actions.
- Appropriate version pinning (SHA for strongest guarantees; exact tags at minimum).
- Protected deployment environments for anything that touches production.
- Secret restrictions respected for untrusted code paths (forked pull requests).
- OIDC instead of long-lived cloud keys where the provider supports it.
- Safe handling of untrusted input — no direct interpolation of titles, branch names, or bodies into scripts.
- Self-hosted runners protected: ephemeral where possible, never privileged-by-default, never shared with fork workloads.
- Workflow changes reviewed like code changes — they are code changes.
- No unnecessary privileged execution (Docker socket, root containers, broad cloud roles).

## What the Real Workflows Demonstrate

| Feature | Where to inspect |
|---|---|
| Push + PR triggers with branch filter | [TaskOps CI](../../../Projects/1_project/taskops-cicd/.github/workflows/ci.yml) `on:` block and its comment |
| Manual trigger (`workflow_dispatch`) | [KubeOps image release](../../../Projects/2_project/kubeops-gitops/.github/workflows/image-release.yml) |
| Workflow-level least-privilege permissions | [KubeOps CI](../../../Projects/2_project/kubeops-gitops/.github/workflows/ci.yml) |
| Job-level `permissions` with `packages: write` | [TaskOps CD](../../../Projects/1_project/taskops-cicd/.github/workflows/cd.yml) `deploy` job |
| Concurrency (cancel vs. serialize) | TaskOps CI (`cancel-in-progress: true`) vs. TaskOps CD (`false`) |
| Job dependency (`needs`) | TaskOps CI `docker: needs: quality`; TaskOps CD `deploy: needs: verify` |
| Step outputs via `$GITHUB_OUTPUT` | KubeOps image release, step `id: img` |
| `$GITHUB_ENV` for cross-step values | TaskOps CD, "Compute lowercase image name" |
| Secrets in action inputs and step env | TaskOps CD (`secrets.DEPLOY_*`, `secrets.GITHUB_TOKEN`) |
| Dependency caching (`cache: pip`) and Docker layer caching (`type=gha`) | TaskOps CI and CD |
| Docker build, scan gate, image publishing | TaskOps CD; KubeOps image release |
| Step condition (`if: always()`) | TaskOps CI final cleanup step |

Not currently demonstrated: matrices, scheduled triggers, repository variables (`vars`), environments and approvals, OIDC, artifact upload/download, reusable workflows, composite actions, and self-hosted runners. These are covered conceptually in this section and may be implemented during a later project-enhancement phase.

## Practical Exercise

Annotate one real workflow end to end. Choose [TaskOps CD](../../../Projects/1_project/taskops-cicd/.github/workflows/cd.yml) (the richest single file) and produce a written annotation covering each item:

```text
Trigger
Permissions
Jobs
Dependencies
Runner
Matrix
Conditions
Variables
Secrets
Artifacts
Deployment behavior
```

For items the workflow does not use (matrix, artifacts, step conditions), state explicitly that they are absent — knowing what is *not* there is part of reading a workflow. Do not execute or edit the workflow, and do not record secret values, only secret *names*. Target 30–35 minutes.

## Knowledge Check

1. Where must workflow files live for GitHub to discover them?
2. What is the difference between a job ID and a job name?
3. What does `permissions: contents: read` control?
4. Why prefer OIDC over a stored cloud key?
5. How do the two TaskOps workflows use concurrency differently, and why?
6. Why can't you tell from workflow syntax alone whether an environment requires approval?

<details>
<summary>View answers</summary>

1. In `.github/workflows/` at the repository root.
2. The job ID is the YAML key used for references like `needs`; the name is the human-readable label shown in the UI.
3. The rights of the run's automatic `GITHUB_TOKEN` — here, read-only repository contents and nothing else.
4. OIDC issues short-lived, per-run credentials, so there is no long-lived key to store, rotate, or leak.
5. CI cancels superseded runs (`cancel-in-progress: true`) to save minutes; CD serializes (`false`) so a deployment is never killed mid-run and deploys never interleave.
6. Reviewer requirements are repository/environment settings stored outside the file; the YAML only names the environment.

</details>

## Navigation

- [Back to Pipeline as Code and Platforms](../README.md)
- [Previous: Runners and Execution Environments](../05-runners-and-execution-environments/)
- [Next: Jenkins](../07-jenkins/)
- [Back to All Learning Materials](../../README.md)
