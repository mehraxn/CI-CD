# Deployment Strategies and Recovery

## Overview

Deployment strategies control how a new version replaces or runs beside an old one. This topic compares recreate, rolling, blue-green, canary, feature-flag, and progressive approaches, along with health checks, zero-downtime goals, rollback, roll-forward, and database migration concerns.

## Why It Matters

Every deployment changes a running system under uncertainty. Strategy affects capacity, user exposure, observability requirements, infrastructure cost, and recovery speed. A recovery plan must account for data compatibility and external effects, not only switching application binaries.

## Main Concepts

- Replacement, parallel-environment, and gradual rollout models
- Runtime feature controls and progressive exposure
- Health evidence and availability during change
- Application and database recovery choices

## Learning Objectives

After completing this section, the learner should be able to:

- Compare rollout strategies using risk, cost, and recovery criteria.
- Define health evidence needed before expanding a deployment.
- Choose between rollback and roll-forward while considering database state.

## Planned Subtopics

- [ ] Recreate deployment
- [ ] Rolling deployment
- [ ] Blue-green deployment
- [ ] Canary deployment
- [ ] Feature flags
- [ ] Progressive delivery
- [ ] Health checks
- [ ] Zero-downtime deployment
- [ ] Rollback and roll-forward
- [ ] Database migrations

## Related Practical Projects

[Project 1](../../Projects/1_project/taskops-cicd/) includes deployment, rollback, smoke-test, and database-related files that can support a recovery analysis. [Project 2](../../Projects/2_project/kubeops-gitops/k8s/) contains Kubernetes deployment and health configuration relevant to rolling updates. Other strategies remain planned study unless implemented explicitly.

## Navigation

- [Back to Learning Materials](../README.md)
- [Previous: Continuous Delivery and Releases](../09-continuous-delivery-and-releases/)
- [Next: Docker in CI/CD](../11-docker-in-cicd/)
