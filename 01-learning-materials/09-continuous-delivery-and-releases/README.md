# Continuous Delivery and Releases

## Overview

Continuous delivery keeps verified changes ready for release while preserving an explicit production decision. This topic examines release pipeline design, build-once promotion, release candidates, approvals, release windows, semantic versions, changelogs, and release notes.

## Why It Matters

A release is a product and operational decision, not merely a successful build. A controlled release flow connects source, test evidence, an immutable artifact, authorization, and user-facing change information. This traceability supports safer decisions and faster diagnosis when something goes wrong.

## Main Concepts

- Delivery and deployment as separate decisions
- Release candidates and immutable artifact promotion
- Approval controls and operational timing
- Versions, changelogs, and release communication

## Learning Objectives

After completing this section, the learner should be able to:

- Distinguish delivery readiness from automatic deployment.
- Outline a build-once, deploy-many release pipeline.
- Connect a release version to approvals, artifacts, and change notes.

## Planned Subtopics

- [ ] Delivery versus deployment
- [ ] Release pipeline design
- [ ] Build once, deploy many
- [ ] Release candidates
- [ ] Artifact promotion
- [ ] Approvals and release windows
- [ ] Semantic versioning
- [ ] Changelogs and release notes

## Related Practical Projects

The CI and CD definitions plus deployment documentation in [Project 1](../../Projects/1_project/taskops-cicd/) offer a release flow to analyze. The image-release workflow in [Project 2](../../Projects/2_project/kubeops-gitops/) supports comparison with a container release. Verify each control in the files before describing it as implemented.

## Navigation

- [Back to Learning Materials](../README.md)
- [Previous: Environments, Configuration, and Secrets](../08-environments-configuration-and-secrets/)
- [Next: Deployment Strategies and Recovery](../10-deployment-strategies-and-recovery/)
