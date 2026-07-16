# Recreate and Rolling Deployments

## Replacement Models

```text
Recreate:
Old version stopped
        ↓
New version started
```

Recreate is stop-before-start. It is simple, uses little extra capacity, and commonly causes downtime. It can fit single-instance systems, incompatible versions, or low-risk maintenance windows.

```text
Rolling:
Old Old Old
 ↓
New Old Old
 ↓
New New Old
 ↓
New New New
```

A rolling update incrementally replaces desired replicas. Old and new replicas coexist, so API, session, cache, and database compatibility are essential. Surge capacity controls extra new replicas; unavailable capacity controls how many desired replicas may be down.

Conceptual Kubernetes examples:

```yaml
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxSurge: 1
    maxUnavailable: 0
```

```yaml
strategy:
  type: Recreate
```

Readiness keeps new pods out of traffic until ready; liveness restarts unhealthy ones. Connection draining and session design protect active work. A rolling restart replaces pods without changing application version and is not itself a new deployment.

Deployment duration depends on replica count, startup time, readiness thresholds, and allowed surge/unavailability. `maxUnavailable: 0` protects desired serving count but requires capacity for surge; a percentage can round differently on small deployments. Slow readiness or a failing new pod should pause progress rather than remove more old capacity.

Version overlap is the defining rolling risk. Both versions may read/write the same database, call each other, share sessions, consume queues, and interpret cached data. Backward-compatible APIs and expand-and-contract schema changes allow that overlap. In-memory sessions may disappear as pods rotate; shared or client-side sessions need format compatibility.

Rollback is itself another rollout and must be observed. The previous artifact, configuration, and schema must remain usable. A rolling restart can refresh configuration or recover stuck processes, but it does not introduce a newly verified artifact and should not be reported as a software release.

## Existing Repository Evidence

[KubeOps raw Deployment](../../../Projects/2_project/kubeops-gitops/k8s/deployment.yaml) and [Helm template](../../../Projects/2_project/kubeops-gitops/helm/kubeops/templates/deployment.yaml) omit `strategy`, `maxSurge`, and `maxUnavailable`. A Kubernetes Deployment therefore uses its platform default RollingUpdate, but the repository does not explicitly choose or tune it. Values request two dev and three production replicas. Liveness and readiness probes exist; no startup probe or connection draining configuration exists. TaskOps Compose uses one app container, so its update cannot claim zero downtime.

## Common Mistakes

- Calling rolling automatically zero downtime.
- Omitting readiness or allowing too much unavailability.
- Using incompatible schema or shared state.
- Lacking surge capacity or session compatibility.
- Assuming restart equals deployment.
- Observing no rollback.

## Practical Exercise

Inspect both KubeOps deployment definitions and values. Record explicit versus default strategy, replicas, probes, capacity implications, version-overlap risks, and what would need evidence before claiming zero downtime. Do not edit manifests.

## Knowledge Check

1. Why does recreate commonly cause downtime?
2. What coexists during rolling deployment?
3. What do `maxSurge` and `maxUnavailable` control?
4. Does KubeOps explicitly configure rolling behavior?
5. Why is readiness essential?

<details><summary>View answers</summary>

1. Old instances stop before new ones serve.
2. Old and new application versions.
3. Temporary extra capacity and permitted unavailable desired capacity.
4. No; the files omit strategy and rely on the Kubernetes default.
5. It prevents traffic reaching an instance before it can serve safely.

</details>

## Navigation

- [Back to Deployment Strategies and Recovery](../README.md)
- [Next: Blue-Green Deployment](../02-blue-green-deployment/)
- [Back to All Learning Materials](../../README.md)
