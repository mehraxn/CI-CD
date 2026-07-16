# Health Checks, Zero Downtime, and Traffic Management

## Three Probe Questions

```text
Liveness:
Should this instance be restarted?

Readiness:
Should this instance receive traffic?

Startup:
Has this slow-starting application completed initialization?
```

A single `/health` endpoint may not safely answer all three. Liveness should usually be shallow enough to avoid restart loops during a dependency outage. Readiness controls traffic eligibility and may include essential dependency state. Startup protects slow initialization from premature liveness failure. Deep health can support diagnostics while shallow checks remain stable.

Service discovery, load balancers, DNS, and routers direct traffic only to ready instances. Warm-up and slow-start policies prevent overload. During termination, a pre-stop hook, connection draining, graceful shutdown, and sufficient grace period let active HTTP requests, WebSockets, long-lived connections, background jobs, and queue consumers finish or transfer safely. Timeouts, bounded retries, and circuit breakers reduce cascading failure.

## Zero-Downtime Checklist

- [ ] More than one healthy serving instance exists
- [ ] New instances become ready before receiving traffic
- [ ] Old instances drain connections before termination
- [ ] Old and new versions are compatible
- [ ] Database changes are backward compatible
- [ ] Capacity remains sufficient during rollout
- [ ] Rollback or roll-forward is prepared

Zero downtime is a system property, not a strategy label. It also requires redundancy, compatible sessions or external session state, sufficient surge capacity, safe routing, and observation. Sticky sessions may reduce movement but complicate balancing. One replica cannot remain available while it is stopped and replaced.

Application health and dependency health are related but not identical. Readiness may fail when an essential database is unavailable, removing the instance from traffic; if every instance shares that dependency, removal does not restore service. Liveness should detect a stuck process it can fix by restart, not every upstream outage. Diagnostic deep checks can report dependencies without driving restarts.

Traffic shifting through a load balancer or service mesh can be immediate, weighted, or cohort-based. DNS changes are slower because of caching. Service discovery must stop returning terminating instances. Retries should be bounded and used only for transient/idempotent operations; otherwise they amplify load. Timeouts and circuit breakers constrain waiting and cascading failure.

Graceful shutdown covers web requests, WebSockets, queue consumers, and background work. Stop accepting new work, advertise unready, drain connections, checkpoint or finish safe work, then exit before the termination grace period. A pre-stop hook can initiate this order, but it must not consume the entire grace window.

## Existing Repository Evidence

[KubeOps deployment](../../../Projects/2_project/kubeops-gitops/k8s/deployment.yaml) correctly uses `/health` for liveness and `/ready` for readiness. The [Helm template](../../../Projects/2_project/kubeops-gitops/helm/kubeops/templates/deployment.yaml) mirrors them. No startup probe, pre-stop hook, explicit termination grace, or traffic draining exists. [TaskOps Dockerfile](../../../Projects/1_project/taskops-cicd/Dockerfile) and [Compose](../../../Projects/1_project/taskops-cicd/docker-compose.prod.yml) use `/health`; [CD](../../../Projects/1_project/taskops-cicd/.github/workflows/cd.yml) adds a post-deploy smoke test. TaskOps has one app container, so zero downtime is not demonstrated.

## Common Mistakes

- Readiness always succeeds or traffic arrives before startup.
- Deep liveness causes restart loops.
- Active connections terminate immediately.
- Claiming zero downtime with one replica.
- Ignoring sessions, surge capacity, or schema compatibility.

## Practical Exercise

Map all repository checks to liveness, readiness, startup, Docker health, smoke, or general diagnostics. For each record path, consumer, failure action, dependencies, interval, and missing lifecycle control.

## Knowledge Check

1. What does readiness control?
2. Why can deep liveness be harmful?
3. What is connection draining?
4. Why is one replica insufficient for zero downtime?
5. Which probe type is absent from KubeOps?

<details><summary>View answers</summary>

1. Whether an instance receives traffic.
2. Dependency failure can trigger useless restart loops.
3. Stop new traffic while allowing active work to finish.
4. Replacement creates a period with no serving instance.
5. Startup probe.

</details>

## Navigation

- [Back to Deployment Strategies and Recovery](../README.md)
- [Previous: Feature Flags, Dark Launches, and A/B Testing](../04-feature-flags-dark-launches-and-ab-testing/)
- [Next: Rollback, Roll-Forward, and Failure Recovery](../06-rollback-roll-forward-and-failure-recovery/)
- [Back to All Learning Materials](../../README.md)
