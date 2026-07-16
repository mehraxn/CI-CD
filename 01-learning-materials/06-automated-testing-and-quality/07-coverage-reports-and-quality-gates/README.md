# Coverage, Reports, and Quality Gates

## What Coverage Measures

**Code coverage** records which code the tests executed. Granularities differ: **line/statement coverage** (was the line run), **branch coverage** (were both sides of each `if` taken — strictly more informative), and **function coverage** (was the function entered at all). The essential honesty:

```text
Coverage answers:
Which code was executed by tests?

Coverage does not answer:
Whether the assertions were correct or whether important behavior was tested.
```

A test that calls everything and asserts nothing produces beautiful coverage and zero verification. Coverage's real strengths are *negative* signals: 0% on a critical module is an unambiguous gap, and a falling **coverage trend** says new code is arriving untested.

A conceptual pytest invocation (coverage is **not currently configured** in this repository):

```bash
pytest \
  --cov=app \
  --cov-report=term-missing \
  --cov-report=xml \
  --cov-fail-under=80
```

`--cov-report=term-missing` lists uncovered lines in the terminal; the XML report feeds platforms and PR annotation tools; `--cov-fail-under` turns the measurement into a gate.

## Reports: Making Results Visible

Test runs produce **test result reports** as well as pass/fail bits. **JUnit XML** is the lingua franca — nearly every tool emits it, nearly every CI platform renders it into per-test result views. **HTML reports** (coverage highlighting per line) serve humans; **pull-request annotations** put failures and uncovered lines on the diff itself. Reports are also **test evidence**: preserved as artifacts, they answer later questions ("was this tested before release?") that logs alone answer badly. This repository's workflows currently rely on pytest's terminal output only — no JUnit XML, coverage reports, or uploaded evidence; those remain conceptual here.

## Gates: Turning Evidence into Decisions

A **quality gate** is a rule that decides whether the pipeline proceeds — as introduced in [Manual Approvals and Quality Gates](../../03-pipeline-architecture/06-manual-approvals-and-quality-gates/). Gates can be **blocking** (failure stops the pipeline; on GitHub, a **required check** blocks merging) or **non-blocking** (informational). Common families with their limits:

| Gate | Possible rule | Important limitation |
|------|---------------|----------------------|
| Unit tests | All required tests pass | Tests may be incomplete |
| Coverage | Coverage is above threshold | Percentage does not prove quality |
| Linting | No blocking violations | Linter rules have limited scope |
| Dependency scan | No disallowed vulnerability | Severity requires context |
| Image scan | No blocked image finding | Scanner databases and configuration matter |

Every gate needs an **owner** and periodic **review**; gates whose purpose nobody can state get worked around. Exceptions — **risk acceptance** for a vulnerability, a suppressed **false positive**, a **gate bypass** in an emergency — are legitimate *when documented, scoped, and time-limited*, and every bypass must leave an audit trail (**auditability** is half the point of gating in the first place).

## Designing Thresholds Responsibly

- **Start with a baseline** — measure what you have before demanding a number.
- **Avoid arbitrary numbers** — 80% is a convention, not a law; the right threshold protects against *regression* from your baseline.
- **Prefer changed-code coverage** — requiring new/modified lines to be tested improves every PR without demanding archaeology on legacy code.
- **Allow documented exceptions** and review them.
- **Never lower the threshold just to make CI green** — that converts a signal into a lie.

## Common Mistakes

- Chasing a coverage percentage with assertion-free tests.
- Treating any green gate as proof of quality.
- Arbitrary thresholds that punish unrelated work.
- Permanent, unreviewed exceptions.
- Non-blocking checks nobody ever reads.
- Gate bypasses without audit trails.

## Existing Workflow Evidence

The repository's real gates are all **blocking by job structure** — each check is a step whose non-zero exit fails the job, and dependent jobs are skipped:

- In [TaskOps CI](../../../Projects/1_project/taskops-cicd/.github/workflows/ci.yml), the `quality` job chains Ruff, Black, isort, pytest, Bandit, and pip-audit — any failure blocks the `docker` job via `needs: quality`. The `docker` job adds the Trivy image gate (explicitly configured blocking: `exit-code: "1"`, HIGH/CRITICAL, `ignore-unfixed: true` — a documented, scoped risk acceptance for unfixable CVEs) and the container smoke test.
- [TaskOps CD](../../../Projects/1_project/taskops-cicd/.github/workflows/cd.yml) re-runs the same gates in `verify` before `deploy` — gates guarding deployment, not just merging.
- Whether these jobs are *required checks for merging* is a repository setting not visible in source files, so this material makes no claim about it.
- Coverage measurement, JUnit XML, HTML reports, PR annotations, and artifact-preserved test evidence are not currently demonstrated and may be added in a later enhancement phase.

## Practical Exercise

Build a gate inventory for TaskOps. List every check in both workflows; for each, record: what evidence it evaluates, whether it is blocking (and *what* it blocks — the job, the pipeline, the deployment), and its documented limitations or risk acceptances (find the Trivy `ignore-unfixed` comment). Then propose — on paper only — a coverage gate for this project: initial threshold strategy, changed-code policy, and exception process. Do not implement anything. Target 25–35 minutes.

## Knowledge Check

1. What does coverage measure, and what does it not measure?
2. Why is branch coverage stronger than line coverage?
3. What is the difference between a blocking and a non-blocking check?
4. Why is "changed-code coverage" often better than a global threshold?
5. What makes a gate exception acceptable?
6. What real risk acceptance is encoded in the TaskOps Trivy configuration?

<details>
<summary>View answers</summary>

1. It measures which code the tests executed; it says nothing about assertion correctness or whether important behavior was verified.
2. A line with an `if` can be "covered" while one branch was never taken; branch coverage requires both outcomes to be exercised.
3. A blocking check stops the pipeline (or merge) on failure; a non-blocking check reports information without stopping anything.
4. It improves every new change without demanding retroactive tests for legacy code, and cannot be gamed by untested old code diluting the metric.
5. Documentation, narrow scope, time limits, review, and an audit trail — not silent permanence.
6. `ignore-unfixed: true` — vulnerabilities without an available fix do not block the build, a deliberate, commented trade of completeness for actionability.

</details>

## Navigation

- [Back to Automated Testing and Quality](../README.md)
- [Previous: Performance Testing](../06-performance-testing/)
- [Next: Parallel Tests, Flaky Tests, and Optimization](../08-parallel-tests-flaky-tests-and-optimization/)
- [Back to All Learning Materials](../../README.md)
