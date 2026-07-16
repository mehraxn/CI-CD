# Blue-Green Deployment

## Two Complete Environments

```text
Users
  ↓
Router
  ├── Blue: version 1 — active
  └── Green: version 2 — validated but inactive
```

After warm-up, readiness, and smoke testing:

```text
Users
  ↓
Router
  ├── Blue: version 1 — standby
  └── Green: version 2 — active
```

Blue and green are complete, named environments. A load balancer, router, Kubernetes Service selector, or sometimes DNS switches traffic. Keeping the old environment healthy can make rollback a fast traffic switch, but only while data, configuration, and dependencies remain compatible.

The strategy usually duplicates capacity and can expose environment drift. Shared databases complicate schema changes; duplicated background jobs and queue consumers may process work twice. Cache formats, sticky sessions, long-lived connections, stateful services, and DNS caching prevent an instantaneous clean switch. Warm-up and connection draining matter on both sides.

A conceptual Kubernetes shape is two Deployments, `blue` and `green`, with a Service selector pointing to one color. Two replicas of one Deployment are not blue-green. The traffic switch and its actor/result need an audit record; cleanup waits until rollback risk has passed.

Validation before switch should reach green directly through a private route, run smoke and compatibility tests, and verify production configuration without serving public traffic. Warm-up may populate caches, establish connections, or compile runtime state. The switch should have one authoritative mechanism and an observable result.

Session handling determines user experience. Server-local sessions may strand users on blue; shared sessions require both versions to understand the format. Long-lived connections remain on the old color until drained, so “100% switched” may still include blue traffic. Background workers need active/standby ownership separate from web routing.

Data migration is often the hardest constraint. Both colors sharing one database need backward-compatible schema. Separate databases require replication, cutover, conflict handling, and a data rollback plan. After the observation window, cleanup removes idle capacity deliberately while retaining release evidence and any required rollback artifacts.

## Existing Repository Evidence

No project defines parallel blue/green deployments, color selectors, or a traffic switch. TaskOps has one Compose application service behind [nginx](../../../Projects/1_project/taskops-cicd/docker/nginx.conf). KubeOps has one Deployment and one Service. Blue-green remains conceptual and may be introduced later.

## Common Mistakes

- Switching before warm-up or destroying old immediately.
- Sharing an incompatible database.
- Running background work twice.
- Allowing configuration drift.
- Ignoring sessions, connections, DNS caching, or switch auditing.
- Calling two replicas blue-green.

## Practical Exercise

Design—not implement—a blue-green TaskOps flow. Define two stacks, database compatibility, background-work ownership, nginx switch, pre-switch checks, connection handling, rollback threshold, audit record, and cleanup time.

## Knowledge Check

1. What makes blue-green different from two replicas?
2. Why can rollback be fast?
3. Why is a shared database difficult?
4. Why may DNS be a poor instant switch?
5. Is blue-green implemented here?

<details><summary>View answers</summary>

1. Each color is a complete independently addressable version and traffic selects one.
2. The old healthy environment remains ready to receive traffic.
3. Both versions must understand the same schema and data during overlap.
4. Resolver and client caches delay propagation.
5. No.

</details>

## Navigation

- [Back to Deployment Strategies and Recovery](../README.md)
- [Previous: Recreate and Rolling Deployments](../01-recreate-and-rolling-deployments/)
- [Next: Canary and Progressive Delivery](../03-canary-and-progressive-delivery/)
- [Back to All Learning Materials](../../README.md)
