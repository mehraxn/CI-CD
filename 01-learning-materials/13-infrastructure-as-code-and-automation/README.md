# Infrastructure as Code and Automation

## Overview

Infrastructure as Code represents infrastructure in version-controlled definitions that tools can validate and apply. This topic covers declarative and imperative approaches, Terraform configuration and state, modules, drift, Ansible automation, pipeline validation, and policy checks.

## Why It Matters

Manual infrastructure changes are difficult to reproduce, review, and audit. Code-based definitions make intended changes visible before execution, but safe automation still requires state protection, controlled credentials, reviewable plans, and policy. Configuration management complements provisioning by defining how systems are prepared.

## Main Concepts

- Declarative desired state and imperative procedures
- Terraform configuration, state, plans, and modules
- Drift detection and Ansible configuration automation
- CI validation and machine-enforced policy

## Learning Objectives

After completing this section, the learner should be able to:

- Compare declarative infrastructure with imperative automation.
- Explain why Terraform state requires protected, coordinated storage.
- Outline validation and approval stages for infrastructure changes.

## Planned Subtopics

- [ ] Infrastructure as Code fundamentals
- [ ] Declarative versus imperative automation
- [ ] Terraform
- [ ] Terraform state
- [ ] Terraform modules
- [ ] Infrastructure drift
- [ ] Ansible
- [ ] IaC validation in CI/CD
- [ ] Policy as Code

## Related Practical Projects

[Project 3](../../Projects/3_project/) contains Terraform definitions for infrastructure and Ansible playbooks and roles for system configuration. Its existing documentation supports inspection of both tool boundaries. A future pipeline can validate this code, but no current workflow behavior is claimed here.

## Navigation

- [Back to Learning Materials](../README.md)
- [Previous: Kubernetes and GitOps](../12-kubernetes-and-gitops/)
- [Next: DevSecOps and Supply-Chain Security](../14-devsecops-and-supply-chain-security/)
