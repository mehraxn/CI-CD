# Formatting, Linting, and Static Analysis

## Checks That Never Run Your Code

The fastest quality checks examine source without executing the application. Four distinct kinds are routinely confused:

```text
Formatter:
Changes code layout to a consistent style.

Linter:
Reports suspicious patterns, style violations, or likely mistakes.

Static analyzer:
Examines code or configuration without executing the application.

Type checker:
Checks whether values and operations match declared type expectations.
```

Formatting is about **style rules** (ending debates, making diffs clean); linting spans style and **correctness rules** (unused variables, shadowed names, likely bugs); static analysis is the umbrella that also includes **security static analysis**, **complexity analysis**, and **duplicate-code detection**; type checking (mypy, pyright) verifies declared **coding standards** at the type level. Each tool reads its **configuration file** — in this repository, everything is configured in each project's `pyproject.toml`.

## The Real Toolchain Here

TaskOps and KubeOps use the same family, visible in [TaskOps CI](../../../Projects/1_project/taskops-cicd/.github/workflows/ci.yml) and configured in [pyproject.toml](../../../Projects/1_project/taskops-cicd/pyproject.toml):

```bash
ruff check .
black --check .
isort --check-only .
bandit -r app
pip-audit
```

- **Ruff** — a fast Python linter (the project selects rule families `E`, `F`, `I`, `B`, `UP`).
- **Black** — a formatter; in CI it runs in **check mode** (`--check`) so it fails instead of rewriting. Locally, `make format` runs the **auto-fix** mode — same tool, two modes, and CI must use check mode or it verifies nothing.
- **isort** — import sorting, configured with `profile = "black"` so the two tools agree.
- **Bandit** — analyzes Python *source patterns* for security issues (e.g. `subprocess` misuse, hard-coded passwords); the project excludes `tests/`.
- **pip-audit** — examines Python *dependency versions* against vulnerability databases.
- **Trivy** — in these workflows, scans the built *container image* (OS packages and libraries) and fails on HIGH/CRITICAL findings.

Bandit, pip-audit, and Trivy are all "security scanners" but have different subjects — your code's patterns, your dependencies' known CVEs, your image's contents. One passing says nothing about the other two; do not merge them into one mental category.

The type checker slot is real but empty here: **mypy is not currently used** by any project (only a leftover `.mypy_cache` entry in the Makefile's clean target). Type checking remains conceptual for this repository.

## Enforcement Mechanics

These checks communicate through **exit codes**: check modes exit non-zero on violations, which fails the CI step — that is the entire gate mechanism. The same tools can run earlier as **local hooks** (the pre-commit framework is the common carrier), giving developers instant feedback; CI enforcement remains the authority because hooks can be skipped. Platforms can surface results as **pull-request annotations** pointing at exact lines.

Two adoption tools matter on existing codebases: **baselines** (record current violations, fail only on new ones) let you enforce rules without fixing a decade of history first, and **suppressions** (inline ignores) handle genuine **false positives** — every static tool has them.

Suppression discipline:

- Require a reason with every suppression.
- Keep the scope narrow — one line, not a whole file.
- Review suppressions periodically.
- Do not suppress entire categories casually.
- Never use ignore rules just to make CI green without fixing problems.

## Common Mistakes

- Running the formatter in write mode in CI (verifies nothing, may create diffs).
- Treating a linter pass as proof of correctness.
- Config drift between local and CI tool versions (pinning helps — TaskOps pins all five tools in `requirements-dev.txt`).
- Letting suppressions accumulate unreviewed.
- Treating Bandit, pip-audit, and Trivy as interchangeable.
- Adopting every rule at once on a legacy codebase and drowning in noise.

## Practical Exercise

Map every check in [TaskOps CI](../../../Projects/1_project/taskops-cicd/.github/workflows/ci.yml)'s `quality` and `docker` jobs into this table:

```text
Tool
Category (formatter / linter / security static analysis / dependency scan / image scan / test)
Input (what it examines)
Failure behavior (what makes the step fail)
What it can detect
What it cannot prove
```

Cover Ruff, Black, isort, pytest, Bandit, pip-audit, and Trivy. For Trivy, note the two settings that shape its gate (`severity`, `ignore-unfixed`) and what each trades away. Do not modify the workflow. Target 25–35 minutes.

## Knowledge Check

1. What is the difference between a formatter and a linter?
2. Why must CI run Black with `--check` instead of letting it fix files?
3. What are the different subjects of Bandit, pip-audit, and Trivy?
4. What is a baseline for, on a legacy codebase?
5. What makes a suppression acceptable?
6. Does this repository use a type checker?

<details>
<summary>View answers</summary>

1. A formatter rewrites layout to a consistent style; a linter reports suspicious patterns and likely mistakes without necessarily changing anything.
2. CI must verify and fail, not silently rewrite; write mode would hide violations and modify a workspace nobody commits.
3. Bandit reads your Python source for insecure patterns; pip-audit checks your dependency versions against CVE databases; Trivy (as used here) scans the built container image's contents.
4. It records existing violations so enforcement can start immediately, failing only on newly introduced problems.
5. A documented reason, the narrowest possible scope, and periodic review — never a category-wide mute to make CI green.
6. No — mypy is not configured in any project; type checking is conceptual here.

</details>

## Navigation

- [Back to Automated Testing and Quality](../README.md)
- [Previous: Testing Strategy and Test Pyramid](../01-testing-strategy-and-test-pyramid/)
- [Next: Unit Testing](../03-unit-testing/)
- [Back to All Learning Materials](../../README.md)
