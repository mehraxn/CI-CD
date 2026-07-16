# Canary and Progressive Delivery

## Controlled Exposure

```text
Version 1: 95% traffic
Version 2: 5% traffic
          ↓
Observe
          ↓
Version 1: 75%
Version 2: 25%
          ↓
Observe
          ↓
Version 2: 100%
```

```text
Canary deployment:
A deployment strategy exposing a new version to a limited audience.

Progressive delivery:
A broader practice that gradually controls exposure using traffic, analysis, approvals, or feature controls.
```

Exposure may use percentages, internal users, cohorts, tenants, regions, rings, or waves. Each step pauses for automated or manual analysis against a stable baseline. Useful signals include error rate, latency, saturation, resource use, conversion, support incidents, and user feedback. Poor or incomplete metrics can approve harm.

Traffic splitting needs weighted routing from a load balancer, ingress controller, or service mesh. Sticky users may be required for consistent sessions or experiments. Low traffic and statistical noise require longer windows or different gates. Every plan needs maximum duration, promotion criteria, and abort/rollback conditions.

Argo Rollouts and Flagger are conceptual controllers that automate steps and analysis; neither exists here. Progressive delivery is broader than canary because it also includes approvals and feature exposure.

Rings expose internal staff, trusted tenants, or low-risk regions before broader populations. Waves roll through target groups rather than percentages. The grouping must match likely failure boundaries: a region can reveal network issues while a random percentage may not. Sticky assignment prevents one user alternating between incompatible versions.

Automated analysis applies explicit queries, thresholds, and windows; manual analysis records a human interpretation of the same evidence. Error rate and latency should be compared with stable baseline traffic under similar load. Saturation signals capacity problems, while business metrics catch technically healthy but harmful behavior. Support incidents and user feedback may justify a pause even before statistical thresholds fail.

An abort should stop further promotion, route traffic safely, preserve diagnostics, and announce ownership. Low traffic may require a minimum request count rather than a fixed short window. Every rollout needs a maximum duration so a forgotten 5% canary does not become a permanent mixed-version state.

## Existing Repository Evidence

The repository has no canary resources, weighted routes, service mesh, rollout controller, ring/wave definitions, or automated comparative analysis. [KubeOps ingress](../../../Projects/2_project/kubeops-gitops/k8s/ingress.yaml) routes to one Service only. Existing monitoring examples do not implement canary decisions.

## Common Mistakes

- Choosing a percentage without analysis.
- Trusting low traffic or incomparable cohorts.
- Lacking rollback automation or maximum duration.
- Using incompatible data across versions.
- Promoting based only on CPU.
- Manual observation without criteria.
- Breaking required user consistency.

## Practical Exercise

Design a KubeOps canary: 5%, 25%, 50%, 100%; define observation time, baseline, error/latency/resource/business measures, minimum traffic, sticky routing need, promotion owner, and abort thresholds. Do not implement it.

## Knowledge Check

1. How is progressive delivery broader than canary?
2. Why compare with a baseline?
3. What problem does low traffic cause?
4. What must every step define?
5. Is routing support present here?

<details><summary>View answers</summary>

1. It controls exposure through traffic, analysis, approvals, and feature controls.
2. Absolute metrics may reflect unrelated system conditions.
3. Too little evidence and high statistical noise.
4. Exposure, window, metrics, promotion, pause, and abort criteria.
5. No weighted or cohort routing is defined.

</details>

## Navigation

- [Back to Deployment Strategies and Recovery](../README.md)
- [Previous: Blue-Green Deployment](../02-blue-green-deployment/)
- [Next: Feature Flags, Dark Launches, and A/B Testing](../04-feature-flags-dark-launches-and-ab-testing/)
- [Back to All Learning Materials](../../README.md)
