# Deployment Strategies and Recovery

## Overview

Deployment strategies control how verified content replaces a running version and how exposure expands or reverses. They trade speed, capacity, complexity, compatibility, and blast radius. No strategy is universally best.

```text
Verified artifact
      ↓
Deployment strategy
      ↓
Traffic and health control
      ↓
Observation
      ↓
Continue, pause, roll forward, or roll back
```

| Strategy | Main idea | Extra capacity | Rollback speed | Complexity |
|----------|-----------|----------------|----------------|------------|
| Recreate | Stop old, start new | Low | Medium | Low |
| Rolling | Replace gradually | Usually low | Medium | Medium |
| Blue-green | Switch between two environments | High | Fast | Medium |
| Canary | Expose a small audience first | Variable | Fast for early stage | High |

Strategy names do not guarantee safety. Zero downtime also requires redundancy, readiness, connection draining, capacity, mixed-version compatibility, safe data changes, observation, and recovery.

Recreate favors simplicity and accepts an interruption. Rolling limits extra capacity but temporarily mixes versions. Blue-green buys a rapid traffic switch with duplicate environments. Canary limits early exposure but demands trustworthy routing and analysis. Feature flags control behavior rather than instance replacement and can complement any of them.

Recovery design begins before deployment. Teams must retain known artifacts, understand configuration and data compatibility, define abort criteria, and verify backups. Rollback can be unsafe after destructive state changes; roll-forward may then be the faster and safer response. Neither action is complete until health and user outcomes are verified.

Stateful systems constrain every strategy. Old and new versions may share databases, queues, caches, sessions, and external contracts. Expand-and-contract migrations and backward-compatible interfaces preserve mixed-version operation. Capacity and traffic controls cannot compensate for incompatible data.

The strategy choice should reflect failure cost, available capacity, traffic volume, observability, team experience, and recovery objectives. A small internal service and a regulated public system can reasonably choose different approaches from the same menu.

## Lessons

| # | Lesson | Focus |
|---|--------|-------|
| 01 | [Recreate and Rolling Deployments](./01-recreate-and-rolling-deployments/) | Stop/start versus incremental replacement |
| 02 | [Blue-Green Deployment](./02-blue-green-deployment/) | Validate parallel capacity, then switch traffic |
| 03 | [Canary and Progressive Delivery](./03-canary-and-progressive-delivery/) | Expand exposure using evidence |
| 04 | [Feature Flags, Dark Launches, and A/B Testing](./04-feature-flags-dark-launches-and-ab-testing/) | Separate code deployment from behavior release |
| 05 | [Health Checks, Zero Downtime, and Traffic Management](./05-health-checks-zero-downtime-and-traffic-management/) | Traffic eligibility and graceful lifecycle |
| 06 | [Rollback, Roll-Forward, and Failure Recovery](./06-rollback-roll-forward-and-failure-recovery/) | Choose and audit recovery actions |
| 07 | [Database Migrations and Stateful Changes](./07-database-migrations-and-stateful-changes/) | Preserve compatibility and data |

## Learning Objectives

You will compare deployment strategies, plan traffic and observation, distinguish feature release from version rollout, design health checks, choose rollback or roll-forward, and apply expand-and-contract to stateful changes.

## Recommended Study Order

Study replacement models first, then exposure controls, health/traffic, recovery, and finally stateful compatibility.

## Real Project Connections

[TaskOps deployment](../../Projects/1_project/taskops-cicd/scripts/deploy.sh) uses Compose replacement with one application container and has a rollback script. [KubeOps deployment](../../Projects/2_project/kubeops-gitops/k8s/deployment.yaml) has multiple replicas and probes but no explicit strategy, so Kubernetes defaults—not a repository-declared rolling policy—apply. Blue-green, canary, traffic splitting, and feature flags are absent.

## Completion Checklist

- [ ] I can compare recreate, rolling, blue-green, and canary.
- [ ] I can explain mixed-version compatibility.
- [ ] I can separate feature flags from traffic routing.
- [ ] I can map liveness, readiness, and startup checks.
- [ ] I can choose rollback or roll-forward.
- [ ] I can design expand-and-contract migration steps.

## Navigation

- [Back to Learning Materials](../README.md)
- [Previous: Continuous Delivery and Releases](../09-continuous-delivery-and-releases/)
- [Next: Docker in CI/CD](../11-docker-in-cicd/)
