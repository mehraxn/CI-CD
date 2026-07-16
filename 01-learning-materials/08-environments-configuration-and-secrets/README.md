# Environments, Configuration, and Secrets

## Overview

Software runs in more than one place: a developer's machine, test runners, staging, production. CI/CD uses multiple **environments** so changes can be exercised under increasing realism and decreasing tolerance for failure before real users meet them. What makes one verified artifact behave correctly in each place is **configuration** — and the most dangerous slice of configuration is **secrets**, which need stronger controls than everything else.

```text
Application artifact:
The versioned software being delivered.

Configuration:
Non-secret values that change behavior by environment.

Secret:
Sensitive data whose disclosure could cause harm.

Environment:
A controlled deployment context with its own configuration, access, and policies.
```

## One Artifact, Many Environments

```text
One versioned application artifact
               ↓
      Environment-specific configuration
               ↓
     Development / Test / Staging / Production
```

The build-once-deploy-many principle from Topic 07 has a configuration corollary: **do not rebuild application code per environment when the same artifact can be configured externally.** If staging and production run different builds, staging validated nothing. The artifact stays constant; the environment supplies its settings at deployment or runtime.

Principles this section keeps returning to:

- Configuration must be separated from application code — code is versioned and promoted; settings vary by environment.
- Secrets require stronger controls than ordinary configuration: encrypted storage, scoped access, rotation, and audit.
- **Secrets should not be committed to Git** — ever, in any repository visibility.
- **Environment parity** means meaningful similarity, not identical cost — not every environment needs production's capacity.
- **Environment names alone do not create security boundaries** — calling a namespace "production" protects nothing; access rules do.

## Lessons

| Number | Lesson | Main focus |
|---|---|---|
| 01 | [Environment Strategy and Parity](./01-environment-strategy-and-parity/) | Why environments exist and how similar they must be |
| 02 | [Preview and Ephemeral Environments](./02-preview-and-ephemeral-environments/) | Temporary per-change environments and their lifecycle |
| 03 | [Externalized Configuration and Variables](./03-externalized-configuration-and-variables/) | Config outside the artifact: files, variables, ConfigMaps, values |
| 04 | [Secrets Management and Injection](./04-secrets-management-and-injection/) | Storing, injecting, and protecting sensitive values |
| 05 | [OIDC, Workload Identity, and Short-Lived Credentials](./05-oidc-workload-identity-and-short-lived-credentials/) | Replacing stored cloud keys with federated identity |
| 06 | [Protected Environments, Approvals, and Release Controls](./06-protected-environments-approvals-and-release-controls/) | Gating who and what may deploy where |
| 07 | [Configuration Validation, Drift, and Cleanup](./07-configuration-validation-drift-and-cleanup/) | Keeping declared and actual state aligned |

## Learning Objectives

After completing this section, the learner should be able to:

- explain the purpose and parity requirements of each environment tier;
- design the lifecycle of a preview environment;
- externalize configuration and document its precedence;
- distinguish secrets from configuration and inject secrets safely;
- explain OIDC-based workload identity and its trust policies;
- design protected-environment rules for production; and
- detect and respond to configuration drift.

## Recommended Study Order

Follow the numbered order: environments first (where software runs), then configuration (what varies), secrets (what must be protected), identity (how pipelines authenticate), controls (who may deploy), and finally validation and drift (keeping it all true over time).

## Practical Project Connections

The repository is unusually rich here:

- [KubeOps](../../Projects/2_project/kubeops-gitops/) — a real [ConfigMap](../../Projects/2_project/kubeops-gitops/k8s/configmap.yaml), a placeholder [Secret example](../../Projects/2_project/kubeops-gitops/k8s/secret.example.yaml) with the copy-and-gitignore pattern, environment-specific [Helm values](../../Projects/2_project/kubeops-gitops/helm/kubeops/) (`values-dev.yaml` vs `values-prod.yaml`), and an [Argo CD Application](../../Projects/2_project/kubeops-gitops/argocd/application.yaml) that reports drift.
- [TaskOps](../../Projects/1_project/taskops-cicd/) — a documented [.env.example](../../Projects/1_project/taskops-cicd/.env.example), a [production Compose file](../../Projects/1_project/taskops-cicd/docker-compose.prod.yml) with defaults and required-variable validation, and secret injection via GitHub Actions secrets in [cd.yml](../../Projects/1_project/taskops-cicd/.github/workflows/cd.yml).
- [Project 3](../../Projects/3_project/) — [Terraform variables with validation blocks](../../Projects/3_project/terraform/variables.tf) and an [Ansible inventory example](../../Projects/3_project/ansible/inventory.example.ini) that keeps keys out of Git.
- Not demonstrated: GitHub deployment environments (`environment:`), OIDC (`id-token: write`), preview environments, and secret managers — those lessons are conceptual.

## Completion Checklist

- [ ] I mapped the environments each project explicitly defines versus implies.
- [ ] I can trace one configuration value from its source to its consumer.
- [ ] I built a configuration inventory and a secret-reference inventory.
- [ ] I can explain why masking, encoding, and privacy are not encryption.
- [ ] I designed an OIDC trust policy and production-environment rules on paper.
- [ ] I can name the real drift-detection mechanism in this repository.
- [ ] I completed all exercises and knowledge checks.

## Navigation

- [Back to Learning Materials](../README.md)
- [Previous: Artifacts, Packages, and Registries](../07-artifacts-packages-and-registries/)
- [Next: Continuous Delivery and Releases](../09-continuous-delivery-and-releases/)
