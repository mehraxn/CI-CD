# Logs, Metrics, Traces, and Observability Fundamentals

## Three Signals, Three Shapes

**Telemetry** is everything a system emits about itself; three signal shapes dominate:

```text
Logs:
Detailed event records.

Metrics:
Numerical measurements over time.

Traces:
The path and timing of work across components.
```

| Signal | Best for | Main limitation |
|--------|----------|-----------------|
| Logs | Detailed event investigation | High volume and search cost |
| Metrics | Trends, thresholds, and alerts | Limited detail |
| Traces | Cross-service latency and flow | Sampling and instrumentation complexity |

**Monitoring** checks known signals against known conditions; **observability** is the broader property that lets you answer questions you did not anticipate. You monitor "error rate above 1%"; you need observability for "why are only Belgian users on the new version seeing 500s?"

## Logs

A log records an **event** with a **timestamp** and a **level** (DEBUG/INFO/WARNING/ERROR). **Structured logging** — machine-parseable fields instead of prose — is what makes logs searchable at scale:

```json
{
  "timestamp": "2026-01-01T10:00:00Z",
  "level": "INFO",
  "service": "task-api",
  "request_id": "example-request",
  "message": "Task created"
}
```

(Identifiers here are examples.) The **correlation/request ID** is the field that turns thousands of interleaved lines into one request's story — every service touching the request logs the same ID. Loki is a common log store in the Prometheus ecosystem; Elasticsearch/Kibana the older standard.

## Metrics

A **metric** is a named number sampled over time — a **time series** — in a few shapes: **counters** (only increase: requests served), **gauges** (rise and fall: memory in use), **histograms** (distributions: request duration buckets, the basis of percentiles), and summaries. **Labels** slice a metric (`service`, `environment`, `status_code`), and here lives the classic trap: **cardinality**. Each distinct label combination is a separate time series — `service` and `environment` are fine; user IDs, request IDs, or any unbounded value multiply series until cost and query load explode. High-detail identifiers belong in logs and traces, which are built for them. **Prometheus** (pull-based scraping, the repository's real tool) and **Grafana** (dashboards) are the reference stack.

## Traces

A **trace** follows one request across components as a tree of **spans** (each an operation with timing); **context propagation** carries trace/span IDs across service calls, and **sampling** keeps volume affordable. **OpenTelemetry** is the vendor-neutral instrumentation standard; Jaeger a common backend. Traces answer "where did the latency go?" across services — overkill for a monolith, indispensable for twenty microservices.

Two connective concepts complete the picture: **dashboards** and **alerts** consume these signals (lesson 03), and **deployment/release markers** — annotations recording *when a version changed* — turn "the graph got worse" into "the graph got worse at 14:02, right at the deploy." **Retention** policies bound cost; **aggregation** and query languages (PromQL) turn raw series into answers.

## Common Mistakes

- Unstructured prose-only logs.
- Secrets or personal data in logs.
- Missing timestamps (or local-time timestamps).
- Different services using incompatible field names.
- Metrics with unbounded labels.
- Alerts based on raw log volume.
- Traces without context propagation — trees with no branches.
- Telemetry retained forever.
- Monitoring infrastructure but not application behavior.
- Dashboards with no owner.

## Existing Repository Evidence

- **Metrics, implemented (Project 3)**: [main.py](../../../Projects/3_project/app/main.py) uses `prometheus_client` to define a request **Counter** (`REQUESTS_TOTAL`) and serve `/metrics`; [prometheus.yml](../../../Projects/3_project/monitoring/prometheus.yml) scrapes it every 15 s at `cloudops-app:8000`; the [Grafana dashboard JSON](../../../Projects/3_project/monitoring/grafana-dashboard.json) charts it; the Compose stack pins `prom/prometheus:v3.5.0` and `grafana/grafana:12.1.0` with a persistent `grafana-data` volume; [docs/monitoring.md](../../../Projects/3_project/docs/monitoring.md) documents the whole loop.
- **Documented-only (KubeOps)**: the [monitoring README](../../../Projects/2_project/kubeops-gitops/monitoring/README.md) states plainly that health endpoints, stdout logs, and probes exist today, while `/metrics`, Prometheus/Grafana, and alerts are a documented *future* plan — a model of honest signal inventory.
- **Logs**: all three apps log to stdout (container-native); none emit structured JSON logs — the example above is conceptual here.
- **Absent**: tracing (no OpenTelemetry anywhere), log aggregation (no Loki/ELK), Alertmanager, and deployment markers.

## Practical Exercise

Inventory the repository's telemetry:

```text
Signal
Source
Collection tool
Storage
Dashboard
Alert
Retention evidence
Missing information
```

Fill one row each for: Project 3 request metrics, Project 3 health endpoints, KubeOps probes/logs, TaskOps health checks, and (as an absent row) traces. Use only file evidence; mark unknowable runtime facts (does Prometheus actually run anywhere now?) as unknowable. Conclude with the single highest-value missing signal for each project. Target 25–35 minutes.

## Knowledge Check

1. When do you reach for logs versus metrics versus traces?
2. What distinguishes observability from monitoring?
3. Why do request IDs belong in logs but not in metric labels?
4. What is a counter, and which real counter exists in this repository?
5. What does a deployment marker add to a dashboard?
6. Which project documents its planned-versus-implemented monitoring explicitly?

<details>
<summary>View answers</summary>

1. Logs for detailed event investigation, metrics for trends/thresholds/alerts over time, traces for cross-component latency and flow of a single request.
2. Monitoring checks known conditions; observability is the ability to answer unanticipated questions from the available telemetry.
3. Each distinct label value creates a new time series — unbounded values explode cardinality and cost; logs and traces are designed for per-request detail.
4. A metric that only increases, counting occurrences — Project 3's `REQUESTS_TOTAL` request counter served at `/metrics`.
5. The moment a version changed, turning correlation ("worse since 14:02") into a deployment-shaped hypothesis instantly.
6. KubeOps — its monitoring README separates what exists today from the documented future Prometheus/Grafana/alerting plan.

</details>

## Navigation

- [Back to Observability, Metrics, and Optimization](../README.md)
- [Next: Pipeline Observability, Debugging, and Evidence](../02-pipeline-observability-debugging-and-evidence/)
- [Back to All Learning Materials](../../README.md)
