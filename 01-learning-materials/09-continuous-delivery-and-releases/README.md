# Continuous Delivery and Releases

## Overview

Continuous delivery keeps every qualifying change in a releasable state. Release management connects a verified source revision, immutable artifact, deployment decision, user-facing change, and operational evidence. A deployment installs software; a release makes a version or feature available. They often coincide, but a feature flag can deploy disabled code and release it later.

```text
Verified source change
        ↓
Immutable artifact
        ↓
Automated test environment
        ↓
Staging validation
        ↓
Release decision
        ↓
Production deployment
        ↓
Post-release verification
```

```text
Deployment:
Installing or activating a software version in an environment.

Release:
Making functionality available to users or declaring a version officially available.

Continuous delivery:
Keeping software in a releasable state, with production deployment available on demand.

Continuous deployment:
Automatically deploying qualifying changes to production without a required manual release step.
```

Build creates an output; verification establishes confidence; artifact storage preserves exact content; deployment puts it into an environment; release decides who may use it. Traceability is lost if any link cannot identify the exact source and artifact.

Continuous delivery is a capability, not a workflow name. It requires repeatable builds, meaningful automated checks, controlled configuration, a preserved artifact, and a deployment path that can be exercised when needed. Continuous deployment uses that capability to send qualifying changes to production automatically. Either approach still needs monitoring and recovery.

Release management adds the human-facing context automation cannot infer: compatibility promises, business timing, known issues, ownership, and communication. Strong automation makes those decisions smaller and better informed. It should not turn a movable branch or `latest` tag into an assumed release identity.

The safest flow normally promotes the same output. If staging validates one build and production receives a rebuild, the evidence no longer proves production content. An exact digest or checksum, source revision, build run, configuration revision, and verification record establish the chain.

## Lessons

| # | Lesson | Focus |
|---|--------|-------|
| 01 | [Delivery, Deployment, and Release](./01-delivery-deployment-and-release/) | Separate integration, delivery, deployment, and feature availability |
| 02 | [Release Pipeline Design and Release Candidates](./02-release-pipeline-design-and-release-candidates/) | Candidate identity, evidence, gates, and progression |
| 03 | [Build Once, Deploy Many, and Artifact Promotion](./03-build-once-deploy-many-and-artifact-promotion/) | Promote one verified output without rebuilding |
| 04 | [Versioning, Tags, Changelogs, and Release Notes](./04-versioning-tags-changelogs-and-release-notes/) | Human and machine release identity |
| 05 | [Approvals, Release Windows, and Change Controls](./05-approvals-release-windows-and-change-controls/) | Risk-based human and automated controls |
| 06 | [Release Readiness and Post-Release Verification](./06-release-readiness-and-post-release-verification/) | Prove readiness and verify real behavior |
| 07 | [Release Automation, Communication, and Audit](./07-release-automation-communication-and-audit/) | Records, notifications, ownership, and evidence |

## Learning Objectives

You will be able to distinguish delivery from deployment, define an exact release candidate, design a release pipeline, promote immutable outputs, use versions and notes responsibly, select useful approvals, verify releases, and retain an auditable record.

## Recommended Study Order

Follow the numbered lessons. Identity and pipeline design come before approvals; readiness comes before automation and communication.

## Real Project Connections

- [TaskOps CD](../../Projects/1_project/taskops-cicd/.github/workflows/cd.yml) verifies, builds, scans, publishes, deploys a commit-SHA image, and smoke-tests production. It deploys automatically on `main`, so it resembles continuous deployment, but repository settings and actual external execution are not visible here.
- [KubeOps image release](../../Projects/2_project/kubeops-gitops/.github/workflows/image-release.yml) publishes images but does not deploy them. [Argo CD](../../Projects/2_project/kubeops-gitops/argocd/application.yaml) uses manual sync, separating publication from deployment.
- No tag-based release, changelog, GitHub Release, staged promotion, or formal release record exists.

## Completion Checklist

- [ ] I can distinguish release from deployment.
- [ ] I can identify a release candidate by source and artifact identity.
- [ ] I can explain build-once-deploy-many.
- [ ] I can draft release notes and a readiness checklist.
- [ ] I can select approvals based on risk.
- [ ] I can design an auditable release record.

## Navigation

- [Back to Learning Materials](../README.md)
- [Previous: Environments, Configuration, and Secrets](../08-environments-configuration-and-secrets/)
- [Next: Deployment Strategies and Recovery](../10-deployment-strategies-and-recovery/)
