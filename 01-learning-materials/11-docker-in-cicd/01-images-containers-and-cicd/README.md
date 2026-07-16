# Images, Containers, and CI/CD

An image is a reusable template of read-only layers and configuration; a container adds a temporary writable layer and runs the configured process. Durable state belongs in volumes or external services.

```text
Docker image → docker run → Running container → stop → Stopped container → remove
Container deleted, image remains
```

| Area | Image | Container |
|------|-------|-----------|
| Purpose | Reusable template | Runtime instance |
| Mutability | Intended immutable | Temporary writable layer |
| Storage | Local or registry | Runtime |
| Lifecycle | Built/versioned | Created, started, stopped, removed |

Image configuration supplies entrypoint, command, environment, user, working directory, and exposed ports. `EXPOSE` documents a port; runtime publication maps it. Networks connect services and volumes persist data. PID 1 must handle signals and shutdown. Containers isolate processes/filesystems while sharing the host kernel, unlike full virtual machines.

CI runners can build images, run containerized jobs, or start service containers. Build once and deploy the same verified image to avoid environment rebuild drift. Containers do not remove kernel risk, state management, networking, architecture, or observability concerns.

## Repository Evidence

[TaskOps Dockerfile](../../../Projects/1_project/taskops-cicd/Dockerfile) exposes 5000, runs as `appuser`, and defines `/health`; production Compose persists SQLite in a named volume and deploys a GHCR image.

## Common Mistakes

Manual container changes, writable-layer data, treating `EXPOSE` as publication, treating containers as VMs, unclear multi-process design, outside-CI builds, and untraceable tags.

## Practical Exercise

Map Dockerfile, image, command, port, user, volume, health check, registry, and deployment consumer for TaskOps. Do not run it.

## Knowledge Check

1. Image versus container? 2. Where should durable data live? 3. Does `EXPOSE` publish? 4. Why build once?

<details><summary>Answers</summary>

1. Template versus runtime instance. 2. Volume/external store. 3. No. 4. To deploy verified identical content.

</details>

## Navigation
- [Back to Docker in CI/CD](../README.md)
- [Next: Dockerfiles, Build Context, and dockerignore](../02-dockerfiles-build-context-and-dockerignore/)
- [Back to All Learning Materials](../../README.md)
