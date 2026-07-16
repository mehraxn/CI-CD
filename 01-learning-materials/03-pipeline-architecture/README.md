# Pipeline Architecture

## Overview

Pipeline architecture describes how automation starts, how work is divided, which work can run together, what must wait, and how results control later actions. The [Pipeline Anatomy lesson](../01-cicd-fundamentals/05-pipeline-anatomy/) introduced the main vocabulary. This section focuses on execution behavior and design decisions.

A simple pipeline can be one job containing a list of commands. A production-quality pipeline normally adds carefully limited triggers, isolated jobs, explicit dependencies, reliable gates, protected deployments, time limits, concurrency rules, cleanup, and useful failure evidence. More features do not automatically mean better architecture: each control should address a real risk or flow problem.

## Why Design Matters

Pipeline structure affects feedback time, cost, security, and recovery. An unnecessarily sequential pipeline wastes runner time. Excessive parallelism can overload shared services. Hidden dependencies make failures confusing. Broad deployment triggers can expose production to branch changes. Missing timeouts can leave work hanging, while careless cancellation can interrupt a deployment halfway through.

Good architecture makes the safe path visible. A learner should be able to trace why a job ran, what it needed, which evidence it produced, and what happens after failure or cancellation.

## Sequential and Parallel Views

```text
Source change
     |
     v
Build
     |
     v
Static checks
     |
     v
Unit tests
     |
     v
Package
     |
     v
Deploy to staging
     |
     v
Smoke tests
     |
     v
Production approval
     |
     v
Deploy to production
```

The flow is easy to read but may wait unnecessarily. Independent verification can run in parallel:

```text
                    +-- Lint ----------+
Source change ------+-- Unit tests ----+-- Package -- Deploy
                    +-- Security scan -+
```

Parallel jobs can reduce duration when they do not depend on one another. Packaging still waits for every required verification result. Runner capacity, external resources, and cost constrain useful parallelism.

## Lessons

| Number | Lesson | Main focus |
|---|---|---|
| 01 | [Triggers and Events](./01-triggers-and-events/) | Decide which events create runs safely and efficiently |
| 02 | [Stages, Jobs, Steps, and Tasks](./02-stages-jobs-steps-and-tasks/) | Divide work into understandable execution units |
| 03 | [Job Dependencies and DAG Pipelines](./03-job-dependencies-and-dag-pipelines/) | Express ordering, parallel branches, and the critical path |
| 04 | [Conditions and Filters](./04-conditions-and-filters/) | Control execution using context, status, and outputs |
| 05 | [Matrix Builds and Parallelism](./05-matrix-builds-and-parallelism/) | Repeat and divide work without unsafe contention |
| 06 | [Manual Approvals and Quality Gates](./06-manual-approvals-and-quality-gates/) | Separate automated evidence from human authorization |
| 07 | [Retries, Timeouts, Cancellation, and Failures](./07-retries-timeouts-cancellation-and-failures/) | Bound work and respond to different failure classes |

## Learning Objectives

After completing this section, the learner should be able to:

- distinguish events, trigger rules, and pipeline runs;
- map stages, jobs, steps, runners, and shared data;
- draw a valid dependency graph and identify its critical path;
- distinguish trigger filters from runtime conditions;
- calculate a matrix expansion and assess parallelism risks;
- separate automated gates from manual approvals; and
- choose appropriate timeout, retry, cancellation, and concurrency behavior.

## Recommended Study Order

Follow the numbered order. Triggers establish why a run exists. Execution units explain where work happens. Dependencies and conditions then describe ordering and selection. Matrix work extends parallel execution. Gates establish progression rules, and failure handling completes the operational design.

## Small Example Architecture

A pull request starts lint, unit-test, and security jobs. The independent jobs run together. A packaging job needs all three and uploads a commit-addressed artifact. A merge to `main` starts delivery, but production deployment requires successful staging smoke tests and an authorized environment decision. New pull-request commits cancel outdated validation, while production deployments use a lock and are not cancelled midway.

This is a conceptual design, not a claim about every repository project.

## Platform Terminology

- GitHub Actions uses workflows, jobs, and steps.
- GitLab CI/CD commonly uses pipelines, stages, jobs, and scripts.
- Jenkins commonly uses pipelines, stages, steps, agents, and nodes.
- Azure Pipelines, CircleCI, and other systems use related concepts with different syntax and exact behavior.

## Practical Project Connections

- [TaskOps CI](../../Projects/1_project/taskops-cicd/.github/workflows/ci.yml) shows pull-request and `main` triggers, two jobs, `needs`, cleanup with `if: always()`, and cancellation of superseded CI runs.
- [TaskOps CD](../../Projects/1_project/taskops-cicd/.github/workflows/cd.yml) shows `verify` before `deploy` and serialized deployment runs with cancellation disabled.
- [KubeOps CI](../../Projects/2_project/kubeops-gitops/.github/workflows/ci.yml) shows a single validation job for pushes and pull requests.
- [KubeOps image release](../../Projects/2_project/kubeops-gitops/.github/workflows/image-release.yml) shows a branch filter and manual dispatch.

## Completion Checklist

- [ ] I can map all seven architecture concerns in a real workflow.
- [ ] I can draw sequential and parallel dependency paths.
- [ ] I can explain isolation and explicit data transfer.
- [ ] I can distinguish filters, conditions, gates, and approvals.
- [ ] I can calculate matrix size and identify contention risks.
- [ ] I can classify failures and choose bounded handling.
- [ ] I completed all exercises and knowledge checks.

## Navigation

- [Back to Learning Materials](../README.md)
- [Previous: Git and Collaboration](../02-git-and-collaboration/)
- [Next: Pipeline as Code and Platforms](../04-pipeline-as-code-and-platforms/)
