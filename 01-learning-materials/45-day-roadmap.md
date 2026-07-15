# 45-Day CI/CD Learning Roadmap

This roadmap builds working literacy and practical habits in about 45 days. It does not imply complete mastery of every platform or advanced practice. Adjust the daily workload to available time, record questions, and prefer a small verified exercise over broad untested configuration.

## Depth Guide

- **Must learn:** Core ideas and skills needed to reason about a basic CI/CD system.
- **Should understand:** Important patterns to recognize and explain, even if implementation practice is limited.
- **Optional advanced study:** Useful extensions to revisit after the 45-day foundation.

## Phase 1 — Days 1–4: CI/CD Fundamentals

**Topics:** [CI/CD Fundamentals](./01-cicd-fundamentals/) and glossary orientation.

**Learning goals:** Must learn the distinctions among continuous integration, delivery, and deployment and identify pipeline inputs, checks, outputs, and feedback. Should understand the relationship between small changes and short feedback loops. Optionally compare organizational adoption models.

**Practical activity:** Read Project 1's CI and CD workflows. Sketch which events start them, what each job verifies, and where delivery or deployment begins. Do not change the workflows.

**Expected output:** A one-page pipeline map and a short explanation of the three continuous practices.

**Related repository project:** [Project 1 — TaskOps CI/CD](../Projects/1_project/taskops-cicd/).

## Phase 2 — Days 5–8: Git and Collaboration

**Topics:** [Git and Collaboration](./02-git-and-collaboration/).

**Learning goals:** Must learn commits, branches, merges, pull requests, and tags. Should understand rebasing, branch protections, semantic versioning, and the tradeoffs of common branching strategies. Optionally study release automation based on conventional commit formats.

**Practical activity:** Use a temporary learning branch to make a focused documentation change, inspect its history, and describe appropriate review and merge rules. Identify branch and tag filters in existing workflows.

**Expected output:** A clean sample commit history and a proposed collaboration checklist.

**Related repository project:** [Projects directory](../Projects/) and the workflow-enabled Project 1 and Project 2 repositories.

## Phase 3 — Days 9–13: Pipeline Architecture

**Topics:** [Pipeline Architecture](./03-pipeline-architecture/).

**Learning goals:** Must learn triggers, jobs, steps, dependencies, conditions, and failure behavior. Should understand DAGs, matrices, parallelism, approvals, timeouts, retries, and cancellation. Optionally model a large monorepo pipeline.

**Practical activity:** Diagram one Project 1 workflow and one Project 2 workflow as dependency graphs. Mark work that is sequential, parallelizable, conditional, or gated, and note how failure propagates.

**Expected output:** Two annotated pipeline diagrams and a short comparison of their architecture.

**Related repository project:** [Project 1 workflows](../Projects/1_project/taskops-cicd/.github/workflows/) and [Project 2 workflows](../Projects/2_project/kubeops-gitops/.github/workflows/).

## Phase 4 — Days 14–18: Pipeline as Code and GitHub Actions

**Topics:** [Pipeline as Code and Platforms](./04-pipeline-as-code-and-platforms/).

**Learning goals:** Must learn basic YAML and the structure of a GitHub Actions workflow. Should understand contexts, expressions, variables, reusable workflows, runner boundaries, and how Jenkins and GitLab CI/CD differ conceptually. Optionally create a reusable workflow in a separate exercise branch.

**Practical activity:** Annotate an existing GitHub Actions file: events, permissions, jobs, runner, actions, commands, inputs, outputs, and expressions. Validate a harmless copied example rather than changing production behavior.

**Expected output:** An annotated workflow and a platform-neutral version of its execution flow.

**Related repository project:** [Project 2 — KubeOps GitOps](../Projects/2_project/kubeops-gitops/).

## Phase 5 — Days 19–22: Builds, Dependencies, Testing, and Quality

**Topics:** [Builds, Dependencies, and Caching](./05-builds-dependencies-and-caching/) and [Automated Testing and Quality](./06-automated-testing-and-quality/).

**Learning goals:** Must learn build inputs, dependency pinning, unit and integration checks, and the difference between artifacts and caches. Should understand reproducibility, static analysis, coverage, quality gates, test parallelism, and flaky-test handling. Performance and contract testing are optional advanced practice.

**Practical activity:** Trace Project 1 from dependency installation through its test commands. Run existing safe tests if the local prerequisites are available, then identify one candidate cache and its invalidation input.

**Expected output:** A build-and-test flow, recorded test result, and proposed cache key with rationale.

**Related repository project:** [Project 1 — TaskOps CI/CD](../Projects/1_project/taskops-cicd/).

## Phase 6 — Days 23–25: Artifacts, Registries, Environments, and Secrets

**Topics:** [Artifacts, Packages, and Registries](./07-artifacts-packages-and-registries/) and [Environments, Configuration, and Secrets](./08-environments-configuration-and-secrets/).

**Learning goals:** Must learn immutable artifact identity, registries, external configuration, and secret handling. Should understand promotion, retention, protected environments, preview environments, OIDC, and drift validation. Optional study includes enterprise secret rotation and cross-account registries.

**Practical activity:** Follow Project 2's image path from Dockerfile to release workflow and deployment reference. Inventory configuration versus secret inputs without displaying secret values.

**Expected output:** An artifact lineage diagram and a configuration/secret boundary table.

**Related repository project:** [Project 2 — KubeOps GitOps](../Projects/2_project/kubeops-gitops/).

## Phase 7 — Days 26–29: Delivery, Releases, and Deployment Strategies

**Topics:** [Continuous Delivery and Releases](./09-continuous-delivery-and-releases/) and [Deployment Strategies and Recovery](./10-deployment-strategies-and-recovery/).

**Learning goals:** Must learn build-once promotion, release traceability, health checks, and rollback versus roll-forward. Should understand semantic releases, approvals, rolling, blue-green, canary, progressive delivery, and database compatibility. Advanced traffic management is optional.

**Practical activity:** Review Project 1's deployment, smoke-test, backup, and rollback files. Write a release decision checklist and walk through a hypothetical failed deployment without executing it.

**Expected output:** A release checklist, recovery decision tree, and noted database risks.

**Related repository project:** [Project 1 — TaskOps CI/CD](../Projects/1_project/taskops-cicd/).

## Phase 8 — Days 30–33: Docker in CI/CD

**Topics:** [Docker in CI/CD](./11-docker-in-cicd/).

**Learning goals:** Must learn build context, layers, tags, image publication, and container-based test execution. Should understand multi-stage builds, Compose in CI, scanning, minimal runtime images, and immutable digests. Advanced multi-architecture builds are optional.

**Practical activity:** Compare the three project Dockerfiles and their ignore files. Build one image locally if tooling is available, inspect its tags and layers, and document where scanning and publication belong.

**Expected output:** A Dockerfile comparison and a verified image-build record or, if tooling is unavailable, an exact build plan.

**Related repository project:** [All practical projects](../Projects/).

## Phase 9 — Days 34–37: Kubernetes and GitOps

**Topics:** [Kubernetes and GitOps](./12-kubernetes-and-gitops/).

**Learning goals:** Must learn core manifests, image references, configuration resources, rollout health, and GitOps reconciliation. Should understand Helm, Argo CD, environment values, drift, and direct-deploy versus pull-based models. Kustomize and multi-cluster delivery are optional at this stage.

**Practical activity:** Trace Project 2 from image release to raw manifests, Helm values, and the Argo CD application. Render or validate configuration locally if the required tools are installed; do not target a shared cluster.

**Expected output:** A desired-state flow diagram and validation notes for one environment.

**Related repository project:** [Project 2 — KubeOps GitOps](../Projects/2_project/kubeops-gitops/).

## Phase 10 — Days 38–40: Infrastructure as Code

**Topics:** [Infrastructure as Code and Automation](./13-infrastructure-as-code-and-automation/).

**Learning goals:** Must learn declarative infrastructure, Terraform configuration and plans, state sensitivity, and Ansible's configuration role. Should understand modules, drift, validation, approval, and policy as code. Remote-state architecture and custom policies are optional.

**Practical activity:** Read Project 3's Terraform and Ansible documentation and map provisioning versus configuration responsibilities. Run formatting or static validation only when tooling and required initialization are safe and available.

**Expected output:** An infrastructure flow, state-safety checklist, and proposed validation pipeline stages.

**Related repository project:** [Project 3](../Projects/3_project/).

## Phase 11 — Days 41–42: DevSecOps

**Topics:** [DevSecOps and Supply-Chain Security](./14-devsecops-and-supply-chain-security/).

**Learning goals:** Must learn least privilege, secret scanning, dependency risk, SAST, and container scanning. Should understand DAST, IaC scanning, SBOMs, signing, provenance, attestations, and runner isolation. Formal supply-chain maturity frameworks are optional advanced study.

**Practical activity:** Build a threat-oriented checklist for one existing workflow. Identify untrusted inputs, credential boundaries, dependencies, produced artifacts, and suitable controls without inventing results from scanners that were not run.

**Expected output:** A pipeline threat checklist and prioritized security-control backlog.

**Related repository project:** [Project 1](../Projects/1_project/taskops-cicd/) plus Project 3's IaC inputs.

## Phase 12 — Days 43–44: Observability and Optimization

**Topics:** [Observability, Metrics, and Optimization](./15-observability-metrics-and-optimization/).

**Learning goals:** Must learn the difference between pipeline and deployment signals and the four DORA metrics. Should understand alert design, duration, queue time, cache effectiveness, incident response, runbooks, postmortems, and cost tradeoffs. Distributed tracing design is optional.

**Practical activity:** Inspect Project 3's Prometheus and Grafana assets. Propose a small dashboard that combines delivery and service signals, then identify one pipeline optimization and how to measure its effect.

**Expected output:** A metric catalog, dashboard sketch, and measurable optimization hypothesis.

**Related repository project:** [Project 3 monitoring](../Projects/3_project/monitoring/) and [documentation](../Projects/3_project/docs/monitoring.md).

## Phase 13 — Day 45: Capstone and Repository Review

**Topics:** Review all fifteen topics and connect them as one delivery system.

**Learning goals:** Must explain the path from commit to observed deployment, including controls and recovery. Should identify gaps and prioritize improvements based on risk and evidence. Implementing advanced optional topics is outside this day's scope.

**Practical activity:** Choose one existing project and produce an end-to-end CI/CD design review. Confirm documentation links, separate current behavior from proposals, and select a small next implementation milestone.

**Expected output:** A capstone architecture diagram, evidence-based gap analysis, updated learning checklist, and concise repository review.

**Related repository project:** Choose [Project 1](../Projects/1_project/taskops-cicd/), [Project 2](../Projects/2_project/kubeops-gitops/), or [Project 3](../Projects/3_project/).

## Navigation

- [Back to Learning Materials](./README.md)
- [Glossary](./glossary.md)
