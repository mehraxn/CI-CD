# Feature Flags, Dark Launches, and A/B Testing

## Different Controls

```text
Feature flag:
Controls whether behavior is enabled.

Canary deployment:
Controls which software version receives traffic.

A/B test:
Compares user outcomes between controlled variants.

Dark launch:
Deploys code or infrastructure without exposing the feature broadly.
```

Feature toggles include temporary release flags, operational kill switches, experiment flags, and permission flags. A flag can target internal users, percentages, cohorts, tenants, or regions. Permission flags still require server-side authorization; a client-visible toggle is not a security boundary.

```text
Deploy version 2 to production
        ↓
Feature remains disabled
        ↓
Enable for internal users
        ↓
Enable for 10%
        ↓
Enable for 100%
        ↓
Remove temporary release flag
```

A dark launch can warm infrastructure or shadow work without user exposure. A/B testing assigns control and experiment groups to measure outcomes; it is a product experiment, not automatically a safety gate. Remote configuration may evaluate flags centrally. Safe offline behavior and defaults must be explicit.

Every flag needs purpose, owner, creation/expiry date, variants, audit trail, monitoring, and removal criteria. Test enabled and disabled paths. Stale flags and interacting combinations create technical debt; sensitive targeting data raises privacy concerns. During incidents, record flag state. A kill switch can reduce feature blast radius but cannot reverse data already changed.

Release flags are temporary controls for gradual availability. Operational flags tune or disable behavior during incidents. Experiment flags assign variants, while permission flags express entitlements but must be enforced by trusted backend authorization. Mixing these purposes makes removal and auditing dangerous.

Flag evaluation may occur locally from configuration or through a remote service. Define the default and offline behavior: failure-open may expose an unfinished feature; failure-closed may disable critical service. Cache and update behavior affect how quickly a kill switch takes effect. Audit who changed a production flag, from what value to what value, and why.

Dark launches may execute shadow reads or duplicate calculations, but must avoid duplicated writes and privacy surprises. A/B tests need stable groups, a hypothesis, success/guardrail metrics, and an end date. Percentage rollout for safety and experimentation can look similar technically but answer different questions.

## Existing Repository Evidence

No application or workflow implements feature flags, dark launches, A/B groups, remote flag configuration, or percentage/tenant targeting. Deployments and release happen together in the demonstrated flows. These patterns remain conceptual.

## Common Mistakes

- Never removing flags or documenting ownership.
- Testing only enabled behavior.
- Using frontend flags to protect sensitive operations.
- Having no safe default during service outage.
- Omitting flag state from incident diagnosis.
- Creating too many combinations.
- Confusing experiments with deployment safety.

## Practical Exercise

Design a temporary TaskOps release flag for a hypothetical task-export feature. Define name, server evaluation, disabled default, internal and percentage stages, metrics, kill behavior, owner, audit fields, privacy limits, and removal date. Do not implement it.

## Knowledge Check

1. How does a flag differ from a canary?
2. Why is a client flag not authorization?
3. What is a dark launch?
4. Why remove release flags?
5. Are flags implemented here?

<details><summary>View answers</summary>

1. A flag selects behavior; a canary routes traffic among software versions.
2. Clients can inspect or change client-side state; the server must enforce access.
3. Deployed capability that is not broadly exposed.
4. Old branches and combinations add complexity and defects.
5. No.

</details>

## Navigation

- [Back to Deployment Strategies and Recovery](../README.md)
- [Previous: Canary and Progressive Delivery](../03-canary-and-progressive-delivery/)
- [Next: Health Checks, Zero Downtime, and Traffic Management](../05-health-checks-zero-downtime-and-traffic-management/)
- [Back to All Learning Materials](../../README.md)
