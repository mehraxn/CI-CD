# Artifacts, Packages, and Registries

## Overview

Artifacts are durable outputs of pipeline work, while caches are disposable accelerators. This topic covers application packages, container and package registries, naming, versioning, immutability, promotion, retention, and cleanup across an artifact lifecycle.

## Why It Matters

Reliable delivery depends on knowing exactly what was built, tested, and deployed. Rebuilding for each environment introduces variation. Immutable, identifiable outputs allow the same verified unit to move forward, while deliberate retention prevents storage from growing without control or removing evidence too early.

## Main Concepts

- Durable artifacts versus performance caches
- Package and container distribution services
- Identity, versions, immutability, and provenance
- Promotion, retention, and cleanup policies

## Learning Objectives

After completing this section, the learner should be able to:

- Distinguish an artifact from a cache and choose the correct mechanism.
- Define traceable naming and versioning for build outputs.
- Explain how immutable artifacts are promoted and eventually cleaned up.

## Planned Subtopics

- [ ] Artifacts versus caches
- [ ] Application packages
- [ ] Package registries
- [ ] Container registries
- [ ] Artifact naming and versioning
- [ ] Immutable artifacts
- [ ] Artifact promotion
- [ ] Retention and cleanup

## Related Practical Projects

The image-release workflow and Dockerfile in [Project 2](../../Projects/2_project/kubeops-gitops/) provide a container-oriented artifact path to inspect. Project 1 also contains container build and delivery configuration. Registry retention and promotion policies are learning targets unless directly evidenced by project configuration.

## Navigation

- [Back to Learning Materials](../README.md)
- [Previous: Automated Testing and Quality](../06-automated-testing-and-quality/)
- [Next: Environments, Configuration, and Secrets](../08-environments-configuration-and-secrets/)
