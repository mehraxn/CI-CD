# Matrix Builds and Parallelism

## Parallel Execution

Parallel execution runs independent work at the same time. It can shorten feedback when runner capacity exists, but it increases concurrent resource use and may increase cost. Jobs are common parallel units. Steps inside one job normally remain sequential unless a tool or script explicitly manages concurrent processes.

A **matrix build** repeats one job definition across selected configuration values. Typical dimensions include operating system, runtime version, CPU architecture, database version, and browser. A matrix is valuable when those combinations represent supported behavior, not simply because more combinations are possible.

## Matrix Expansion

```yaml
name: Matrix Tests

on:
  pull_request:

jobs:
  test:
    runs-on: ${{ matrix.os }}

    strategy:
      fail-fast: false
      matrix:
        os:
          - ubuntu-latest
          - windows-latest
        python-version:
          - "3.11"
          - "3.12"

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Display test environment
        run: |
          python --version
          echo "${{ matrix.os }}"
```

The Cartesian product contains four jobs:

```text
Ubuntu + Python 3.11
Ubuntu + Python 3.12
Windows + Python 3.11
Windows + Python 3.12
```

If three operating systems and four runtime versions are selected, the base product is 12 jobs. Adding browsers or databases multiplies the count again.

`fail-fast: false` lets other matrix jobs continue after one fails, helping reveal the full compatibility pattern. With fail-fast enabled, a failure may cancel queued or running siblings according to platform behavior. Neither choice is universal: early cancellation saves resources, while complete results aid compatibility diagnosis.

## Include and Exclude

```yaml
strategy:
  matrix:
    os:
      - ubuntu-latest
      - windows-latest
    python-version:
      - "3.10"
      - "3.11"
      - "3.12"
    exclude:
      - os: windows-latest
        python-version: "3.10"
```

`exclude` removes a known unsupported or unnecessary combination from the base expansion.

```yaml
strategy:
  matrix:
    python-version:
      - "3.11"
      - "3.12"
    include:
      - python-version: "3.12"
        experimental: true
```

`include` can add metadata or additional combinations depending on its keys and platform semantics. Here it associates an `experimental` value with Python 3.12 for conditional behavior. Verify actual expansion rather than assuming include behaves like a simple merge in every case.

## Parallel Techniques

| Technique | Purpose |
|-----------|---------|
| Independent jobs | Run unrelated pipeline work simultaneously |
| Matrix build | Repeat one job across several configurations |
| Test sharding | Divide one large test suite into smaller groups |
| Parallel steps | Tool-specific concurrent work inside one job |

Test sharding assigns disjoint test groups to workers. Good sharding balances duration and combines reports so failures remain visible. It differs from a compatibility matrix, although both can be combined.

## Capacity, Queueing, and Cost

Maximum parallel settings can limit how many matrix jobs run simultaneously. Runner quotas and availability may queue the rest. Ten parallel jobs do not improve elapsed time if only two runners are available. Hosted minutes, larger runner prices, and self-hosted capacity affect cost.

Measure queue time and execution time separately. Moving work into many tiny jobs may add scheduling and setup overhead. A matrix should prioritize supported and high-risk combinations. A broad nightly matrix and a smaller pull-request matrix can be useful, but this repository does not currently implement that pattern.

## Safe Parallelism

Parallel jobs can race when they use one mutable external resource. Integration tests should not share a database name, account, queue, port on the same host, or environment without coordination. Use unique resource names derived from safe run and job identifiers, isolated containers or schemas, and guaranteed cleanup.

Parallel deployments require special design. Two production jobs changing the same service can interleave migrations or overwrite desired state. Serialize them unless the deployment system explicitly supports safe concurrency.

Combining matrix results requires a fan-in gate or required checks. An allowed experimental combination should be labeled without hiding failure in supported combinations.

## Existing Workflow Evidence

The repository workflows do not currently use a matrix or test sharding. [TaskOps CI](../../../Projects/1_project/taskops-cicd/.github/workflows/ci.yml) actually serializes `docker` after `quality`, so it is a useful candidate for discussing which quality checks could conceptually fan out. Do not assume such a refactor is automatically faster; each job would repeat setup and require enough runners.

## Common Mistakes

- Testing every imaginable combination without a support reason.
- Forgetting Cartesian growth and cost.
- Assuming declared parallelism eliminates runner queues.
- Sharing databases, names, or ports carelessly.
- Splitting tiny work until setup overhead dominates.
- Cancelling useful matrix evidence without understanding fail-fast.
- Failing to combine results into a clear gate.
- Running concurrent production changes without coordination.

## Practical Exercise

Calculate `3 operating systems x 2 runtime versions = 6 jobs`. Exclude one invalid pair, then add one browser dimension with two values and recalculate. Identify runner, cost, and shared-resource risks. Keep the example in notes; do not create a workflow.

## Knowledge Check

1. What does a two-by-two matrix produce?
2. Why can a larger matrix increase queue time?
3. How does test sharding differ from a compatibility matrix?
4. Why should integration jobs use unique resource names?
5. What tradeoff does fail-fast control?

<details>
<summary>View answers</summary>

1. Four job combinations before include or exclude adjustments.
2. Runner limits may prevent all expanded jobs from starting together.
3. Sharding divides one suite; a matrix repeats work across configurations.
4. It prevents races and destructive interference among parallel jobs.
5. Saving resources after an early failure versus collecting complete combination results.

</details>

## Navigation

- [Back to Pipeline Architecture](../README.md)
- [Previous: Conditions and Filters](../04-conditions-and-filters/)
- [Next: Manual Approvals and Quality Gates](../06-manual-approvals-and-quality-gates/)
- [Back to All Learning Materials](../../README.md)
