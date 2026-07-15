# Pipeline as Code and Platforms

## Overview

Pipeline as Code stores automation definitions with the source they validate. This topic introduces YAML, platform expressions and data, reusable configuration, execution environments, and the different models used by GitHub Actions, Jenkins, and GitLab CI/CD.

## Why It Matters

Versioned pipeline definitions can be reviewed, tested, traced, and changed with the application. Understanding platform syntax and execution boundaries prevents subtle mistakes involving variable scope, untrusted input, runner state, and reuse. Platform comparison also separates portable pipeline ideas from vendor-specific features.

## Main Concepts

- YAML structures used for pipeline configuration
- Variables, contexts, expressions, and parameters
- Reusable workflows and templates
- Hosted and self-hosted execution environments
- Platform-specific workflow models

## Learning Objectives

After completing this section, the learner should be able to:

- Read the structure of a basic pipeline configuration.
- Explain how values flow into reusable pipeline components.
- Compare runners and the core models of major CI/CD platforms.

## Planned Subtopics

- [ ] YAML fundamentals
- [ ] Variables, contexts, expressions, and parameters
- [ ] Reusable workflows and templates
- [ ] Runners and execution environments
- [ ] GitHub Actions
- [ ] Jenkins
- [ ] GitLab CI/CD overview

## Related Practical Projects

[Project 1](../../Projects/1_project/taskops-cicd/.github/workflows/) and [Project 2](../../Projects/2_project/kubeops-gitops/.github/workflows/) contain GitHub Actions YAML to inspect. Jenkins and GitLab CI/CD remain comparison topics; their configuration is not currently represented in these projects.

## Navigation

- [Back to Learning Materials](../README.md)
- [Previous: Pipeline Architecture](../03-pipeline-architecture/)
- [Next: Builds, Dependencies, and Caching](../05-builds-dependencies-and-caching/)
