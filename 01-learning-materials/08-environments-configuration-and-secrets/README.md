# Environments, Configuration, and Secrets

## Overview

Applications move through environments that differ in purpose, access, scale, and risk. This topic covers persistent and temporary environments, external configuration, environment variables, secrets, short-lived credentials, protection rules, and techniques for detecting configuration drift.

## Why It Matters

Embedding environment details or credentials in deployable code makes promotion unsafe and leaks sensitive information. Clear boundaries allow the same artifact to run with approved settings in each target. Protected environments and temporary identity also limit who or what can affect production.

## Main Concepts

- Development, test, staging, production, and preview targets
- Externalized settings and environment variables
- Secret storage and short-lived authentication
- Environment controls, validation, and drift

## Learning Objectives

After completing this section, the learner should be able to:

- Separate deployable artifacts from environment-specific configuration.
- Compare stored secrets with OIDC-based short-lived credentials.
- Describe controls for protected targets and configuration validation.

## Planned Subtopics

- [ ] Development, test, staging, and production
- [ ] Preview and ephemeral environments
- [ ] Environment variables
- [ ] Externalized configuration
- [ ] Secret management
- [ ] OIDC and short-lived credentials
- [ ] Protected environments
- [ ] Configuration drift and validation

## Related Practical Projects

Environment examples and deployment files in [Project 1](../../Projects/1_project/taskops-cicd/) show application configuration boundaries. [Project 2](../../Projects/2_project/kubeops-gitops/) includes Kubernetes ConfigMaps, an example Secret, and environment-specific Helm values. Example files must never be treated as real credentials.

## Navigation

- [Back to Learning Materials](../README.md)
- [Previous: Artifacts, Packages, and Registries](../07-artifacts-packages-and-registries/)
- [Next: Continuous Delivery and Releases](../09-continuous-delivery-and-releases/)
