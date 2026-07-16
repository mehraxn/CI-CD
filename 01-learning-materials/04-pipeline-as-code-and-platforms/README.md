# Pipeline as Code and Platforms

## Overview

Pipeline as Code means storing pipeline configuration as versioned files in the same version-control system as the software it builds and delivers. Instead of clicking options in a web interface, the team describes triggers, jobs, and rules in files such as a GitHub Actions workflow, a `Jenkinsfile`, or a `.gitlab-ci.yml`, and changes those files through the normal commit-and-review process.

This section covers the idea itself, the YAML syntax most platforms use, how data flows through variables and expressions, how configuration is reused, where jobs actually execute, and how the three most common platforms — GitHub Actions, Jenkins, and GitLab CI/CD — structure the same concepts. GitHub Actions receives the deepest treatment because it is the platform this repository's practical projects actually use.

## Why Version-Control the Pipeline

```text
Developer changes pipeline configuration
                    ↓
Pipeline file is committed to Git
                    ↓
Pull request and review
                    ↓
Syntax and configuration validation
                    ↓
Change is merged
                    ↓
Updated pipeline behavior takes effect
                    ↓
Git history supports auditing and rollback
```

Every pipeline change becomes visible, reviewable, and reversible. When a deployment behaves differently this week than last week, `git log` on the workflow file answers "what changed, when, and by whom" — a question that UI-only configuration often cannot answer.

| Area | UI-only configuration | Pipeline as Code |
|------|-----------------------|------------------|
| Version history | Often limited or separate | Stored in Git |
| Review | Often difficult | Pull-request based |
| Reproducibility | Usually lower | Usually higher |
| Auditability | Platform dependent | Git history plus pipeline logs |
| Rollback | Often manual | Can use version history |
| Portability | Usually limited | Potentially improved, but still platform dependent |

## Benefits Are Not Guarantees

Pipeline as Code is a foundation, not a certificate. It does **not** automatically guarantee security, correctness, maintainability, portability, reproducibility, good testing, or appropriate permissions. A badly designed workflow committed to Git is still a badly designed workflow — it is merely a *visible and reviewable* one. Review and change-management discipline (small changes, a second reviewer for pipeline files, validation before merge) is what converts visibility into quality.

## Lessons

| Number | Lesson | Main focus |
|---|---|---|
| 01 | [Pipeline as Code Fundamentals](./01-pipeline-as-code-fundamentals/) | Versioned, reviewed, auditable pipeline configuration |
| 02 | [YAML Fundamentals](./02-yaml-fundamentals/) | The syntax layer beneath most pipeline files |
| 03 | [Variables, Contexts, Expressions, and Outputs](./03-variables-contexts-expressions-and-outputs/) | How data flows into, through, and between jobs |
| 04 | [Reusable Workflows, Templates, and Components](./04-reusable-workflows-templates-and-components/) | Reducing duplication without hiding logic |
| 05 | [Runners and Execution Environments](./05-runners-and-execution-environments/) | Where jobs actually execute and what that implies |
| 06 | [GitHub Actions](./06-github-actions/) | The repository's primary platform, in depth |
| 07 | [Jenkins](./07-jenkins/) | Controller/agent model, Jenkinsfile, and plugins |
| 08 | [GitLab CI/CD](./08-gitlab-cicd/) | Stages, jobs, rules, and `.gitlab-ci.yml` |

## Learning Objectives

After completing this section, the learner should be able to:

- explain what Pipeline as Code is and why it belongs in version control;
- read and write correct YAML and distinguish valid syntax from valid pipeline semantics;
- trace variables, expressions, inputs, outputs, and secrets through a workflow;
- distinguish reusable workflows, composite actions, templates, and shared libraries;
- explain hosted, self-hosted, and ephemeral runner tradeoffs;
- read any GitHub Actions workflow in this repository line by line; and
- recognize the equivalent concepts in Jenkins and GitLab CI/CD.

## Recommended Study Order

Follow the numbered order. Fundamentals and YAML establish the file format; variables and reuse explain how data and structure scale; runners ground everything in real machines. Study GitHub Actions in depth before the Jenkins and GitLab overviews, because the comparison lessons assume the GitHub Actions vocabulary.

## Platform Overview

| Platform | Main configuration | Execution workers | Typical strength |
|----------|--------------------|-------------------|------------------|
| GitHub Actions | YAML workflows | Hosted or self-hosted runners | GitHub-native automation |
| Jenkins | Jenkinsfile or UI configuration | Agents, nodes, and executors | Flexible self-hosted automation |
| GitLab CI/CD | `.gitlab-ci.yml` | GitLab Runners | Integrated GitLab delivery workflow |

## Detailed Platform Comparison

| Area | GitHub Actions | Jenkins | GitLab CI/CD |
|------|----------------|---------|---------------|
| Main configuration | YAML files in `.github/workflows/` | `Jenkinsfile` (Groovy) or UI jobs | `.gitlab-ci.yml` at repository root |
| Hosting model | SaaS (GitHub) with optional self-hosted runners | Self-hosted controller (or managed offerings) | SaaS (GitLab.com) or self-managed |
| Execution workers | Hosted and self-hosted runners | Agents/nodes with executors | GitLab Runners with executors |
| Repository integration | Native to GitHub events | Via plugins and webhooks | Native to GitLab events |
| Maintenance responsibility | Mostly provider; runners optional | Mostly the operating team | Provider on GitLab.com; team if self-managed |
| Reuse model | Reusable workflows, composite actions, marketplace actions | Shared Libraries | `include`, templates, components, child pipelines |
| Extension model | Actions (marketplace and local) | Plugins | Templates, components, integrations |
| Suitable situations | Repositories already on GitHub | Heavily customized or internal-network automation | Repositories already on GitLab |
| Main operational concern | Third-party action supply chain, token permissions | Plugin and controller maintenance, upgrades, backup | Runner fleet management on self-managed instances |

Choosing among them depends on the existing source-control platform, team experience, security and compliance requirements, cost, maintenance capacity, runner and internal-network needs, cloud integration, repository count, plugin or extension requirements, and migration effort. No platform is universally best; the strongest single predictor is where the code already lives.

## Practical Project Connections

All real pipeline configuration in this repository is GitHub Actions:

- [TaskOps CI](../../Projects/1_project/taskops-cicd/.github/workflows/ci.yml) and [TaskOps CD](../../Projects/1_project/taskops-cicd/.github/workflows/cd.yml) in Project 1.
- [KubeOps CI](../../Projects/2_project/kubeops-gitops/.github/workflows/ci.yml) and [KubeOps image release](../../Projects/2_project/kubeops-gitops/.github/workflows/image-release.yml) in Project 2.

There is no `Jenkinsfile` and no `.gitlab-ci.yml` in the repository; lessons 07 and 08 are conceptual comparisons.

## Completion Checklist

- [ ] I can explain Pipeline as Code and its limits.
- [ ] I can read and validate YAML, including block scalars and quoting.
- [ ] I can map variable scope, precedence, and output flow in a real workflow.
- [ ] I can distinguish the four main reuse mechanisms.
- [ ] I can compare hosted, self-hosted, and ephemeral runners.
- [ ] I annotated one real GitHub Actions workflow completely.
- [ ] I can describe Jenkins and GitLab CI/CD structure at a conversational level.
- [ ] I completed all exercises and knowledge checks.

## Navigation

- [Back to Learning Materials](../README.md)
- [Previous: Pipeline Architecture](../03-pipeline-architecture/)
- [Next: Builds, Dependencies, and Caching](../05-builds-dependencies-and-caching/)
