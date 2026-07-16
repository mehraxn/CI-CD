# Pipeline Duration, Queues, Caches, and Bottlenecks

## Optimize the Right Number

The number that matters is not compute consumed — it is how long humans wait:

```text
Total developer wait time
        =
Queue time
+ execution time
+ approval wait
+ retry or rerun time
```

**Queue time** (waiting for a runner) is invisible in job durations and often dominates on busy days; **retry/rerun time** is the tax flaky tests levy on everyone. Optimizing execution while ignoring the other three polishes a third of the problem.

## The Critical Path

With parallel jobs, total duration is set by the longest dependency chain, not the sum:

```text
Build: 4 minutes
Unit tests: 3 minutes
Integration tests: 10 minutes
Security scan: 5 minutes
Package: 2 minutes

Critical path:
Build → Integration tests → Package
Approximately 16 minutes
```

Adding all durations (24 minutes) is wrong when tests and scans run in parallel after Build. Consequence: speeding up the security scan changes *nothing* here — only critical-path work moves the total. This is [Topic 03's DAG lesson](../../03-pipeline-architecture/03-job-dependencies-and-dag-pipelines/) wearing an optimization hat.

## Where the Time Hides

| Symptom | Possible investigation |
|---------|------------------------|
| Long queue time | Runner capacity or concurrency limits |
| Slow dependency install | Cache or lockfile behavior |
| Slow image build | Docker layer order and remote cache |
| Slow test job | Test selection, sharding, or fixtures |
| Frequent reruns | Flaky tests or infrastructure instability |
| Slow artifact transfer | Artifact size or unnecessary files |

Cache-specific honesty: a **cache hit** is only a win if **restore duration** is less than the work it saves — huge caches can restore slower than a fresh install; **cache upload** time is paid on every save. Image work splits into **build time** (layer order, remote cache — [Topic 05](../../05-builds-dependencies-and-caching/04-build-caching/)) and **pull time** (image size). External friction — **network latency**, **registry rate limits** — masquerades as tool slowness. And **matrix size**, **timeouts**, and **cancellation** policy decide how much work is wasted versus cut short.

## Optimization Principles

- **Measure before changing** — and against a **baseline**, using **percentiles** (p50 and p90 tell different stories) and **trends**, never one run.
- **Optimize the critical path first.**
- **Do not remove valuable checks solely for speed** — a fast pipeline that misses regressions is a fast path to incidents.
- Separate **fast feedback** from slower comprehensive validation (per-push versus main/nightly suites).
- Cache only safe, recreatable data.
- More parallelism may increase cost and *queue pressure* — jobs beyond runner capacity just wait in a different place.
- Cancellation of superseded runs reduces wasted work.
- Compare successful and failed runs separately — failures have different duration profiles.
- Treat each change as an **experiment**: hypothesis, one change, measured result, watch for **regression**.

## Common Mistakes

- Optimizing total compute rather than developer wait.
- Ignoring queue time entirely.
- Assuming a cache hit always saves time.
- Caching unstable outputs.
- Matrix combinations with little value.
- Retrying deterministic failures.
- Unlimited parallelism.
- Removing security checks for speed.
- Measuring one run and declaring victory.
- No baseline before optimizing.

## Existing Repository Evidence

- **A real critical path to map**: [TaskOps CI](../../../Projects/1_project/taskops-cicd/.github/workflows/ci.yml) is strictly sequential across jobs — `quality` (checkout, Python setup, pip install, six check steps) then `docker` (Buildx, cached build, Trivy, container start, up-to-10-poll smoke test, cleanup). With no parallel branches, everything is critical path; [Topic 06's optimization lesson](../../06-automated-testing-and-quality/08-parallel-tests-flaky-tests-and-optimization/) already sketched what could fan out.
- **Real duration reducers in place**: pip caching via `setup-python`, BuildKit layer caching (`type=gha`) in both TaskOps workflows, cache-friendly Dockerfile layer ordering, and `cancel-in-progress: true` cutting superseded CI runs. KubeOps CI has the pip cache but builds its image with no remote layer cache — a measurable contrast candidate.
- **A designed wait**: [TaskOps CD](../../../Projects/1_project/taskops-cicd/.github/workflows/cd.yml)'s serialized concurrency means deployment runs can queue behind each other on purpose — queue time that is a safety feature, not a defect.
- **A bounded retry cost**: the smoke test's 10 × 3-second poll caps at ~30 seconds of legitimate readiness wait.
- **Absent**: any duration tracking, baselines, percentile dashboards, or measured cache hit rates — all analysis today means reading individual run pages.

## Practical Exercise

Build a theoretical duration map of [TaskOps CI](../../../Projects/1_project/taskops-cicd/.github/workflows/ci.yml). List every step in both jobs, estimate a plausible duration and a cache-cold duration for each, and compute:

1. The critical path (trivial here — say why) and total wait for the cache-warm and cache-cold cases.
2. The two steps where a requirements change hurts most, and why (which caches invalidate).
3. What fanning `quality`'s six checks into three parallel jobs would save on paper — and the two overheads it would add.
4. Which single measurement you would collect for two weeks before changing anything.

Notes only; modify nothing. Target 25–35 minutes.

## Knowledge Check

1. What four components make up developer wait time?
2. Why is summing job durations wrong for parallel pipelines?
3. When is a cache hit not a win?
4. Why can more parallelism make waiting worse?
5. What queue time in this repository is deliberate?
6. What must exist before any optimization is attempted?

<details>
<summary>View answers</summary>

1. Queue time, execution time, approval wait, and retry/rerun time.
2. Parallel jobs overlap; total duration equals the longest dependency chain (critical path), not the sum of all work.
3. When restore (plus eventual upload) takes longer than the work saved — oversized caches can lose to a fresh install.
4. Jobs beyond runner capacity queue; parallelism converts execution time into queue time while raising cost.
5. TaskOps CD's serialized deployment concurrency — runs queue so deployments never overlap or cancel mid-flight.
6. A measured baseline over multiple runs (percentiles, trend), so the change's effect is attributable and regressions visible.

</details>

## Navigation

- [Back to Observability, Metrics, and Optimization](../README.md)
- [Previous: Incidents, Runbooks, On-Call, and Postmortems](../05-incidents-runbooks-on-call-and-postmortems/)
- [Next: Cost, Capacity, Dashboards, and Continuous Optimization](../07-cost-capacity-dashboards-and-continuous-optimization/)
- [Back to All Learning Materials](../../README.md)
