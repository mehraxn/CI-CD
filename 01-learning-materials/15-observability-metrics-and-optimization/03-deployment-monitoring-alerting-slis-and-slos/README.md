# Deployment Monitoring, Alerting, SLIs, and SLOs

## Watching a Release Land

A deployment is a hypothesis ("this version is fine") that monitoring tests:

```text
Deploy new version
       ↓
Record deployment marker
       ↓
Watch technical and business SLIs
       ↓
Compare with baseline
       ↓
Continue, pause, roll forward, or roll back
```

The watch list mixes **health checks** and **smoke tests** (immediate: is it up?), **synthetic checks** (scripted user actions on a schedule), **application metrics**, **infrastructure metrics**, and — often the earliest honest signal — **business metrics** (orders per minute drops before CPU notices anything). The **golden signals** organize the technical side: **latency**, **traffic**, **errors**, **saturation**. A **verification window** with defined **rollback criteria** turns watching into a decision procedure ([Topic 10](../../10-deployment-strategies-and-recovery/) covers the strategies that consume it).

## SLIs, SLOs, and Error Budgets

```text
SLI:
A measured indicator of service behavior.

SLO:
A target for an SLI over a defined period.

SLA:
A formal agreement that may include consequences.

Error budget:
The amount of allowed unreliability implied by the SLO.
```

A worked pair:

```text
SLI:
Percentage of successful API requests.

SLO:
99.9% successful requests over 30 days.
```

A complete SLO defines: the **service**, the **measurement** (which metric, measured where), the **success condition** (what counts as good), the **time window**, the **data source**, and **ownership**. The 0.1% the SLO tolerates is the **error budget** — a shared currency between speed and stability: budget remaining means deploys can proceed; budget exhausted means reliability work takes priority. **Burn rate** measures how fast the budget is being consumed — the basis of modern **multi-window alerts** (page on fast burn, ticket on slow burn).

## Alerting That Humans Can Live With

- Alert on **user-impacting symptoms** (error rate, latency) rather than causes (CPU) where possible.
- Not every metric needs an alert; dashboards exist for the rest.
- Every alert needs an **actionable response** — ideally a runbook (lesson 05); an alert nobody can act on is noise.
- Severity tiers: **paging** alerts (wake someone), **ticket** alerts (business hours), **dashboard-only** signals.
- Routing, **grouping**, **deduplication**, and inhibition (suppressing downstream alerts when the upstream cause already fired) are what Alertmanager-class tools do.
- **Alert fatigue** is the failure mode that kills everything else: too many false pages and humans stop believing the pager.
- Deployment-time specifics: alerts should carry **version and environment**; static **thresholds** may misfire during deployments — but suppressing alerts during deploys needs safeguards, because deployment is exactly when things break.

## Common Mistakes

- An alert for every warning.
- No runbook attached.
- Alerts without owners.
- SLOs copied from another service's numbers.
- Availability measured only as process uptime (up but erroring counts as "available").
- No deployment markers, so regressions cannot be tied to releases.
- Alerting only on infrastructure CPU.
- Error budget used as permission to ignore incidents.
- Production releases accepted immediately with no verification window.
- Alerts suppressed during deployment without safeguards.

## Existing Repository Evidence

- **Post-deployment verification, implemented**: [TaskOps CD](../../../Projects/1_project/taskops-cicd/.github/workflows/cd.yml) runs a smoke test against the live `/health` after deploy — a one-shot verification window with automatic failure signaling; container `HEALTHCHECK`s and KubeOps' readiness/liveness probes supply continuous health signals.
- **SLI raw material, implemented (Project 3)**: `REQUESTS_TOTAL` in [main.py](../../../Projects/3_project/app/main.py) is scraped by [Prometheus](../../../Projects/3_project/monitoring/prometheus.yml) and charted in [Grafana](../../../Projects/3_project/monitoring/grafana-dashboard.json) — traffic exists as a signal today; error-rate and latency SLIs would need labeled counters and histograms not yet present.
- **Alerting, documented-only**: no Alertmanager and no alert rules exist anywhere; the [KubeOps monitoring README](../../../Projects/2_project/kubeops-gitops/monitoring/README.md) *suggests* future alerts (pod restart rate, readiness failing, p95 latency) — a reasonable starter set this lesson's exercise builds on.
- **Deployment markers**: absent — no annotation records when a version lands; the `/version` endpoint in Project 3 at least lets you ask a running instance what it is.

## Practical Exercise

Design the monitoring the repository is one step away from. Using Project 3's real signals plus KubeOps' suggested alerts, classify:

```text
Signal
SLI candidate
Alert rule
Owner
Action
Deployment relevance
```

Cover: the request counter (what must be added to make an error-rate SLI?), `/health`–`/ready` probes, pod restart rate, and p95 latency (which metric type is missing for it?). Then write one complete SLO for the Project 3 app — service, measurement, success condition, window, data source, owner — and state which of its inputs exist today versus need instrumentation. Do not modify any monitoring configuration. Target 25–35 minutes.

## Knowledge Check

1. What must a complete SLO define beyond a percentage?
2. What is an error budget, and what tension does it manage?
3. Why alert on symptoms rather than causes where possible?
4. Why is process uptime a poor availability SLI?
5. What real post-deployment verification exists in this repository?
6. Which SLI ingredients exist in Project 3 today, and which are missing?

<details>
<summary>View answers</summary>

1. The service, the exact measurement and data source, the success condition, the time window, and an owner.
2. The unreliability the SLO tolerates, treated as spendable budget — balancing deployment speed against reliability work with one number.
3. Symptoms are what users experience; causes are hypotheses. CPU can be high while users are fine, and users can suffer while CPU is idle.
4. A process can be up and serving errors; availability should measure successful service, not existence.
5. TaskOps CD's post-deploy smoke test against the live health endpoint, plus continuous container health checks and Kubernetes probes.
6. Traffic exists (the scraped request counter); error-rate needs status labels and latency needs a histogram — neither is instrumented yet.

</details>

## Navigation

- [Back to Observability, Metrics, and Optimization](../README.md)
- [Previous: Pipeline Observability, Debugging, and Evidence](../02-pipeline-observability-debugging-and-evidence/)
- [Next: DORA Metrics and Delivery Performance](../04-dora-metrics-and-delivery-performance/)
- [Back to All Learning Materials](../../README.md)
