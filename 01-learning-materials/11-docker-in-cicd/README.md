# Docker in CI/CD

## Overview

Docker packages an application and its runtime filesystem as an image that pipelines can build and distribute. This topic covers image builds, build context, multi-stage Dockerfiles, tagging, Compose-based CI environments, scanning, publishing, and deployment.

## Why It Matters

Containers can make build and runtime environments more consistent, but only when images are small, traceable, securely built, and immutable. The build context and Dockerfile affect performance and information exposure, while tagging and publishing rules determine whether a deployment points to the intended image.

## Main Concepts

- Reproducible image builds and controlled build context
- Multi-stage images and runtime minimization
- Traceable tags, scanning, and registry publication
- Compose-based integration and image deployment

## Learning Objectives

After completing this section, the learner should be able to:

- Explain how a pipeline turns source into a container image.
- Use build context, stages, and tags deliberately.
- Outline checks required before publishing and deploying an image.

## Planned Subtopics

- [ ] Building Docker images in pipelines
- [ ] Docker build context
- [ ] Multi-stage builds
- [ ] Image tagging
- [ ] Docker Compose in CI
- [ ] Image scanning
- [ ] Publishing images
- [ ] Deploying container images

## Related Practical Projects

All three [projects](../../Projects/) contain Dockerfiles or Compose configuration. Project 1 combines application delivery with Compose, Project 2 includes an image-release workflow, and Project 3 supplies a multi-service Compose stack. These are useful for comparing contexts and deployment targets without modifying their implementations.

## Navigation

- [Back to Learning Materials](../README.md)
- [Previous: Deployment Strategies and Recovery](../10-deployment-strategies-and-recovery/)
- [Next: Kubernetes and GitOps](../12-kubernetes-and-gitops/)
