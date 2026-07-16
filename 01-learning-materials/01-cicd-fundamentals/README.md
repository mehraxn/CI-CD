# CI/CD Fundamentals

## Overview

CI/CD is a set of engineering practices for integrating changes, checking them automatically, and moving software toward a release in a repeatable way. The abbreviation combines continuous integration (CI) with continuous delivery or continuous deployment (CD). Those two meanings of CD are related, but they describe different production-release decisions.

This section builds the vocabulary needed before studying pipeline architecture or a particular automation platform. It focuses on the purpose of each practice, the flow of a change, and the feedback that helps a team correct problems.

## Why CI/CD Exists

Software changes from many people must eventually work together. If integration happens rarely, conflicts and defects accumulate. If builds, tests, packaging, and deployments depend on undocumented manual steps, results vary and releases become stressful. Slow feedback also allows a small error to remain hidden while more work is built on top of it.

CI/CD helps address these problems through small changes, frequent integration, automated verification, repeatable artifacts, controlled delivery, and visible results. It does not eliminate defects or operational risk. It makes important checks repeatable and gives the team earlier evidence for decisions.

## A Simplified Delivery Flow

```text
Developer changes code
        |
        v
Code is pushed to Git
        |
        v
Automated pipeline starts
        |
        v
Build and tests run
        |
        v
Artifact is produced
        |
        v
Application is delivered or deployed
        |
        v
Monitoring provides feedback
```

This is a conceptual flow. A real pipeline may contain parallel jobs, security checks, multiple environments, approvals, rollback logic, and several feedback paths.

## Lessons

| Number | Lesson | Main question |
|---|---|---|
| 01 | [Continuous Integration](./01-continuous-integration/) | How are changes integrated and verified frequently? |
| 02 | [Continuous Delivery](./02-continuous-delivery/) | How is software kept ready for a production release? |
| 03 | [Continuous Deployment](./03-continuous-deployment/) | When can qualifying changes reach production automatically? |
| 04 | [CI vs. Delivery vs. Deployment](./04-ci-vs-delivery-vs-deployment/) | Where do the three practices differ? |
| 05 | [Pipeline Anatomy](./05-pipeline-anatomy/) | What are the essential parts of a pipeline? |
| 06 | [DevOps and Feedback Loops](./06-devops-and-feedback-loops/) | How do collaboration and feedback support delivery? |

## Learning Objectives

After completing this section, the learner should be able to:

- distinguish continuous integration, continuous delivery, and continuous deployment;
- trace a change from a Git event through verification and release;
- explain the roles of jobs, steps, runners, artifacts, gates, and environments;
- identify feedback from review, automation, deployment, monitoring, and users; and
- inspect a basic workflow without assuming every successful pipeline deploys.

## Recommended Study Order

Follow the numbered lessons. Learn CI first because delivery and deployment depend on trustworthy integration. Compare the three practices before studying pipeline vocabulary. Finish with DevOps and feedback loops to place automation inside the broader way a team works.

## Conceptual Example

A developer fixes a validation bug on a small branch and opens a pull request. CI installs dependencies, checks formatting, runs tests, and builds the application. After review, the change merges. A delivery process creates a versioned artifact and verifies it in a staging environment. If production requires approval, the organization is practicing continuous delivery. If the eligible artifact proceeds automatically without a required manual release action, it is practicing continuous deployment.

## Practical Project Connections

- [TaskOps CI workflow](../../Projects/1_project/taskops-cicd/.github/workflows/ci.yml) runs on pull requests and pushes to `main`, then performs quality, security, image-build, image-scan, and smoke-test work.
- [TaskOps CD workflow](../../Projects/1_project/taskops-cicd/.github/workflows/cd.yml) runs on pushes to `main`, verifies the change, publishes commit-SHA and `latest` image tags, deploys over SSH, and runs a health smoke test.
- [KubeOps CI workflow](../../Projects/2_project/kubeops-gitops/.github/workflows/ci.yml) validates pushes and pull requests without deploying. Its documentation states that Argo CD handles deployment.

## Completion Checklist

- [ ] I can define CI, continuous delivery, and continuous deployment.
- [ ] I can explain why small changes and fast feedback matter.
- [ ] I can identify the major parts of a workflow.
- [ ] I can distinguish producing an artifact from releasing it.
- [ ] I can identify real CI/CD behavior in the practical projects.
- [ ] I completed the six lesson exercises and knowledge checks.

## Navigation

- [Back to Learning Materials](../README.md)
- [Next: Git and Collaboration](../02-git-and-collaboration/)
