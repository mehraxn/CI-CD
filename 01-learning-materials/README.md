# CI/CD Learning Materials

This directory provides a scalable foundation for learning continuous integration, delivery, deployment, and the engineering practices around them. It organizes the subject into fifteen topics without treating the planned lessons as finished content.

The expected outcome is the ability to explain a CI/CD system, read and reason about pipeline configuration, connect build and deployment decisions, and apply those ideas deliberately in the repository projects.

## Recommended Study Order

Study the topics in numbered order. Early sections establish terminology and pipeline structure; later sections apply that foundation to containers, orchestration, infrastructure, security, and operations. Use the [45-day roadmap](./45-day-roadmap.md) for pacing and the [glossary](./glossary.md) for quick reference.

| Number | Topic | Main objective | Status |
|--------|-------|----------------|--------|
| 01 | [CI/CD Fundamentals](./01-cicd-fundamentals/) | Distinguish integration, delivery, deployment, pipelines, and feedback loops | Complete |
| 02 | [Git and Collaboration](./02-git-and-collaboration/) | Use version-control practices that support safe automation | Complete |
| 03 | [Pipeline Architecture](./03-pipeline-architecture/) | Understand triggers, execution units, dependencies, and failure handling | Complete |
| 04 | [Pipeline as Code and Platforms](./04-pipeline-as-code-and-platforms/) | Describe pipeline configuration, reuse, runners, and major platforms | Complete |
| 05 | [Builds, Dependencies, and Caching](./05-builds-dependencies-and-caching/) | Produce efficient and repeatable builds | Complete |
| 06 | [Automated Testing and Quality](./06-automated-testing-and-quality/) | Place appropriate automated checks in a pipeline | Complete |
| 07 | [Artifacts, Packages, and Registries](./07-artifacts-packages-and-registries/) | Store, identify, promote, and retain build outputs | Complete |
| 08 | [Environments, Configuration, and Secrets](./08-environments-configuration-and-secrets/) | Separate deployable code from environment-specific settings and credentials | Complete |
| 09 | [Continuous Delivery and Releases](./09-continuous-delivery-and-releases/) | Design controlled, traceable release flows | Complete |
| 10 | [Deployment Strategies and Recovery](./10-deployment-strategies-and-recovery/) | Compare rollout strategies and plan safe recovery | Complete |
| 11 | [Docker in CI/CD](./11-docker-in-cicd/) | Build, test, scan, publish, and deploy container images | Complete |
| 12 | [Kubernetes and GitOps](./12-kubernetes-and-gitops/) | Deliver Kubernetes changes through declarative and GitOps workflows | Complete |
| 13 | [Infrastructure as Code and Automation](./13-infrastructure-as-code-and-automation/) | Validate and apply repeatable infrastructure changes | Not started |
| 14 | [DevSecOps and Supply-Chain Security](./14-devsecops-and-supply-chain-security/) | Integrate security controls throughout software delivery | Complete |
| 15 | [Observability, Metrics, and Optimization](./15-observability-metrics-and-optimization/) | Measure pipeline and deployment health and improve the system | Complete |

## Theory and Practical Projects

The materials explain the decisions behind CI/CD practices. The existing [projects](../Projects/) provide concrete workflows, applications, tests, containers, Kubernetes resources, GitOps configuration, Terraform, Ansible, and monitoring assets to inspect. A topic README identifies relevant projects but does not claim that every project implements every planned concept. Keep learning notes here and implementation-specific documentation beside its project.

## Progress Checklist

- [x] 01 — CI/CD Fundamentals
- [x] 02 — Git and Collaboration
- [x] 03 — Pipeline Architecture
- [x] 04 — Pipeline as Code and Platforms
- [x] 05 — Builds, Dependencies, and Caching
- [x] 06 — Automated Testing and Quality
- [x] 07 — Artifacts, Packages, and Registries
- [x] 08 — Environments, Configuration, and Secrets
- [x] 09 — Continuous Delivery and Releases
- [x] 10 — Deployment Strategies and Recovery
- [x] 11 — Docker in CI/CD
- [x] 12 — Kubernetes and GitOps
- [ ] 13 — Infrastructure as Code and Automation
- [x] 14 — DevSecOps and Supply-Chain Security
- [x] 15 — Observability, Metrics, and Optimization

## Authoring Resources

Use the [main-topic template](./templates/main-topic-readme-template.md) and [subtopic template](./templates/subtopic-readme-template.md) when expanding this foundation.
