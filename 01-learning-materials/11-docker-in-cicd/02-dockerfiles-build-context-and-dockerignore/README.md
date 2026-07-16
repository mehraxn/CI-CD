# Dockerfiles, Build Context, and `.dockerignore`

```text
Build context: files available to the builder.
Dockerfile: instructions selecting files and creating layers.
.dockerignore: exclusions from context.
```

`FROM` selects a base; `WORKDIR`, `COPY`, `RUN`, `ENV`, `ARG`, `USER`, `EXPOSE`, `VOLUME`, `HEALTHCHECK`, `ENTRYPOINT`, and `CMD` shape content and runtime defaults. Exec-form commands handle signals more directly than shell form. `ADD` has extra archive/URL behavior and should be chosen deliberately. `COPY --chown` establishes ownership without later repair layers.

## How a Build Is Assembled

The context root is the directory passed to the builder, usually the final `docker build` argument. A Dockerfile can be selected elsewhere, but `COPY` and `ADD` only read files made available through that context. They cannot reach outside with `../`. A repository-root context may send unrelated history, test output, databases, and credentials unless ignore rules exclude them. Smaller relevant contexts improve transfer time and reduce accidental input.

`FROM` establishes a base filesystem and configuration. Pinning a reviewed version or digest improves predictability; an unreviewed moving base can change between builds. `WORKDIR` selects the directory for later instructions. `COPY` is preferred for ordinary local files; `ADD` includes archive extraction and remote-source behavior and should be deliberate. Deterministic copy order makes inputs and invalidation visible.

`RUN` executes at build time and records output in a layer. `ARG` provides a build-time value, whereas `ENV` persists a default in image configuration. Neither is safe for sensitive credentials. BuildKit secret mounts can expose a value only to one instruction when correctly used; no repository Dockerfile demonstrates them. Image history and cache output still need review.

`USER` chooses the runtime identity. Creating an unprivileged account and assigning minimal ownership limits damage. `COPY --chown` sets ownership as files enter the image. `EXPOSE` documents a port, not host publication. `VOLUME` identifies persistent intent but not backup or production storage. `HEALTHCHECK` supplies a runtime check. `ENTRYPOINT` and `CMD` define startup: exec form starts the program directly and handles signals more predictably, while shell form enables shell syntax but may complicate forwarding.

Conceptual exclusions:

```text
.git
.venv
__pycache__
*.pyc
.env
coverage.xml
htmlcov
dist
build
```

Exclude secrets, Git metadata, generated output, caches, and unnecessary tests while retaining required dependency/application files. Ordinary `ARG`/`ENV` are not secret stores; deleting a copied secret later does not remove it from earlier history. Use supported secret mounts and ensure no secret reaches layers or cache.

Educational example:

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY app/ ./app/
USER 1000
CMD ["python", "-m", "app"]
```

## Educational Example Explained

The example above is conceptual, not a repository change. `FROM` selects Python. `WORKDIR` creates/selects `/app`. Copying only `requirements.txt` first allows dependency installation to remain cached when source changes. The second copy adds frequently changing code. `USER 1000` requests an unprivileged identity, though a production image must ensure it exists and has access. Exec-form `CMD` launches the module directly.

`.dockerignore` applies before Dockerfile copies. Git metadata, virtual environments, bytecode, coverage, local builds, editor files, logs, databases, and `.env` are common exclusions. Tests might be excluded from runtime context, but doing so breaks a build stage intended to run them. Required dependency files must remain. Negation can re-include a safe template, so rule order matters.

Never copy a real `.env`, registry credential, key, or package token. Normal `ARG`, `ENV`, or a write-then-delete sequence is unsafe: earlier layers and build records can retain the value. A private repository does not protect a secret embedded in an image. Use supported ephemeral secret mechanisms and verify output and history.

## Repository Audit

[TaskOps](../../../Projects/1_project/taskops-cicd/Dockerfile) assumes its project directory is context, starts from `python:3.12-slim`, copies dependencies first, creates `appuser`, uses `COPY --chown`, exposes 5000, declares `/data`, and checks health. Its [ignore file](../../../Projects/1_project/taskops-cicd/.dockerignore) excludes tests, docs, scripts, databases, Git, caches, and real `.env` while retaining `.env.example`.

[KubeOps](../../../Projects/2_project/kubeops-gitops/Dockerfile) copies dependencies first, creates UID 1000, exposes 8000, and checks `/health`. Its [ignore file](../../../Projects/2_project/kubeops-gitops/.dockerignore) excludes tests, docs, and environment files. [Project 3](../../../Projects/3_project/app/Dockerfile) uses `app` as its Compose context, starts from `python:3.13-slim`, copies dependencies before `main.py`, and exposes 8000. It lacks `USER` and `HEALTHCHECK`, and no `.dockerignore` sits beside it. The accurate total is three Dockerfiles and two `.dockerignore` files.

Audit base selection, context, dependency/application layers, identity, health, and exclusions. Do not modify the files during this exercise.

## Review Method

Start at the build command to identify context and Dockerfile selection. List every `COPY`/`ADD` source and prove it is inside context and not excluded. Compare ignore rules with dependency, test, and packaging steps: a small context is useless if required input is missing. Identify secrets, databases, logs, and generated files that would enter without exclusions.

Read instructions in order. Record base identity, network installation, ownership, user, writable paths, port metadata, health command, and process. Separate build arguments from runtime variables and assess exec versus shell form. Deterministic ordering does not make external downloads deterministic.

Finally inspect history risks. A secret copied in one layer stays unsafe if deleted later. A combined `RUN` cannot make an exposed argument secret. Specific evidence such as “TaskOps copies requirements before source and runs as created UID 1000” is supportable; “secure and reproducible” needs resolved inputs, tests, scans, and runtime policy.

## Practical Exercise

Audit context, base, dependency/application layers, user, check, and exclusions for all Dockerfiles without editing.

## Knowledge Check

1. What sets builder visibility? 2. Why dependency-first? 3. Is `ARG` safe for secrets? 4. Can Docker copy outside context?

<details><summary>Answers</summary>

1. Build context and ignore rules. 2. Cache reuse. 3. No. 4. No.

</details>

## Navigation
- [Back to Docker in CI/CD](../README.md)
- [Previous: Images, Containers, and CI/CD](../01-images-containers-and-cicd/)
- [Next: Layers, Caching, and Multi-Stage Builds](../03-layers-caching-and-multi-stage-builds/)
- [Back to All Learning Materials](../../README.md)
