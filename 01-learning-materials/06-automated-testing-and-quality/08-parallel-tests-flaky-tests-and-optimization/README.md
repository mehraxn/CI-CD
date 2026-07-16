# Parallel Tests, Flaky Tests, and Optimization

## Three Speed Techniques

```text
Parallel testing:
Runs independent tests at the same time.

Test sharding:
Splits one large test suite into separate groups.

Matrix testing:
Repeats a job across multiple environments or versions.
```

They combine but solve different problems: parallelism uses idle cores or runners; sharding divides *one* suite so its wall-clock time shrinks; a matrix runs the *same* suite many times for compatibility. A conceptual sharding matrix:

```yaml
strategy:
  matrix:
    shard:
      - 1
      - 2
      - 3
      - 4
```

Each shard job runs a quarter of the suite; a fan-in step (or required checks) combines results. Sharding needs balanced groups (split by measured duration, not file count) and combined reporting so failures stay visible.

Other levers before adding machines: **test selection** — run only what a change affects (**changed-file testing**, or full **test-impact analysis** mapping tests to code); **test markers/categories** splitting a **fast suite** (every push) from a **slow suite** (PR or main); and honest **measurement** — profile test durations, find the **critical path**, and remember **queue time is not execution time**: adding jobs beyond runner capacity moves waiting from inside the job to in front of it. More parallel jobs also cost more (see [Matrix Builds and Parallelism](../../03-pipeline-architecture/05-matrix-builds-and-parallelism/)); optimize what measurement says is slow, not what feels slow.

## Flaky Tests

A **flaky test** passes and fails **intermittently** without code changes. Sources of the **non-determinism**: **race conditions** and **timing dependencies** (sleeps instead of readiness waits), **shared state** between tests, **test-order dependency**, **external-service instability**, uncontrolled **randomness**, **time-zone or clock dependencies**, and **resource contention** (parallel tests fighting over ports, files, databases). Diagnosis starts with the failure pattern:

| Symptom | Possible cause |
|---------|----------------|
| Fails only in parallel | Shared state or resource collision |
| Fails near midnight | Date or time-zone dependency |
| Fails only in CI | Environment or timing difference |
| Fails randomly | Random seed or race condition |
| Fails after another test | Order dependency |

**Reproduction** is the diagnostic goal: rerun in the failing conditions — same order, same parallelism, fixed **seed** (seed control turns "random" failures deterministic), tightened **timeouts**. A flaky test is a real defect in the test or its environment; it is dangerous because it trains people to rerun red builds, and a team that reruns on red will eventually rerun past a genuine regression.

## Retrying a Flaky Test Is Not the Final Fix

- Retries can collect evidence — a pass-on-second-try pattern confirms flakiness and its frequency.
- Retries can reduce immediate noise while a fix is in progress.
- Retries may hide instability — an auto-retried suite reports green while rotting underneath.
- **Quarantine** (excluding a flaky test from blocking status) must be temporary and *visible*: tracked, owned, time-boxed.
- Root cause must still be investigated — flaky-test **tracking** (which tests, how often, since when) is what makes the investigation queue real.
- Blocking status must be restored after repair, or quarantine becomes silent test deletion.

## Common Mistakes

- Retrying every failure automatically.
- Ignoring quarantined tests forever.
- Sharing one database between shards.
- Running more parallel jobs than runner capacity, buying queue time not speed.
- Optimizing without measuring.
- Removing useful tests only to shorten the pipeline.
- Treating queue time as test execution time.
- Caching test output as if it proves a new change passed.

## Existing Repository Evidence

- The test suites run **sequentially** — no `pytest-xdist`, sharding, or matrix testing exists in any project or workflow; the suites are small enough that parallelism would buy little.
- The suites are built to *avoid* flakiness at the design level: TaskOps gives each test a private temp SQLite database ([conftest.py](../../../Projects/1_project/taskops-cicd/tests/conftest.py)), KubeOps resets its in-memory store around every test — no shared state, no order dependency by construction. TaskOps' `test_routes.py` even documents an anti-flake pattern: it fetches the real database id after creation rather than assuming id `1`.
- The one intentional retry in the repository is not a test retry: [TaskOps CI](../../../Projects/1_project/taskops-cicd/.github/workflows/ci.yml)'s health poll retries *connection readiness* up to 10 times — the legitimate retry category.
- Automatic test retries, quarantine mechanisms, duration profiling, and test-impact analysis are not currently demonstrated; they remain conceptual.

## Practical Exercise

Propose safe optimizations without changing anything. Using the TaskOps CI workflow structure and its test suite: (1) estimate what could run in parallel that currently runs sequentially (jobs and/or tests) and what isolation properties make that safe; (2) identify which static checks could fan out into separate jobs and what overhead that adds; (3) classify five hypothetical failures — pip timeout, assertion failure, port collision under parallelism, midnight date failure, pass-after-rerun — using the diagnosis table, and state the correct response to each. Target 25–35 minutes.

## Knowledge Check

1. How do parallel testing, sharding, and matrix testing differ?
2. Why is a flaky test dangerous beyond its own noise?
3. What is the proper role of retries for flaky tests?
4. What conditions make quarantine acceptable?
5. Why must shards not share a database?
6. What design choices make this repository's suites flake-resistant?

<details>
<summary>View answers</summary>

1. Parallelism runs independent tests simultaneously; sharding splits one suite into groups to shorten it; a matrix repeats the same job across environments for compatibility.
2. It trains the team to rerun red builds, which eventually reruns past a real regression — it erodes trust in the entire signal.
3. Evidence collection and temporary noise reduction while the root cause is investigated — never the permanent fix.
4. Visibility, tracking, ownership, and a time limit — with blocking status restored after repair.
5. Shards run concurrently; shared mutable state creates collisions and order dependence, i.e. manufactured flakiness.
6. Per-test private state (temp SQLite file, in-memory store reset), no shared fixtures across tests, and tests that query real ids instead of assuming them.

</details>

## Navigation

- [Back to Automated Testing and Quality](../README.md)
- [Previous: Coverage, Reports, and Quality Gates](../07-coverage-reports-and-quality-gates/)
- [Back to All Learning Materials](../../README.md)
