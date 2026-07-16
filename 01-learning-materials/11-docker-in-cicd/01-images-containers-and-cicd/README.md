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

## From Image to Process

Containerization packages an application with the userspace files and image configuration it expects. Each image layer records a filesystem change; ordered layers are presented together when a container starts. The runtime adds a writable layer for temporary changes. Removing the container removes that layer, so durable state belongs in a named volume, persistent storage, or an external service. A stateless container can be replaced freely because important state lives elsewhere. A stateful workload needs explicit storage, backup, consistency, and recovery design.

```text
Docker image
     | docker run
Running container
     | stop
Stopped container
     | remove
Container deleted, image remains
```

An entrypoint identifies the executable, while a command supplies default arguments or, without an entrypoint, the executable itself. Environment variables provide runtime configuration but are not a universal secret solution. `EXPOSE 5000` documents an expected port; a runtime option or Compose `ports` entry publishes it. Networks let containers address services without fixed host addresses. Volumes give selected paths storage with a separate lifecycle.

A container normally runs one main application concern. That process is PID 1 inside the container and must receive termination signals, reap child processes when necessary, and exit predictably. Several cooperating processes can be justified, but unrelated daemons complicate health, logs, scaling, and shutdown. Image settings such as `USER`, working directory, entrypoint, command, and environment become defaults that the runtime may override.

## Isolation and Pipeline Environments

Containers use operating-system isolation while sharing the host kernel. A virtual machine includes a guest kernel and generally offers a stronger boundary at greater startup and resource cost. Neither is automatically secure. Kernel exposure, capabilities, privileged execution, unsafe mounts, vulnerable images, and weak runtime policy still matter.

The same image moves through distinct contexts. A build environment turns source and a Dockerfile into layers. A test environment runs or inspects the result. A runtime environment pulls the accepted identity and supplies deployment configuration. Rebuilding in the runtime environment collapses this separation and breaks confidence that tested content equals deployed content.

A CI runner may run shell steps, execute a job inside a container, or start service containers such as a database. A containerized job standardizes job tools. A service container supplies a test dependency. Building the application image produces a release candidate for scanning, publishing, and deployment.

Images can be local or remote. A pull retrieves a manifest and missing layers; a push uploads referenced content and publishes a manifest under a repository reference. Images are intended to be immutable, but a tag can move. True content identity depends on a digest and registry policy, not a friendly tag alone.

Benefits include repeatable packaging, fast startup, clear release units, dependency isolation, and a common CI/deployment interface. Limits remain: architecture must match available image content; persistent state needs separate design; networking and observability do not disappear; and images can contain vulnerable or unnecessary software. Consistency means the same packaged userspace, not identical behavior on every host.

## Repository Evidence

[TaskOps Dockerfile](../../../Projects/1_project/taskops-cicd/Dockerfile) exposes 5000, runs as `appuser`, and defines `/health`; production Compose persists SQLite in a named volume and deploys a GHCR image.

The complete map is: the Dockerfile creates the image and sets Gunicorn as its command; `EXPOSE 5000` documents the application port; `USER appuser` selects the created UID 1000; `/data` is declared as a volume; and the health check calls `/health`. [Development Compose](../../../Projects/1_project/taskops-cicd/docker-compose.yml) names the local image `taskops:latest` and publishes port 5000. [Production Compose](../../../Projects/1_project/taskops-cicd/docker-compose.prod.yml) consumes a configurable GHCR repository and `IMAGE_TAG`, mounts `taskops-data`, and places nginx in front. The CD workflow supplies the commit SHA as the deployed tag. These files demonstrate the chain without proving an external server is currently running it.

## Common Mistakes

Manual container changes, writable-layer data, treating `EXPOSE` as publication, treating containers as VMs, unclear multi-process design, outside-CI builds, and untraceable tags.

## Evidence Review

Record image references separately from container names and IDs. Note the PID 1 process, documented versus published ports, ephemeral paths, durable volumes, required networks, and runtime identity. Then identify build, test, and runtime environments and confirm that they consume the same content. This inventory prevents a manually adjusted running container from being mistaken for the release artifact and exposes shutdown, persistence, architecture, and privilege assumptions before deployment.

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
