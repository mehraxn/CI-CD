# Variables, Contexts, Expressions, and Outputs

## Two Evaluation Worlds

The most common source of confusion in pipeline configuration is that two different systems evaluate what looks like "variables":

```text
Pipeline expression:
Evaluated by the CI/CD platform.

Shell variable:
Evaluated by the command shell during execution.
```

In GitHub Actions, `${{ github.ref }}` is a **pipeline expression**: the platform replaces it with a value *before* the step's script ever reaches the shell. `$HOME` or `$APPLICATION_NAME` inside a `run:` script is a **shell variable**: the runner's shell expands it *during* execution. The platform never sees shell variables, and the shell never sees `${{ }}` — by the time the script runs, the expression is already plain text. Mixing up the two layers produces empty values, literal `${{ }}` strings in output, and injection vulnerabilities.

## Kinds of Variables

- **Environment variables** — key-value pairs visible to processes in a step. Declared with `env:` at workflow, job, or step level, or exported by the shell itself.
- **Configuration variables** (GitHub: repository and organization *variables*, the `vars` context) — non-sensitive settings managed in platform settings rather than the file, useful for values that differ per repository without being secret.
- **Secrets** — sensitive values (tokens, keys, passwords) stored encrypted in platform settings and exposed to workflows via the `secrets` context. Secrets and ordinary variables are different mechanisms with different protections; never store credentials as normal variables, and never use secrets for ordinary configuration.
- **Inputs / parameters** — values supplied when a workflow is called or manually dispatched.

**Scope and precedence:** a workflow-level `env` applies everywhere; a job-level `env` applies to that job; a step-level `env` applies to that step and overrides the outer levels for the same name. Values also have a **lifetime** — an environment variable exported by one step's shell process does not automatically persist to the next step unless written to the platform's environment file (`$GITHUB_ENV` in GitHub Actions).

## Worked Example: Inputs and Env Levels

```yaml
name: Variables Example

on:
  workflow_dispatch:
    inputs:
      environment:
        description: Deployment environment
        required: true
        default: staging
        type: choice
        options:
          - staging
          - production

env:
  APPLICATION_NAME: task-api

jobs:
  display-values:
    runs-on: ubuntu-latest

    env:
      TARGET_ENVIRONMENT: ${{ inputs.environment }}

    steps:
      - name: Display non-sensitive values
        run: |
          echo "Application: $APPLICATION_NAME"
          echo "Environment: $TARGET_ENVIRONMENT"
```

Walking through the layers:

- `workflow_dispatch.inputs` defines a manual **input** with a type, a default, and a constrained choice list — constraining inputs is the first line of input validation.
- The workflow-level `env` sets `APPLICATION_NAME` for every job.
- The job-level `env` uses a **pipeline expression** (`${{ inputs.environment }}`) to copy the input into an environment variable.
- The script then reads both via **shell expansion** (`$APPLICATION_NAME`) — the shell sees ordinary environment variables and knows nothing about how they were populated.

## Contexts, Expressions, Functions, and Operators

A **context** is a structured object of data the platform exposes: `github` (event, ref, actor, repository), `env`, `vars`, `secrets`, `inputs`, `needs`, `matrix`, `runner`, and others. An **expression** — `${{ ... }}` — reads contexts and combines them with operators (`==`, `!=`, `&&`, `||`, `!`) and functions (`contains()`, `startsWith()`, `format()`, and the status functions from the Conditions lesson). Expressions power conditions, dynamic values, **dynamic job names** (`name: Deploy to ${{ inputs.environment }}`), **dynamic runner selection** (`runs-on: ${{ vars.RUNNER_LABEL }}`), and **dynamic matrices** (a matrix built from a previous job's JSON output).

Not every context is available everywhere: some events do not populate some contexts, and secrets are unavailable in certain positions and restricted for forked pull requests. Check availability rather than assuming.

## Outputs: Passing Metadata Between Steps and Jobs

```yaml
jobs:
  version:
    runs-on: ubuntu-latest

    outputs:
      application-version: ${{ steps.generate.outputs.version }}

    steps:
      - id: generate
        name: Generate version
        run: echo "version=1.2.3" >> "$GITHUB_OUTPUT"

  package:
    needs: version
    runs-on: ubuntu-latest

    steps:
      - name: Display version
        run: echo "Version ${{ needs.version.outputs.application-version }}"
```

The chain has four links:

1. The step has an **`id`** (`generate`) so it can be referenced.
2. The script writes a `name=value` line to the **environment file** `$GITHUB_OUTPUT`, creating a **step output**.
3. The job's `outputs` block promotes the step output to a **job output**.
4. A dependent job declares `needs: version` and reads `needs.version.outputs.application-version`.

Outputs are for **small metadata** — versions, image names, flags — not for files. Files produced on one runner do not exist on another; moving files between jobs requires artifacts (a later topic). Trying to pass file contents through outputs hits size limits and logging hazards.

## Secrets and Safety

- Never intentionally print secrets.
- **Masking is not complete protection** — the platform redacts exact secret values from logs, but a transformed value (base64-encoded, split, concatenated) may not be masked.
- Do not pass secrets to jobs or steps that do not need them; scope them as narrowly as the platform allows.
- Forked pull requests receive restricted secret access by design; workflows must not assume secrets exist in that event.
- Prefer short-lived identity (such as OIDC-issued cloud credentials) over long-lived stored keys where supported.
- Validate user-provided inputs before using them in sensitive operations, and never interpolate untrusted input (issue titles, branch names, PR bodies) directly into shell commands via `${{ }}` — the expression is substituted into the script text, so crafted input can inject commands. Pass untrusted values through `env:` and reference them as quoted shell variables instead.

## Common Mistakes

- Confusing pipeline expressions with shell variables.
- Using a value outside its scope, or expecting a step-exported variable in a later step without `$GITHUB_ENV`.
- Passing files through outputs instead of artifacts.
- Printing sensitive values (directly or transformed).
- Assuming every context is populated for every event.
- Ignoring precedence when the same name is set at several levels.
- Using secrets for ordinary configuration, or ordinary variables for credentials.
- Failing to quote shell values (`"$VAR"`), breaking on spaces or empty strings.

## Existing Workflow Evidence

- [KubeOps image release](../../../Projects/2_project/kubeops-gitops/.github/workflows/image-release.yml) is a complete real output chain: the step with `id: img` writes `image=...` to `"$GITHUB_OUTPUT"`, and later steps read `${{ steps.img.outputs.image }}`. It also shows a step-level `env:` (`OWNER`) feeding a shell parameter expansion (`${OWNER,,}` — shell-level lowercasing, invisible to the platform).
- [TaskOps CD](../../../Projects/1_project/taskops-cicd/.github/workflows/cd.yml) writes `IMAGE=...` to `"$GITHUB_ENV"` so later *steps in the same job* can use `${{ env.IMAGE }}`, and passes secrets (`secrets.DEPLOY_HOST`, `secrets.GITHUB_TOKEN`) into action inputs and step `env:` without printing them.
- The repository does not currently use configuration variables (the `vars` context), workflow inputs beyond a bare `workflow_dispatch`, or dynamic matrices; those remain conceptual here.

## Practical Exercise

Build a variable map for [TaskOps CD](../../../Projects/1_project/taskops-cicd/.github/workflows/cd.yml). For each value the workflow uses, record:

```text
Variable name
Source (env file, step env, secrets context, github context, literal)
Scope (workflow, job, step)
Sensitive or non-sensitive
Used by (which step or action input)
```

Cover at least: `IMAGE`, `OWNER`, `IMAGE_TAG`, `FLASK_SECRET_KEY`, `GHCR_TOKEN`, and one `github.*` context value. Do not display or copy any secret values — record only names and flow. Target 25–35 minutes.

## Knowledge Check

1. Who evaluates `${{ github.ref }}`, and who evaluates `$HOME` in a `run:` script?
2. Why does an `export` in one step not affect the next step?
3. What are outputs for, and what should they never carry?
4. Why is secret masking insufficient protection on its own?
5. Why is interpolating a pull-request title directly into a `run:` command dangerous?
6. When the same `env` name is set at workflow and step level, which wins inside that step?

<details>
<summary>View answers</summary>

1. The platform substitutes `${{ }}` expressions before execution; the runner's shell expands `$HOME` during execution.
2. Each step runs in a fresh shell process; persistence between steps requires the platform's environment file, such as `$GITHUB_ENV`.
3. Small metadata (versions, names, flags) passed between steps and jobs; never files or large data — those need artifacts.
4. Masking redacts exact known values; transformed or split secret values may not be recognized, and printing them can leak.
5. The expression is substituted into the script text before the shell runs it, so crafted input can inject arbitrary commands; pass untrusted values via `env:` and quote them.
6. The step-level value — the most specific scope takes precedence.

</details>

## Navigation

- [Back to Pipeline as Code and Platforms](../README.md)
- [Previous: YAML Fundamentals](../02-yaml-fundamentals/)
- [Next: Reusable Workflows, Templates, and Components](../04-reusable-workflows-templates-and-components/)
- [Back to All Learning Materials](../../README.md)
