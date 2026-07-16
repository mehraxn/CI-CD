# Docker in CI/CD

Docker packages an application and runtime dependencies into a versioned image so CI and deployment use consistent content.

```text
Source code → Dockerfile → Image build → Tests → Image scan → Registry push → Deployment pulls verified image
```

**Dockerfile:** build instructions. **Image:** intended-immutable filesystem layers and metadata. **Container:** an image runtime instance. **Registry:** image storage/distribution. **Compose file:** declarative related-container configuration.

An image does not guarantee security, reproducibility, small size, correct configuration/behavior, or support for every CPU architecture.

## Lessons

| # | Lesson |
|---|--------|
| 01 | [Images, Containers, and CI/CD](./01-images-containers-and-cicd/) |
| 02 | [Dockerfiles, Build Context, and dockerignore](./02-dockerfiles-build-context-and-dockerignore/) |
| 03 | [Layers, Caching, and Multi-Stage Builds](./03-layers-caching-and-multi-stage-builds/) |
| 04 | [Image Tagging, Versioning, and Metadata](./04-image-tagging-versioning-and-metadata/) |
| 05 | [Docker Compose in Development and CI](./05-docker-compose-in-development-and-ci/) |
| 06 | [Container Testing, Health Checks, and Scanning](./06-container-testing-health-checks-and-scanning/) |
| 07 | [Publishing Images and Registry Workflows](./07-publishing-images-and-registry-workflows/) |
| 08 | [Deploying Container Images](./08-deploying-container-images/) |

## Learning Objectives

Explain image lifecycle, build context, layer caching, tags/digests, Compose testing, scanning, publication, and verified deployment.

## Study Order and Project Connections

Follow the numbered sequence. [TaskOps Dockerfile](../../Projects/1_project/taskops-cicd/Dockerfile) demonstrates non-root execution, dependency-first copying, health checking, and CI BuildKit cache. [KubeOps image release](../../Projects/2_project/kubeops-gitops/.github/workflows/image-release.yml) publishes SHA and `latest` tags to GHCR. None of the three Dockerfiles is multi-stage; QEMU and multi-architecture publication are absent.

## Completion Checklist

- [ ] I distinguish image from container.
- [ ] I can audit build context and layers.
- [ ] I can explain scan limits and registry permissions.
- [ ] I can trace one verified image into deployment.

## Navigation

- [Back to Learning Materials](../README.md)
- [Previous: Deployment Strategies and Recovery](../10-deployment-strategies-and-recovery/)
- [Next: Kubernetes and GitOps](../12-kubernetes-and-gitops/)
