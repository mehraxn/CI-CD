# Cost, Capacity, Dashboards, and Continuous Optimization

## What CI/CD Actually Costs

The visible bill — **runner minutes** — is a fraction of the total. Full-cost thinking includes **storage** (artifact retention, cache storage, registry images, log ingestion), **network egress**, **monitoring costs** (metric **cardinality** and **trace sampling** rates are cost dials, not just technical settings), and above all people:

```text
Hosted runners:
Usage fees + reduced maintenance

Self-hosted runners:
Infrastructure + maintenance + patching + scaling + security
```

Self-hosted is **not automatically cheaper** — the infrastructure often is, the humans are not ([Topic 04](../../04-pipeline-as-code-and-platforms/05-runners-and-execution-environments/) made the same point about security responsibility). Capacity is cost's twin: **queue depth** and **runner utilization** reveal whether you have **idle capacity** (paying for nothing) or **peak contention** (paying in developer wait); **autoscaling** and **concurrency** limits tune between them, and **capacity planning** means measuring both over time. **Cost allocation** via **tagging** (which team, which project), **budgets**, and **forecasts** keep the spend governed. **Sustainable CI/CD** adds a newer lens — carbon-aware scheduling of flexible workloads — worth knowing exists.

## Dashboards Worth Keeping

| Dashboard area | Useful examples |
|----------------|-----------------|
| Pipeline health | Success rate, duration, queue time |
| Delivery | Deployment frequency, lead time |
| Reliability | Change failure rate, restore time |
| Resources | Runner utilization, queue depth |
| Caching | Hit rate and transfer duration |
| Cost | Runner minutes, storage, network |
| Security | Open findings and remediation age |

Design rules that separate dashboards from wallpaper: a clear **audience** and **owner**, defined **data sources**, a useful **time window**, a *limited* number of actionable signals, links to underlying evidence, and version/environment filters. A **scorecard** (few numbers, targets, trend arrows) serves leadership; an investigation dashboard serves responders — one artifact cannot be both.

## The Optimization Cycle

```text
Measure
  ↓
Find bottleneck
  ↓
Form hypothesis
  ↓
Make limited change
  ↓
Compare against baseline
  ↓
Keep, adjust, or revert
  ↓
Repeat
```

Improvement is an **experiment** discipline: a **baseline**, a **target**, one change at a time, and honest comparison — the same loop for speed, cost, and reliability. An **optimization backlog** with owners and a **review cycle** keeps it running; without ownership, every dashboard decays into last year's numbers.

## Common Mistakes

- Counting runner minutes while ignoring engineer-hours of maintenance.
- Self-hosting to "save money" without staffing it.
- Dashboards without owners or audiences.
- Twenty-panel dashboards nobody reads.
- Optimizing without a baseline (lesson 06's rule, repeated because it is violated constantly).
- Log and metric ingestion growing unbounded because nobody owns retention.
- Cost reviews that never reach the people who can change the pipelines.
- One-off optimizations with no follow-up measurement.

## Existing Repository Evidence

- **Real cost-relevant behaviors**: `cancel-in-progress: true` in [TaskOps CI](../../../Projects/1_project/taskops-cicd/.github/workflows/ci.yml) stops paying for superseded runs; pip and BuildKit caches cut repeat work; branch-restricted push triggers (both CI workflows filter; CD runs only on `main`) avoid pointless runs — each a small, deliberate spend decision already made in the workflows' comments.
- **Real dashboard material**: Project 3's [Grafana dashboard](../../../Projects/3_project/monitoring/grafana-dashboard.json) is the repository's one live dashboard (application traffic; hosted on the compose stack with a persistent `grafana-data` volume); it monitors the *application*, not the pipeline — pipeline health, delivery, cost, and security dashboards from the table above are all absent.
- **Unbounded growth to notice**: per-commit images accumulate in GHCR with no retention policy ([Topic 07](../../07-artifacts-packages-and-registries/07-retention-cleanup-access-and-replication/) proposed one) — the repository's clearest real cost-governance gap.
- Hosted runners only; no utilization, queue, or spend telemetry exists. All governance machinery here is conceptual.

## Practical Exercise

Design a one-page CI/CD scorecard for this repository — the final exercise of the technical topics, deliberately integrative:

1. Pick five signals total, at most one per dashboard-table area, that this repository could realistically populate (name the data source for each: workflow API, GHCR, Grafana, Git history).
2. Set a target and time window per signal.
3. Assign each an owner and the action its regression should trigger.
4. Name the two signals you *wanted* but cannot populate without new instrumentation, and what each would need.
5. Write the first optimization-backlog entry: the highest-value improvement across Topics 05–15's findings (candidates: image retention policy, artifact/report retention, TaskOps CI permissions block, an error-rate SLI) with hypothesis and measurement plan.

Notes only; change nothing. Target 25–35 minutes.

## Knowledge Check

1. Why are self-hosted runners not automatically cheaper?
2. What two capacity signals reveal over- and under-provisioning?
3. What separates a useful dashboard from wallpaper?
4. Why is metric cardinality a cost topic?
5. What real cost-reducing decisions already exist in this repository's workflows?
6. What is the repository's clearest unmanaged-growth example?

<details>
<summary>View answers</summary>

1. The infrastructure price excludes maintenance, patching, scaling, and security work — human costs that often exceed hosted-runner fees.
2. Runner utilization (idle capacity wastes money) and queue depth (contention wastes developer time).
3. A defined audience and owner, few actionable signals with data sources and links to evidence — someone who looks at it and acts.
4. Every distinct label combination is a stored, queried time series; unbounded labels multiply ingestion and query cost.
5. Cancelling superseded runs, dependency and layer caching, and branch-restricted triggers that avoid unnecessary runs.
6. GHCR images accumulating one per main commit with no retention or cleanup policy.

</details>

## Navigation

- [Back to Observability, Metrics, and Optimization](../README.md)
- [Previous: Pipeline Duration, Queues, Caches, and Bottlenecks](../06-pipeline-duration-queues-caches-and-bottlenecks/)
- [Back to All Learning Materials](../../README.md)
