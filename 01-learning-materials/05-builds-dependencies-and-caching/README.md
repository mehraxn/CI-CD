# Builds, Dependencies, and Caching

## Overview

A build turns a specific source revision and its dependencies into verified, versioned output. This section covers the build lifecycle and its tools, how dependency managers and lockfiles control what goes into a build, why pinning and reproducibility matter, how caching makes builds fast without making them wrong, how metadata connects an output back to its source, and what changes when one build must serve several platforms or architectures.

```text
Build:
The process that transforms source code and configuration into verified output.

Artifact:
A preserved output produced by a build or test job.

Cache:
Reusable data intended mainly to make later runs faster.
```

## Why Reliable Builds Matter

CI/CD rests on a chain of trust: source code plus dependencies produce a build output; verification turns that output into an artifact worth keeping; deployment moves *the same* artifact through environments. If the build step is unreliable — different results from the same source, dependencies that drift, caches that leak stale data — everything downstream inherits the unreliability. A pipeline can only promote what the build produced, so the build must be predictable, traceable, and fast enough to give useful feedback.

```text
Source code
    ↓
Resolve dependencies
    ↓
Restore safe caches
    ↓
Compile, package, or assemble
    ↓
Run verification
    ↓
Create versioned build output
    ↓
Publish or deploy the same output
```

## Not Every Build Compiles

"Build" does not always mean compilation:

- Python may package or assemble an application without traditional compilation — this repository's projects install dependencies and build container images around interpreted code.
- Java commonly compiles and packages bytecode.
- Go commonly compiles a native binary.
- JavaScript applications may transpile, bundle, or package assets.
- Containers build filesystem layers and an image manifest.

The lifecycle above applies to all of them; only the "compile, package, or assemble" step differs.

## Lessons

| Number | Lesson | Main focus |
|---|---|---|
| 01 | [Build Lifecycle and Build Tools](./01-build-lifecycle-and-build-tools/) | What a build is, its phases, and the tools that run it |
| 02 | [Dependency Management and Lockfiles](./02-dependency-management-and-lockfiles/) | Manifests, lockfiles, resolution, and dependency risk |
| 03 | [Version Pinning and Reproducible Builds](./03-version-pinning-and-reproducible-builds/) | Repeatable, reproducible, deterministic, and hermetic builds |
| 04 | [Build Caching](./04-build-caching/) | Cache keys, invalidation, layer caching, and cache safety |
| 05 | [Build Metadata and Version Injection](./05-build-metadata-and-version-injection/) | Versions, commit SHAs, labels, and traceability |
| 06 | [Cross-Platform and Multi-Architecture Builds](./06-cross-platform-and-multi-architecture-builds/) | OS and CPU differences, multi-platform images |

## Learning Objectives

After completing this section, the learner should be able to:

- describe a build lifecycle and identify its inputs and outputs;
- distinguish manifests, pinned lists, lockfiles, and constraints files;
- explain repeatable, reproducible, deterministic, and hermetic builds;
- design a safe cache key and reason about invalidation and poisoning;
- attach traceable version metadata to a build output; and
- identify platform and architecture assumptions in a real project.

## Recommended Study Order

Follow the numbered order: lifecycle first (what a build is), then dependencies (what goes in), pinning (keeping inputs stable), caching (keeping it fast safely), metadata (naming what comes out), and finally multi-platform concerns (doing all of it more than once).

## Practical Project Connections

The three projects deliberately illustrate different points on the spectrum:

- [TaskOps (Project 1)](../../Projects/1_project/taskops-cicd/) — exactly pinned [requirements.txt](../../Projects/1_project/taskops-cicd/requirements.txt), a [Dockerfile](../../Projects/1_project/taskops-cicd/Dockerfile) with deliberate cache-friendly layer ordering, a [Makefile](../../Projects/1_project/taskops-cicd/Makefile) matching CI commands, and a [CI workflow](../../Projects/1_project/taskops-cicd/.github/workflows/ci.yml) with pip and Docker layer caching.
- [KubeOps (Project 2)](../../Projects/2_project/kubeops-gitops/) — *unpinned* [requirements.txt](../../Projects/2_project/kubeops-gitops/requirements.txt), and an [image-release workflow](../../Projects/2_project/kubeops-gitops/.github/workflows/image-release.yml) that tags images with the commit SHA.
- [Project 3](../../Projects/3_project/app/) — version *ranges* in [requirements.txt](../../Projects/3_project/app/requirements.txt) and a `/version` endpoint in the application.

## Completion Checklist

- [ ] I can draw the build lifecycle for one real project.
- [ ] I classified every dependency file in the repository.
- [ ] I can explain why the three projects' pinning styles behave differently.
- [ ] I identified the real caching in TaskOps CI and its invalidation inputs.
- [ ] I traced how one real image tag connects back to a commit.
- [ ] I documented the platform assumptions the projects make.
- [ ] I completed all exercises and knowledge checks.

## Navigation

- [Back to Learning Materials](../README.md)
- [Previous: Pipeline as Code and Platforms](../04-pipeline-as-code-and-platforms/)
- [Next: Automated Testing and Quality](../06-automated-testing-and-quality/)
