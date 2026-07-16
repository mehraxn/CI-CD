# Performance Testing

## Beyond "Does It Work"

Performance testing asks how the system behaves under load: how much **throughput** it sustains (requests per second), what **latency** users experience, and what resources it burns doing so. A **benchmark** measures a specific operation's speed in isolation; system-level tests come in flavors defined by their load shape:

```text
Load test:
Tests expected or projected usage.

Stress test:
Pushes beyond normal capacity to observe failure behavior.

Spike test:
Applies a sudden increase in traffic.

Soak test:
Runs for a long period to reveal leaks or degradation.
```

(A **soak test** is also called an **endurance test**; a **scalability test** measures how performance changes as resources are added.)

## Reading the Numbers

Averages lie. If 99 requests take 20 ms and one takes 4 seconds, the average (~60 ms) describes no request that actually happened. Report **percentiles**: p50 (median), p95, p99 — "p99 = 800 ms" means 1% of requests were slower than 800 ms, and that 1% is often your busiest users. Alongside latency and throughput, watch **resource utilization** — CPU, memory, disk, network — because the resource that saturates first is the **bottleneck**, and finding it is usually the test's real product. **Concurrent users** and request rate are related but distinct load models; know which one your tool is holding constant. External **rate limits** (and shared infrastructure) can silently become the thing you are measuring.

## Method Discipline

Performance numbers are only meaningful against a **baseline** measured in a comparable environment:

- **Warm-up first** — caches, JIT compilers, and connection pools make the first minute unrepresentative.
- **Test duration** long enough for stable numbers; a 10-second run is noise.
- **Production-like environment** — results from a laptop or a shared CI runner do not transfer; comparing runs from *different* environments is meaningless.
- **Realistic test data** — an empty database is fast; production tables are not.
- A **performance regression** is a change relative to the baseline — which is why results need **storage and trend analysis**, not one-off eyeballing.

## Performance in the Pipeline

**Pass/fail criteria** turn measurements into **performance gates** — but noisy thresholds fail randomly and teach people to ignore the gate. The workable split: **pull-request performance tests** stay small and stable (a quick benchmark of a hot path, generous thresholds guarding against order-of-magnitude regressions), while larger load tests run **on schedules** against dedicated environments, with humans reviewing trends. Load generation and dedicated environments have real **cost** — another reason full load tests do not belong on every commit.

A conceptual invocation (k6 is *not* present in this repository):

```bash
k6 run tests/performance/smoke.js
```

## Common Mistakes

- Running load tests against shared production unintentionally.
- Comparing results from different environments.
- Using averages only.
- No warm-up.
- No baseline.
- Unrealistic test data.
- Treating one run as a trend.
- Failing the pipeline on noisy thresholds.
- Ignoring infrastructure cost.

## Existing Repository Evidence

The repository contains **no performance tests** — no k6, Locust, JMeter, or benchmark suites; nothing here should be mistaken for one. Two adjacent real assets are worth knowing: the TaskOps health checks verify *availability*, not performance; and [Project 3's monitoring stack](../../../Projects/3_project/monitoring/) (Prometheus and Grafana) is the kind of observability that performance testing feeds — measured latency and throughput become meaningful when the same metrics are watched in production (Topic 15 territory). Performance testing may be added in a later project-enhancement phase; this lesson is conceptual.

## Practical Exercise

Design (do not implement) a performance-test plan for the TaskOps API:

1. Choose one endpoint and justify it by risk.
2. Define the load model: concurrent users or request rate, warm-up, duration.
3. Define pass/fail criteria using percentiles, not averages, and state your baseline strategy.
4. Specify the environment and test data, and explain why the CI runner is or is not acceptable for your plan.
5. Decide what runs on pull requests versus on a schedule, and why.

Keep it to one page of notes. Target 20–30 minutes.

## Knowledge Check

1. What distinguishes load, stress, spike, and soak tests?
2. Why are averages misleading for latency?
3. Why does a performance number need a baseline and a comparable environment?
4. Why should heavyweight load tests not run on every pull request?
5. What is the danger of noisy performance gates?

<details>
<summary>View answers</summary>

1. Load tests expected usage; stress pushes beyond capacity to observe failure; spike applies sudden traffic jumps; soak runs long to expose leaks and degradation.
2. A few very slow requests hide inside a comfortable average; percentiles (p95, p99) expose the tail that real users experience.
3. Absolute numbers are meaningless — only change relative to a baseline signals regression, and environment differences swamp code differences.
4. They are slow, costly, environment-sensitive, and noisy — better run scheduled against dedicated environments with trend review.
5. Random failures train the team to rerun and ignore the gate, destroying its value; thresholds must be stable enough to mean something.

</details>

## Navigation

- [Back to Automated Testing and Quality](../README.md)
- [Previous: API, Contract, End-to-End, and Smoke Testing](../05-api-contract-end-to-end-and-smoke-testing/)
- [Next: Coverage, Reports, and Quality Gates](../07-coverage-reports-and-quality-gates/)
- [Back to All Learning Materials](../../README.md)
