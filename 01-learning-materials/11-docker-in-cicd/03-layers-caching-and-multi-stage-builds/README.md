# Layers, Caching, and Multi-Stage Builds

Instruction order controls cache invalidation:

```text
Dependency file copied → dependencies installed → source copied → application packaged
```

Source changes then retain the expensive dependency layer. BuildKit can import/export remote cache; TaskOps workflows use `cache-from: type=gha` and `cache-to: type=gha,mode=max`. Caches are accelerators, not trusted releases; scope them by architecture and inputs and consider poisoning or secret leakage.

A conceptual multi-stage build uses named builder/runtime stages and `COPY --from` to keep compilers and development dependencies out of production. This reduces size and attack surface but adds complexity and may reduce debuggability. Distroless/scratch images are smaller yet operationally constrained.

```dockerfile
FROM python:3.12-slim AS builder
WORKDIR /build
COPY requirements.txt .
RUN python -m pip wheel --wheel-dir /wheels -r requirements.txt

FROM python:3.12-slim AS runtime
WORKDIR /app
COPY --from=builder /wheels /wheels
RUN python -m pip install --no-cache-dir /wheels/*
COPY app/ ./app/
USER 1000
CMD ["python", "-m", "app"]
```

No repository Dockerfile is multi-stage. TaskOps/KubeOps do use dependency-first ordering; only TaskOps workflows demonstrate GHA BuildKit cache.

## Practical Exercise

Map TaskOps instructions to layers and invalidation triggers. Identify which inputs invalidate dependencies and source.

## Knowledge Check

1. Why does order matter? 2. What does multi-stage omit? 3. Is cache permanent? 4. Is smallest always best?

<details><summary>Answers</summary>

1. Earlier changes invalidate later layers. 2. Build-only tools. 3. No. 4. No; operability matters.

</details>

## Navigation
- [Back to Docker in CI/CD](../README.md)
- [Previous: Dockerfiles, Build Context, and dockerignore](../02-dockerfiles-build-context-and-dockerignore/)
- [Next: Image Tagging, Versioning, and Metadata](../04-image-tagging-versioning-and-metadata/)
- [Back to All Learning Materials](../../README.md)
