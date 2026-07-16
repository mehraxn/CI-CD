# DevSecOps and Supply-Chain Security

## Overview

Security used to be a phase — a review before release, performed by a separate team, arriving too late to change anything cheaply. DevSecOps replaces the phase with a property: security feedback and controls integrated at every step of delivery, automated where automation works, and owned by the same people who build and ship.

```text
DevSecOps:
An operating approach that integrates security responsibility and automation throughout software delivery.

Shift-left security:
Move useful security feedback earlier in design, coding, and build stages.

Shift-right security:
Validate security and behavior in deployed or runtime environments.

Software supply chain:
The people, tools, source, dependencies, build systems, artifacts, and services involved in producing software.
```

The supply chain matters because modern software is mostly assembled: your code sits on top of dependencies, built by pipelines, packaged into images, pulled through registries. Every link is an attack surface, and attackers increasingly target the links rather than the final application.

## Security Across the Lifecycle

```text
Design
  ↓
Code and review
  ↓
Build
  ↓
Test and scan
  ↓
Package and sign
  ↓
Deploy
  ↓
Monitor
  ↓
Respond and improve
```

Each stage contributes a different control family: threat modeling at design, review and static analysis at code, dependency and secret controls at build, scanning at test, signing and provenance at packaging, permission and environment controls at deploy, detection at runtime, and incident response feeding back into design. The frame that organizes them all: **prevention** reduces the chance of harm, **detection** notices it, **response** contains it, and **recovery** restores service — a mature setup invests in all four, because prevention alone always eventually fails.

## What DevSecOps Is Not

- One security scanner in CI.
- Security only inside CI — runtime and design matter equally.
- Developers replacing security specialists — the specialists shift from gatekeepers to enablers.
- Blocking every finding — triage and risk context decide what blocks.
- Trusting a green pipeline — the pipeline proves the encoded checks passed, nothing more.
- Removing human threat modeling — automation finds known patterns, not novel design flaws.
- Eliminating incident response — something will always get through.

## Lessons

| Number | Lesson | Main focus |
|---|---|---|
| 01 | [DevSecOps Fundamentals and Security by Design](./01-devsecops-fundamentals-and-security-by-design/) | Threats, risks, controls, and design-time security |
| 02 | [SAST, Code Quality, and Secret Scanning](./02-sast-code-quality-and-secret-scanning/) | Analyzing source and catching committed secrets |
| 03 | [Dependency, License, and Software Composition Analysis](./03-dependency-license-and-software-composition-analysis/) | Third-party component risk |
| 04 | [Container, Kubernetes, and IaC Security Scanning](./04-container-kubernetes-and-iac-security-scanning/) | Scanning images, manifests, and infrastructure code |
| 05 | [SBOM, Signing, Provenance, and Attestations](./05-sbom-signing-provenance-and-attestations/) | Inventories and verifiable build evidence |
| 06 | [Secure Pipelines, Permissions, Actions, and Runners](./06-secure-pipelines-permissions-actions-and-runners/) | The pipeline itself as an attack surface |
| 07 | [DAST, API Security, and Runtime Validation](./07-dast-api-security-and-runtime-validation/) | Testing running applications from the outside |
| 08 | [Vulnerability Management, Exceptions, and Response](./08-vulnerability-management-exceptions-and-response/) | Triaging, fixing, accepting, and closing findings |

## Learning Objectives

After completing this section, the learner should be able to:

- distinguish threats, vulnerabilities, risks, and controls;
- match SAST, SCA, secret scanning, container/IaC scanning, and DAST to what each can and cannot find;
- explain SBOMs, signing, provenance, attestations, and SLSA at working level;
- audit a pipeline's permissions, action references, and runner trust;
- triage findings into remediate, mitigate, accept, or reject decisions; and
- map every concept onto this repository's real security controls.

## Recommended Study Order

Follow the numbered order: principles first, then the scanner families roughly in pipeline order (source → dependencies → images and infrastructure), then the supply-chain evidence layer, the pipeline's own security, runtime testing, and finally what to *do* with everything the tools find.

## Practical Project Connections

The repository has a real, layered security toolchain — all blocking gates:

- **Bandit** (Python source patterns, `bandit -r app`, tests excluded via `pyproject.toml`) in [TaskOps CI](../../Projects/1_project/taskops-cicd/.github/workflows/ci.yml), [TaskOps CD](../../Projects/1_project/taskops-cicd/.github/workflows/cd.yml), and [KubeOps CI](../../Projects/2_project/kubeops-gitops/.github/workflows/ci.yml).
- **pip-audit** (dependency advisories) in the same three workflows.
- **Trivy** (image scanning, HIGH/CRITICAL, `exit-code: "1"`, `ignore-unfixed: true`, pinned to `@0.28.0`) in all four workflows — including a real scan-before-push versus scan-after-push contrast.
- **Least-privilege tokens** (`contents: read`, job-scoped `packages: write`) and **non-root containers** (Dockerfile `USER`, Helm `securityContext`).

Not present — covered conceptually: CodeQL/Semgrep, secret-scanning tools, Dependabot/Renovate, IaC scanners (Checkov/tfsec), SBOMs, signing/provenance (Cosign/SLSA), DAST, and SHA-pinned actions.

## Completion Checklist

- [ ] I built a threat-boundary map for one project.
- [ ] I mapped every real security check to its category, stage, and limitation.
- [ ] I can explain what pip-audit finds that Bandit cannot, and vice versa.
- [ ] I traced the real Trivy gates and their `ignore-unfixed` risk decision.
- [ ] I audited one workflow's permissions, pins, and runner trust.
- [ ] I designed an evidence bundle and wrote a sample vulnerability record.
- [ ] I completed all exercises and knowledge checks.

## Navigation

- [Back to Learning Materials](../README.md)
- [Previous: Infrastructure as Code and Automation](../13-infrastructure-as-code-and-automation/)
- [Next: Observability, Metrics, and Optimization](../15-observability-metrics-and-optimization/)
