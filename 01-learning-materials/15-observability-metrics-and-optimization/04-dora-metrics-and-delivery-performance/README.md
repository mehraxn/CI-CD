# DORA Metrics and Delivery Performance

## The Four Metrics

The DORA research program distilled delivery performance into two speed and two stability measures:

```text
Deployment frequency:
How often successful production deployments occur.

Lead time for changes:
Time from a code change to successful production deployment.

Change failure rate:
Proportion of production changes that cause failure requiring remediation.

Time to restore service:
Time needed to recover service after a change-related failure or incident.
```

Their power is the pairing: speed without stability is recklessness measured; stability without speed is stagnation measured. Teams strong on all four tend to be practicing everything this repository teaches — small changes, automation, good recovery.

A worked example:

```text
Commit merged: 10:00
Production deployment completed: 14:00

Lead time for this change:
Approximately 4 hours
```

## Definitions Are the Hard Part

Every term above hides decisions your organization must make *consistently*: what counts as a **deployment event** and a **successful deployment**? What is **production scope** (which services count)? What is a **failed change** (rollback? hotfix? any incident within N hours of deploy?), and which **recovery event** stops the restore clock? Measurement details matter too: use **medians/percentiles** over **averages** (one stuck change swamps a mean), pick a **measurement window**, and respect **service/team boundaries** when aggregating.

Real-world complications:

- Several commits may ship in one deployment (whose lead time is it?).
- One commit may deploy to several services.
- **Release ≠ deployment** — a feature flag may release days after its code deployed.
- Failed deployments get retried; partial rollouts blur counting.
- Incidents may have several causes; mobile releases add store delays.

## Interpretation and Misuse

DORA metrics are a flashlight, not a scoreboard:

| Metric | Improvement may indicate | Possible gaming risk |
|--------|--------------------------|----------------------|
| Deployment frequency | Smaller, easier changes | Splitting meaningless deployments |
| Lead time | Faster feedback | Skipping review or testing |
| Change failure rate | Safer delivery | Hiding failures |
| Restore time | Better recovery | Closing incidents early |

Misuse patterns to refuse: comparing unrelated teams without context, rewarding deployment counts, redefining incidents to flatter the numbers, using averages that hide long tails, treating DORA as *individual* performance metrics (they measure systems, not people), ignoring reliability and user outcomes, and optimizing speed by weakening the controls Topics 03–14 built. **Data quality** underlies everything — metrics computed from incomplete deployment or incident records are confident nonsense. Used well, the metrics are trend instruments for **continuous improvement**: did *our* lead time improve after *our* change, over months not weeks?

## Common Mistakes

- Measuring before defining terms.
- Averages instead of medians and percentiles.
- Counting deployments nobody needed.
- Failure data collected only when convenient.
- Cross-team league tables.
- One quarter of data treated as a trend.
- Metrics without any improvement action attached.

## Existing Repository Evidence

**No DORA measurement is implemented** — no deployment records beyond workflow history, no incident tracking, no dashboards. But the *raw data* for a minimal implementation already exists, which is exactly what the exercise uses:

- **Deployment events**: every successful [TaskOps CD](../../../Projects/1_project/taskops-cicd/.github/workflows/cd.yml) run on `main` *is* a production deployment, timestamped by the platform; KubeOps deployments are Argo CD syncs, recorded in Git history (values changes) plus controller history.
- **Lead time endpoints**: commit timestamps (merge to `main`) and CD-run completion times bracket each change's journey.
- **Change failure signals**: a failed CD run, a `rollback.sh` invocation (the [script](../../../Projects/1_project/taskops-cicd/scripts/rollback.sh) exists; invocations are not currently logged anywhere durable), or a failed post-deploy smoke test.
- **Restore signals**: time between a failed smoke test and the next successful deployment or rollback.

The honest caveat: with a single-developer portfolio repository, these numbers describe the automation's shape, not team performance — a correct scope observation this lesson's interpretation rules demand.

## Practical Exercise

Design (do not implement) DORA measurement for TaskOps from repository-native data:

1. Define all four metrics operationally for this repository — exact event sources, using workflow runs, commit timestamps, and script/state evidence named above.
2. State your definition decisions explicitly: what counts as production, a failed change, and a recovery.
3. Identify the two data gaps that make change-failure rate and restore time unreliable today (hint: where are rollbacks and incidents recorded?).
4. Choose median or percentile per metric and justify.
5. Write one sentence on what these numbers can and cannot say about a solo portfolio project.

Target 20–30 minutes.

## Knowledge Check

1. Why do the four metrics come as speed/stability pairs?
2. Why must "failed change" be defined before measuring change failure rate?
3. Why medians and percentiles rather than averages?
4. How can release-versus-deployment separation distort lead time?
5. Name two gaming risks and the honest practice that prevents each.
6. Which DORA inputs already exist in this repository, and which are missing?

<details>
<summary>View answers</summary>

1. Optimizing speed alone encourages recklessness and stability alone encourages stagnation; the pairs keep both visible so neither is bought by sacrificing the other.
2. Without a fixed definition (rollback? hotfix? incident within a window?), the rate can be silently redefined until it flatters — the number means nothing.
3. Delivery times are long-tailed; one stuck change distorts a mean, while medians and percentiles describe typical and worst-case honestly.
4. With feature flags, code can deploy quickly (short measured lead time) while users see the feature much later — the metric measures deployment, not delivery of value.
5. Splitting meaningless deployments (prevented by measuring outcomes alongside frequency) and hiding failures (prevented by fixed, audited failure definitions).
6. Existing: timestamped deployment events (CD runs), commit timestamps, smoke-test results. Missing: durable rollback/incident records to compute failure and restore metrics reliably.

</details>

## Navigation

- [Back to Observability, Metrics, and Optimization](../README.md)
- [Previous: Deployment Monitoring, Alerting, SLIs, and SLOs](../03-deployment-monitoring-alerting-slis-and-slos/)
- [Next: Incidents, Runbooks, On-Call, and Postmortems](../05-incidents-runbooks-on-call-and-postmortems/)
- [Back to All Learning Materials](../../README.md)
