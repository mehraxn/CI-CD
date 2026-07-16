# Docker in CI/CD

Docker packages an application and runtime dependencies into a versioned image so CI and deployment use consistent content.

```text
Source code → Dockerfile → Image build → Tests → Image scan → Registry push → Deployment pulls verified image
```

**Dockerfile:** build instructions. **Image:** intended-immutable filesystem layers and metadata. **Container:** an image runtime instance. **Registry:** image storage/distribution. **Compose file:** declarative related-container configuration.

An image does not guarantee security, reproducibility, small size, correct configuration/behavior, or support for every CPU architecture.

## Container Delivery Model

In a traditional pipeline, build and deployment hosts can accumulate different libraries, tools, and defaults. An image narrows that gap by carrying a defined filesystem and runtime configuration from verification to deployment. The pipeline can test the same image reference that a server or cluster later pulls. This is **build once, deploy many** for container delivery: inject environment-specific configuration at runtime instead of creating a different image per environment.

```text
Source code
    |
Dockerfile
    |
Image build
    |
Automated tests
    |
Image scan
    |
Registry push
    |
Deployment pulls verified image
```

The objects have different responsibilities:

- **Dockerfile:** instructions for building an image from a base and files in a build context.
- **Image:** intended-immutable filesystem layers and metadata used to start containers.
- **Container:** a running or stopped instance created from an image, with a temporary writable layer.
- **Registry:** a service that stores and distributes image manifests and layers.
- **Compose file:** a declarative definition for running related containers, networks, and volumes.

Source code alone is not the release unit in this model. The Dockerfile selects and assembles it, CI creates an image, and a registry makes that verified object available to deployment systems. A deployment should identify the accepted image with a traceable tag and preferably record its content digest. It should not quietly rebuild from source because that produces a new, unverified object.

Images improve consistency but do not guarantee security, reproducibility, small size, correct configuration, correct runtime behavior, or portability across every CPU architecture. Those properties require deliberate controls: review base images and dependencies, stabilize build inputs, scan and runtime-test images, keep secrets out of layers, and explicitly build each supported architecture. Containers do not replace application testing, least privilege, monitoring, backups, or recovery planning.

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

After completing this topic, you should be able to:

- explain image lifecycle and why a container writable layer is temporary;
- audit a Dockerfile, its build context, and `.dockerignore` rules;
- arrange layers for caching and explain when multi-stage builds help;
- compare mutable tags with content-addressed digests;
- describe Compose-based local and CI test stacks;
- place smoke tests, health checks, and scans at useful gates;
- describe least-privilege registry publication; and
- trace an accepted image from source revision to deployment and rollback.

## Study Order and Project Connections

Follow the numbered sequence because image structure leads naturally to build inputs, caching, identity, testing, publication, and deployment.

[TaskOps Dockerfile](../../Projects/1_project/taskops-cicd/Dockerfile) demonstrates dependency-first copying, a non-root user, persistent-data metadata, port metadata, and a Docker health check. Its [CI workflow](../../Projects/1_project/taskops-cicd/.github/workflows/ci.yml) uses Buildx with the GitHub Actions cache, scans the loaded image with Trivy, runs it, tests `/health`, and cleans it up. Its [CD workflow](../../Projects/1_project/taskops-cicd/.github/workflows/cd.yml) publishes commit-SHA and `latest` tags to GHCR before deploying the SHA tag through production Compose.

[KubeOps image release](../../Projects/2_project/kubeops-gitops/.github/workflows/image-release.yml) also publishes SHA and `latest` tags, then scans the pushed SHA image. Its Kubernetes and Helm files consume repository/tag fields. [Project 3 Compose](../../Projects/3_project/docker-compose.yml) combines an application with Prometheus and Grafana, but its workflow directory contains only `.gitkeep`; no executable image workflow is present. None of the three Dockerfiles is multi-stage. QEMU, multi-architecture publication, OCI labels, signing, SBOM publication, and recorded deployment digests are absent.

## Completion Checklist

- [ ] I distinguish image from container.
- [ ] I can audit build context and layers.
- [ ] I can explain scan limits and registry permissions.
- [ ] I can trace one verified image into deployment.
- [ ] I can separate repository evidence from conceptual recommendations.

## Navigation

- [Back to Learning Materials](../README.md)
- [Previous: Deployment Strategies and Recovery](../10-deployment-strategies-and-recovery/)
- [Next: Kubernetes and GitOps](../12-kubernetes-and-gitops/)
