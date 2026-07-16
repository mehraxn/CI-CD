# Git and Collaboration

## Overview

Git records the history of a project and provides the events that many CI/CD systems observe. A commit identifies a source state, a branch supports isolated work, a pull request creates a review boundary, and a tag can identify a release. These concepts make automated results traceable to exact changes.

Version control is essential to CI/CD because automation needs a reliable source of truth. A pipeline can answer "which commit was tested?" only when history and references are managed consistently. Git does not enforce good collaboration by itself; teams add review conventions, protected branches, status checks, and release rules.

## A Common Collaboration Flow

```text
Create branch
    |
    v
Make a small change
    |
    v
Commit change
    |
    v
Push branch
    |
    v
Open pull request
    |
    v
CI pipeline runs
    |
    v
Code review
    |
    v
Merge into main
    |
    v
Release or deployment pipeline starts
```

This flow is common, not universal. Trunk-based teams may use very short branches or direct integration under strong controls. A tag or manual event may start release automation instead of every merge.

## Lessons

| Number | Lesson | Main focus |
|---|---|---|
| 01 | [Git Fundamentals](./01-git-fundamentals/) | Repository state and the basic local/remote workflow |
| 02 | [Commits and History](./02-commits-and-history/) | Focused snapshots, useful history, and safe undoing |
| 03 | [Branches, Merging, and Rebasing](./03-branches-merging-and-rebasing/) | Parallel work and integration choices |
| 04 | [Pull Requests and Code Review](./04-pull-requests-and-code-review/) | Review, automated checks, and collaboration responsibilities |
| 05 | [Branching Strategies](./05-branching-strategies/) | Selecting a branch model that supports delivery flow |
| 06 | [Tags, Versioning, and Releases](./06-tags-versioning-and-releases/) | Immutable release references and semantic versions |
| 07 | [Protected Branches and Merge Rules](./07-protected-branches-and-merge-rules/) | Repository controls that protect shared history |

## Learning Objectives

After completing this section, the learner should be able to:

- distinguish the working directory, staging area, local repository, and remote;
- create focused commits and inspect or undo history safely;
- compare merge, squash, and rebase behavior;
- participate in a small pull request with useful review evidence;
- select a simple branching strategy for a CI/CD project; and
- explain how tags, status checks, and branch protections affect automation.

## Recommended Study Order

Follow the numbered order. Git fundamentals establishes the state model used by every later command. Commits come before branches because branches point into commit history. Study pull requests after integration mechanics, then compare broader strategies. Finish with release references and server-side controls.

## Git Events and GitHub Actions

Git hosting platforms translate repository activity into events. GitHub Actions can react to `push`, `pull_request`, manual dispatch, schedules, and other events. Filters can narrow a push to `main` or to tags. A workflow result can become a required status check before merge. These are GitHub mechanisms built around general version-control events; other platforms use different configuration and names.

## Practical Project Connections

- [TaskOps CI](../../Projects/1_project/taskops-cicd/.github/workflows/ci.yml) validates pull requests and pushes to `main`.
- [TaskOps CD](../../Projects/1_project/taskops-cicd/.github/workflows/cd.yml) starts on a push to `main`, illustrating how merge activity can lead to deployment.
- [KubeOps CI](../../Projects/2_project/kubeops-gitops/.github/workflows/ci.yml) runs for every push and pull request.
- [KubeOps image release](../../Projects/2_project/kubeops-gitops/.github/workflows/image-release.yml) starts from `main` or manual dispatch. No existing workflow uses a version-tag trigger, so that remains a later exercise.

## Completion Checklist

- [ ] I understand Git's main storage areas and remote workflow.
- [ ] I can create a focused commit and inspect its difference.
- [ ] I can explain merge versus rebase and resolve a simple conflict.
- [ ] I can prepare and review a small pull request.
- [ ] I can compare common branching strategies.
- [ ] I can create an annotated local tag safely.
- [ ] I can propose beginner protection rules for `main`.

## Navigation

- [Back to Learning Materials](../README.md)
- [Previous: CI/CD Fundamentals](../01-cicd-fundamentals/)
- [Next: Pipeline Architecture](../03-pipeline-architecture/)
