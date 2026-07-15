# DevSecOps and Supply-Chain Security

## Overview

DevSecOps integrates security feedback and controls throughout delivery rather than isolating them at the end. This topic covers code, dependency, secret, application, container, and infrastructure scanning, plus SBOMs, signing, provenance, runner security, and pipeline permissions.

## Why It Matters

A pipeline handles trusted credentials and produces software users may rely on, making it both a control point and a target. Layered checks can detect different risks, while least privilege and verifiable outputs reduce the impact of compromise. Findings still require triage; a scanner result alone is not a security decision.

## Main Concepts

- Shift-left checks across code, dependencies, applications, and infrastructure
- Component inventories, signatures, provenance, and attestations
- Trusted build environments and isolated runners
- Minimal permissions and controlled secret access

## Learning Objectives

After completing this section, the learner should be able to:

- Match security checks to suitable pipeline phases.
- Explain how SBOMs, signing, and provenance answer different questions.
- Identify permission and runner risks in a pipeline design.

## Planned Subtopics

- [ ] Secure CI/CD principles
- [ ] SAST
- [ ] Dependency and license scanning
- [ ] Secret scanning
- [ ] DAST and API security testing
- [ ] Container scanning
- [ ] Infrastructure as Code scanning
- [ ] SBOMs
- [ ] Artifact signing
- [ ] Provenance and attestations
- [ ] Runner security
- [ ] Pipeline permission security

## Related Practical Projects

Use the workflows, dependency manifests, Dockerfiles, and security notes in [Project 1](../../Projects/1_project/taskops-cicd/) and [Project 2](../../Projects/2_project/kubeops-gitops/) to identify existing controls and gaps. Project 3 adds Terraform and Ansible inputs suitable for later IaC-security exercises.

## Navigation

- [Back to Learning Materials](../README.md)
- [Previous: Infrastructure as Code and Automation](../13-infrastructure-as-code-and-automation/)
- [Next: Observability, Metrics, and Optimization](../15-observability-metrics-and-optimization/)
