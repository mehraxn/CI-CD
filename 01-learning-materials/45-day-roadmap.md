# 45-Day CI/CD Learning Roadmap

This roadmap builds working literacy and practical habits in about 45 days. It does not imply complete mastery of every platform or advanced practice. Adjust the daily workload to available time, record questions, and prefer a small verified exercise over broad untested configuration.

## Depth Guide

- **Must learn:** Core ideas and skills needed to reason about a basic CI/CD system.
- **Should understand:** Important patterns to recognize and explain, even if implementation practice is limited.
- **Optional advanced study:** Useful extensions to revisit after the 45-day foundation.

## Phase 1 — Days 1–4: CI/CD Fundamentals

**Topics:** [CI/CD Fundamentals](./01-cicd-fundamentals/), including [continuous integration](./01-cicd-fundamentals/01-continuous-integration/), [continuous delivery](./01-cicd-fundamentals/02-continuous-delivery/), [continuous deployment](./01-cicd-fundamentals/03-continuous-deployment/), [their comparison](./01-cicd-fundamentals/04-ci-vs-delivery-vs-deployment/), [pipeline anatomy](./01-cicd-fundamentals/05-pipeline-anatomy/), and [feedback loops](./01-cicd-fundamentals/06-devops-and-feedback-loops/).

**Learning goals:** Must learn the distinctions among continuous integration, delivery, and deployment and identify pipeline inputs, checks, outputs, and feedback. Should understand the relationship between small changes and short feedback loops. Optionally compare organizational adoption models.

**Practical activity:** Read Project 1's CI and CD workflows. Identify each trigger, job, runner, step group, gate, and artifact; sketch where integration ends and delivery or deployment begins. Compare the result with the four feedback loops in the lesson. Do not change the workflows.

**Expected output:** A one-page pipeline map and a short explanation of the three continuous practices.

**Related repository project:** [Project 1 — TaskOps CI/CD](../Projects/1_project/taskops-cicd/).

## Phase 2 — Days 5–8: Git and Collaboration

**Topics:** [Git and Collaboration](./02-git-and-collaboration/), from [Git fundamentals](./02-git-and-collaboration/01-git-fundamentals/) and [commit history](./02-git-and-collaboration/02-commits-and-history/) through [branches](./02-git-and-collaboration/03-branches-merging-and-rebasing/), [pull requests](./02-git-and-collaboration/04-pull-requests-and-code-review/), [strategies](./02-git-and-collaboration/05-branching-strategies/), [release tags](./02-git-and-collaboration/06-tags-versioning-and-releases/), and [branch protections](./02-git-and-collaboration/07-protected-branches-and-merge-rules/).

**Learning goals:** Must learn commits, branches, merges, pull requests, and tags. Should understand rebasing, branch protections, semantic versioning, and the tradeoffs of common branching strategies. Optionally study release automation based on conventional commit formats.

**Practical activity:** In a disposable practice repository, create focused commits, create and merge a short-lived branch, and inspect the history. Draft a pull request, observe which CI event would run, create an annotated local tag without pushing it, and review branch-protection options without changing repository settings.

**Expected output:** A clean sample commit history and a proposed collaboration checklist.

**Related repository project:** [Projects directory](../Projects/) and the workflow-enabled Project 1 and Project 2 repositories.

## Phase 3 — Days 9–13: Pipeline Architecture

**Topics:** [Pipeline Architecture](./03-pipeline-architecture/), covering [triggers and events](./03-pipeline-architecture/01-triggers-and-events/), [stages, jobs, steps, and tasks](./03-pipeline-architecture/02-stages-jobs-steps-and-tasks/), [dependencies and DAG pipelines](./03-pipeline-architecture/03-job-dependencies-and-dag-pipelines/), [conditions and filters](./03-pipeline-architecture/04-conditions-and-filters/), [matrix builds and parallelism](./03-pipeline-architecture/05-matrix-builds-and-parallelism/), [approvals and quality gates](./03-pipeline-architecture/06-manual-approvals-and-quality-gates/), and [failure handling](./03-pipeline-architecture/07-retries-timeouts-cancellation-and-failures/).

**Day 9 — Triggers:** Pipeline triggers, repository events (push, pull request, tag), and manual and scheduled execution. Output: a trigger comparison table for the Project 1 and Project 2 workflows, noting branch filters and any duplicate-run risks.

**Day 10 — Execution units:** Stages, jobs, steps, and runner isolation, including why files and variables do not automatically cross job boundaries. Output: a mapped workflow — a written `Workflow → Job → Step` tree of one existing workflow, without modifying it.

**Day 11 — Dependencies:** Job dependencies, DAG pipelines, parallel jobs, and the critical path. Output: a hand-drawn or Markdown DAG of one Project 1 workflow, with its approximate critical path marked and any parallelizable work identified.

**Day 12 — Selection and expansion:** Conditions, filters, and matrix builds. Output: a small matrix calculation (for example, 3 operating systems × 2 runtime versions = 6 jobs) and a written conditional-deployment example kept in notes, not in a workflow file.

**Day 13 — Gates and failure handling:** Manual approvals, automated quality gates, failures, retries, timeouts, and concurrency. Output: a proposed quality-gate design for one project and a failure-handling table classifying five scenarios (retry, do not retry, investigate first, cancel outdated run, serialize execution).

**Learning goals:** Must learn triggers, jobs, steps, dependencies, conditions, and failure behavior. Should understand DAGs, matrices, parallelism, approvals, timeouts, retries, and cancellation. Optionally model a large monorepo pipeline.

**Expected output:** The five daily outputs above, culminating in two annotated pipeline diagrams and a short comparison of Project 1 and Project 2 architecture.

**Related repository project:** [Project 1 workflows](../Projects/1_project/taskops-cicd/.github/workflows/) and [Project 2 workflows](../Projects/2_project/kubeops-gitops/.github/workflows/).

## Phase 4 — Days 14–18: Pipeline as Code and Platforms

**Topics:** [Pipeline as Code and Platforms](./04-pipeline-as-code-and-platforms/), covering [Pipeline as Code fundamentals](./04-pipeline-as-code-and-platforms/01-pipeline-as-code-fundamentals/), [YAML](./04-pipeline-as-code-and-platforms/02-yaml-fundamentals/), [variables and expressions](./04-pipeline-as-code-and-platforms/03-variables-contexts-expressions-and-outputs/), [reuse](./04-pipeline-as-code-and-platforms/04-reusable-workflows-templates-and-components/), [runners](./04-pipeline-as-code-and-platforms/05-runners-and-execution-environments/), [GitHub Actions](./04-pipeline-as-code-and-platforms/06-github-actions/), [Jenkins](./04-pipeline-as-code-and-platforms/07-jenkins/), and [GitLab CI/CD](./04-pipeline-as-code-and-platforms/08-gitlab-cicd/).

**Day 14 — Pipeline as Code fundamentals:** Versioning, review, and auditing of pipeline configuration. Output: the Git-history inspection of one real workflow, with the revert command you would use written down (not executed).

**Day 15 — YAML:** Mappings, sequences, scalars, block styles, quoting, schema validation, and syntax versus semantics. Output: a YAML correction exercise — fix the broken indentation example from the lesson in notes and label each error.

**Day 16 — Data flow:** Variables, contexts, expressions, inputs, outputs, and a secrets overview. Output: a variable-scope map of TaskOps CD listing name, source, scope, sensitivity, and consumer for each value (names only, never secret values).

**Day 17 — Reuse and runners:** Reusable workflows, templates, composite actions, and execution environments. Outputs: a written reuse proposal for the duplicated TaskOps quality checks, and a hosted-versus-self-hosted runner comparison for one job.

**Day 18 — Platforms:** GitHub Actions in depth, Jenkins overview, GitLab CI/CD overview, and platform comparison. Outputs: one fully annotated real workflow and a platform-selection table applying the selection factors to a team scenario you invent.

**Learning goals:** Must learn basic YAML and the structure of a GitHub Actions workflow. Should understand contexts, expressions, variables, reusable workflows, runner boundaries, and how Jenkins and GitLab CI/CD differ conceptually. Optionally create a reusable workflow in a separate exercise branch.

**Expected output:** The five daily outputs above, centered on an annotated workflow and a platform-neutral version of its execution flow.

**Related repository project:** [Project 1 — TaskOps CI/CD](../Projects/1_project/taskops-cicd/) and [Project 2 — KubeOps GitOps](../Projects/2_project/kubeops-gitops/).

## Phase 5 — Days 19–22: Builds, Dependencies, Testing, and Quality

**Topics:** [Builds, Dependencies, and Caching](./05-builds-dependencies-and-caching/) (six lessons from [build lifecycle](./05-builds-dependencies-and-caching/01-build-lifecycle-and-build-tools/) to [multi-architecture builds](./05-builds-dependencies-and-caching/06-cross-platform-and-multi-architecture-builds/)) and [Automated Testing and Quality](./06-automated-testing-and-quality/) (eight lessons from [testing strategy](./06-automated-testing-and-quality/01-testing-strategy-and-test-pyramid/) to [flaky tests and optimization](./06-automated-testing-and-quality/08-parallel-tests-flaky-tests-and-optimization/)).

**Day 19 — Build fundamentals:** Build lifecycle, build tools, and build inputs and outputs. Output: a build map of Project 1 (inputs, dependency files, build command, test command, output, container build, CI workflow).

**Day 20 — Dependencies and reproducibility:** Dependency management, lockfiles, version pinning, and reproducible builds. Outputs: a classification of every dependency file in the repository (manifest / pinned list / lockfile / constraints), and a version-reference audit of Project 1 separating pinned from floating references.

**Day 21 — Caching, metadata, platforms, and static checks:** Build caching, build metadata, cross-platform builds, testing strategy, and formatting/linting/static analysis. Outputs: an analysis of the two real caches in TaskOps CI (key inputs and invalidation), a test-level classification of all three projects' suites, and a static-check map of every tool in TaskOps CI.

**Day 22 — Test levels and quality:** Unit, integration, API, and end-to-end tests, coverage, quality gates, and flaky tests. Outputs: a quality-gate table for both TaskOps workflows, a proposed coverage-gate design, and the flaky-test diagnosis exercise (five failure scenarios classified with responses).

**Learning goals:** Must learn build inputs, dependency pinning, unit and integration checks, and the difference between artifacts and caches. Should understand reproducibility, static analysis, coverage, quality gates, test parallelism, and flaky-test handling. Performance and contract testing are optional advanced practice.

**Practical activity:** Trace Project 1 from dependency installation through its test commands. Run existing safe tests if the local prerequisites are available, then identify one candidate cache and its invalidation input.

**Expected output:** The daily outputs above, centered on a build-and-test flow, recorded test result, and cache analysis with rationale.

**Related repository project:** [Project 1 — TaskOps CI/CD](../Projects/1_project/taskops-cicd/), with dependency-style contrasts from [Project 2](../Projects/2_project/kubeops-gitops/) and [Project 3](../Projects/3_project/).

## Phase 6 — Days 23–25: Artifacts, Registries, Environments, and Secrets

**Topics:** [Artifacts, Packages, and Registries](./07-artifacts-packages-and-registries/) (seven lessons from [artifacts and caches](./07-artifacts-packages-and-registries/01-artifacts-caches-and-job-outputs/) to [retention and cleanup](./07-artifacts-packages-and-registries/07-retention-cleanup-access-and-replication/)) and [Environments, Configuration, and Secrets](./08-environments-configuration-and-secrets/) (seven lessons from [environment strategy](./08-environments-configuration-and-secrets/01-environment-strategy-and-parity/) to [drift and cleanup](./08-environments-configuration-and-secrets/07-configuration-validation-drift-and-cleanup/)).

**Day 23 — Outputs and registries:** Artifacts versus caches and job outputs, package formats, package and container registries, and registry authentication. Outputs: an artifact classification table for this repository's pipeline outputs, and a registry reference map decomposing one real GHCR image reference (registry, namespace, repository, tag, source revision, publisher, consumer).

**Day 24 — Identity and lifecycle:** Artifact naming and metadata, immutability, promotion, release bundles, and retention and cleanup. Outputs: an artifact-naming proposal for TaskOps, a promotion diagram for KubeOps (including which Git files change at each promotion), and a retention-policy proposal for the accumulated GHCR images.

**Day 25 — Environments, configuration, and secrets:** Environment strategy and parity, externalized configuration, secret management, OIDC and short-lived credentials, protected environments, and drift. Outputs: an environment map of all three projects, a configuration inventory for TaskOps, a secret-reference inventory (names only, never values), an OIDC trust-policy design, and a production-environment control proposal.

**Learning goals:** Must learn immutable artifact identity, registries, external configuration, and secret handling. Should understand promotion, retention, protected environments, preview environments, OIDC, and drift validation. Optional study includes enterprise secret rotation and cross-account registries.

**Practical activity:** Follow Project 2's image path from Dockerfile to release workflow and deployment reference. Inventory configuration versus secret inputs without displaying secret values.

**Expected output:** The daily outputs above, centered on an artifact lineage diagram and a configuration/secret boundary table.

**Related repository project:** [Project 2 — KubeOps GitOps](../Projects/2_project/kubeops-gitops/), with deployment and secret-injection contrasts from [Project 1 — TaskOps CI/CD](../Projects/1_project/taskops-cicd/) and validation examples from [Project 3](../Projects/3_project/).

## Phase 7 — Days 26–29: Delivery, Releases, and Deployment Strategies

**Topics:** [Continuous Delivery and Releases](./09-continuous-delivery-and-releases/) and [Deployment Strategies and Recovery](./10-deployment-strategies-and-recovery/).

**Day 26 — Delivery and candidates:** Delivery versus deployment, releases, release candidates, and release-pipeline design. Outputs: a CI/delivery/deployment classification and a release-candidate record.

**Day 27 — Promotion and identity:** Build once, deploy many; artifact promotion; versioning; tags; changelogs; and release notes. Outputs: a promotion diagram and release-notes draft tied to source and artifact identity.

**Day 28 — Controls and verification:** Approvals, release windows, readiness, post-release verification, communication, and audit. Outputs: an approval decision table and release-readiness checklist.

**Day 29 — Deployment and recovery:** Recreate, rolling, blue-green, canary, feature flags, zero downtime, rollback/roll-forward, and database migrations. Outputs: a deployment-strategy comparison, canary plan, health-check map, rollback decision table, and expand-and-contract migration design.

**Learning goals:** Must learn build-once promotion, release traceability, health checks, and rollback versus roll-forward. Should understand semantic releases, approvals, rolling, blue-green, canary, progressive delivery, and database compatibility. Advanced traffic management is optional.

**Practical activity:** Review Project 1's deployment, smoke-test, backup, and rollback files. Write a release decision checklist and walk through a hypothetical failed deployment without executing it.

**Expected output:** The daily outputs above, connecting release identity and evidence to a controlled deployment and recovery path.

**Related repository project:** [Project 1 — TaskOps CI/CD](../Projects/1_project/taskops-cicd/).

## Phase 8 — Days 30–33: Docker in CI/CD

**Topics:** [Docker in CI/CD](./11-docker-in-cicd/).

**Day 30 — Foundations:** Images versus containers, Dockerfiles, build context, and `.dockerignore`. Outputs: an image/container map, Dockerfile layer audit, and `.dockerignore` proposal.

**Day 31 — Efficient identity:** Layers, caching, multi-stage builds, metadata, and tags. Output: an image-tagging policy.

**Day 32 — Runtime verification:** Compose, health checks, runtime tests, and scanning. Outputs: a Compose service map and container-check classification.

**Day 33 — Publication and deployment:** Registries, publishing workflows, deployment, and review. Outputs: a registry-workflow annotation and image-deployment trace.

**Learning goals:** Must learn build context, layers, tags, image publication, and container-based test execution. Should understand multi-stage builds, Compose in CI, scanning, minimal runtime images, and immutable digests. Advanced multi-architecture builds are optional.

**Practical activity:** Compare the three project Dockerfiles and their ignore files. Build one image locally if tooling is available, inspect its tags and layers, and document where scanning and publication belong.

**Expected output:** A Dockerfile comparison and a verified image-build record or, if tooling is unavailable, an exact build plan.

**Related repository project:** [All practical projects](../Projects/).

## Phase 9 — Days 34–37: Kubernetes and GitOps

**Topics:** [Kubernetes and GitOps](./12-kubernetes-and-gitops/).

**Day 34 — Kubernetes resources:** Fundamentals, manifests, Deployments, Services, and Namespaces. Output: a Kubernetes resource relationship map.

**Day 35 — Workload configuration:** ConfigMaps, Secrets, probes, resources, and Helm. Outputs: a configuration/probe/resource audit and Helm values-to-template trace.

**Day 36 — Composition and reconciliation:** Kustomize, GitOps principles, reconciliation, and drift. Outputs: a Kustomize overlay proposal and GitOps flow diagram.

**Day 37 — Argo CD and fleet design:** Applications, sync, multi-environment, and multi-cluster concepts. Outputs: an Argo CD Application annotation and multi-environment directory proposal.

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

**Topics:** [DevSecOps and Supply-Chain Security](./14-devsecops-and-supply-chain-security/), covering [fundamentals](./14-devsecops-and-supply-chain-security/01-devsecops-fundamentals-and-security-by-design/), [SAST and secret scanning](./14-devsecops-and-supply-chain-security/02-sast-code-quality-and-secret-scanning/), [dependency analysis](./14-devsecops-and-supply-chain-security/03-dependency-license-and-software-composition-analysis/), [container and IaC scanning](./14-devsecops-and-supply-chain-security/04-container-kubernetes-and-iac-security-scanning/), [SBOMs and provenance](./14-devsecops-and-supply-chain-security/05-sbom-signing-provenance-and-attestations/), [pipeline security](./14-devsecops-and-supply-chain-security/06-secure-pipelines-permissions-actions-and-runners/), [DAST](./14-devsecops-and-supply-chain-security/07-dast-api-security-and-runtime-validation/), and [vulnerability management](./14-devsecops-and-supply-chain-security/08-vulnerability-management-exceptions-and-response/).

**Day 41 — Finding weaknesses:** DevSecOps principles, SAST and secret scanning, dependency and license analysis, and container/Kubernetes/IaC scanning. Outputs: a threat-boundary map for TaskOps, a scanner map of every real check (tool, category, stage, blocking behavior, limitation), and the Trivy scan-before-push versus scan-after-push comparison.

**Day 42 — Trust and response:** SBOMs, signing, and provenance; pipeline permissions, actions, and runners; DAST; and vulnerability management. Outputs: a workflow security audit of TaskOps CI, a designed evidence bundle for KubeOps, a safe DAST plan, and one complete sample vulnerability record.

**Learning goals:** Must learn least privilege, secret scanning, dependency risk, SAST, and container scanning. Should understand DAST, IaC scanning, SBOMs, signing, provenance, attestations, and runner isolation. Formal supply-chain maturity frameworks are optional advanced study.

**Practical activity:** Build a threat-oriented checklist for one existing workflow. Identify untrusted inputs, credential boundaries, dependencies, produced artifacts, and suitable controls without inventing results from scanners that were not run.

**Expected output:** The daily outputs above, centered on a pipeline threat checklist and prioritized security-control backlog.

**Related repository project:** [Project 1](../Projects/1_project/taskops-cicd/) plus Project 3's IaC inputs.

## Phase 12 — Days 43–44: Observability and Optimization

**Topics:** [Observability, Metrics, and Optimization](./15-observability-metrics-and-optimization/), covering [signals](./15-observability-metrics-and-optimization/01-logs-metrics-traces-and-observability-fundamentals/), [pipeline debugging](./15-observability-metrics-and-optimization/02-pipeline-observability-debugging-and-evidence/), [deployment monitoring and SLOs](./15-observability-metrics-and-optimization/03-deployment-monitoring-alerting-slis-and-slos/), [DORA metrics](./15-observability-metrics-and-optimization/04-dora-metrics-and-delivery-performance/), [incidents and postmortems](./15-observability-metrics-and-optimization/05-incidents-runbooks-on-call-and-postmortems/), [pipeline bottlenecks](./15-observability-metrics-and-optimization/06-pipeline-duration-queues-caches-and-bottlenecks/), and [cost and dashboards](./15-observability-metrics-and-optimization/07-cost-capacity-dashboards-and-continuous-optimization/).

**Day 43 — Signals and monitoring:** Logs, metrics, and traces; pipeline debugging and evidence; deployment monitoring, alerting, SLIs, and SLOs. Outputs: a telemetry inventory of all three projects, an annotated diagnostic map of TaskOps CI, and one complete SLO for the Project 3 application.

**Day 44 — Performance and learning:** DORA metrics, incidents and runbooks, pipeline duration and bottlenecks, and cost and dashboards. Outputs: a DORA measurement design from repository data, a written runbook for a failed TaskOps deployment, a duration map of TaskOps CI, and a five-signal CI/CD scorecard.

**Learning goals:** Must learn the difference between pipeline and deployment signals and the four DORA metrics. Should understand alert design, duration, queue time, cache effectiveness, incident response, runbooks, postmortems, and cost tradeoffs. Distributed tracing design is optional.

**Practical activity:** Inspect Project 3's Prometheus and Grafana assets. Propose a small dashboard that combines delivery and service signals, then identify one pipeline optimization and how to measure its effect.

**Expected output:** The daily outputs above, centered on a metric catalog, dashboard sketch, and measurable optimization hypothesis.

**Related repository project:** [Project 3 monitoring](../Projects/3_project/monitoring/) and [documentation](../Projects/3_project/docs/monitoring.md), with pipeline evidence from [Project 1](../Projects/1_project/taskops-cicd/).

## Phase 13 — Day 45: Capstone and Repository Review

**Topics:** Review all fifteen topics and connect them as one delivery system.

**Learning goals:** Must explain the path from commit to observed deployment, including controls and recovery. Should identify gaps and prioritize improvements based on risk and evidence. Implementing advanced optional topics is outside this day's scope.

**Practical activity:** Choose one existing project and produce an end-to-end CI/CD design review. Confirm documentation links, separate current behavior from proposals, and select a small next implementation milestone.

**Expected output:** A capstone architecture diagram, evidence-based gap analysis, updated learning checklist, and concise repository review.

**Related repository project:** Choose [Project 1](../Projects/1_project/taskops-cicd/), [Project 2](../Projects/2_project/kubeops-gitops/), or [Project 3](../Projects/3_project/).

## Navigation

- [Back to Learning Materials](./README.md)
- [Glossary](./glossary.md)
