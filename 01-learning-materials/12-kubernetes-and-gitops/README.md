# Kubernetes and GitOps

## Overview

Kubernetes runs containerized workloads from declarative resource definitions. GitOps adds a model in which version-controlled desired state is reconciled into a cluster. This topic introduces pipeline deployments, manifests, configuration, Helm, Kustomize, Argo CD, and delivery across environments or clusters.

## Why It Matters

Cluster delivery involves more than running a deployment command. Teams must manage desired state, configuration differences, access boundaries, rollout health, and drift. GitOps can separate artifact creation from cluster reconciliation and provide a reviewable history of operational changes.

## Main Concepts

- Declarative Kubernetes resources and pipeline delivery
- ConfigMaps, Secrets, Helm, and Kustomize
- GitOps desired state and reconciliation
- Environment and cluster promotion patterns

## Learning Objectives

After completing this section, the learner should be able to:

- Describe how an image reference becomes a Kubernetes rollout.
- Compare direct pipeline deployment with GitOps reconciliation.
- Identify configuration boundaries across environments and clusters.

## Planned Subtopics

- [ ] Deploying to Kubernetes from CI/CD
- [ ] Kubernetes manifests
- [ ] ConfigMaps and Secrets
- [ ] Helm
- [ ] Kustomize overview
- [ ] GitOps principles
- [ ] Argo CD
- [ ] Multi-environment delivery
- [ ] Multi-cluster delivery

## Related Practical Projects

[Project 2: KubeOps GitOps](../../Projects/2_project/kubeops-gitops/) contains Kubernetes manifests, a Helm chart, deployment scripts, and an Argo CD application definition. It is the primary practical reference. Kustomize and multi-cluster delivery are planned concepts and should not be inferred from absent files.

## Navigation

- [Back to Learning Materials](../README.md)
- [Previous: Docker in CI/CD](../11-docker-in-cicd/)
- [Next: Infrastructure as Code and Automation](../13-infrastructure-as-code-and-automation/)
