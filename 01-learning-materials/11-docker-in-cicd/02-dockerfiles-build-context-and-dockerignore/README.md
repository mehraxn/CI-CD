# Dockerfiles, Build Context, and `.dockerignore`

```text
Build context: files available to the builder.
Dockerfile: instructions selecting files and creating layers.
.dockerignore: exclusions from context.
```

`FROM` selects a base; `WORKDIR`, `COPY`, `RUN`, `ENV`, `ARG`, `USER`, `EXPOSE`, `VOLUME`, `HEALTHCHECK`, `ENTRYPOINT`, and `CMD` shape content and runtime defaults. Exec-form commands handle signals more directly than shell form. `ADD` has extra archive/URL behavior and should be chosen deliberately. `COPY --chown` establishes ownership without later repair layers.

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

The repository has three Dockerfiles and three `.dockerignore` files. TaskOps and KubeOps use slim Python bases, dependency-first copy, non-root users, ports, and health checks; Project 3 is simpler and has no Docker `HEALTHCHECK`.

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
