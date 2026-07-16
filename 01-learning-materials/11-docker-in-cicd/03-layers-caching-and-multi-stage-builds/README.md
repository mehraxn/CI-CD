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

## Cache Mechanics and Trust

The builder evaluates each instruction with its relevant inputs. If an early result changes, later dependent results are normally rebuilt. Copying dependency declarations before source code is useful because dependencies often change less frequently than the application. A broad `COPY . .` before installation makes every source, documentation, or generated-file change invalidate that expensive layer. Base-image movement, build arguments, command text, and unpinned network downloads can also change results.

BuildKit is the modern build engine behind Buildx. Cache import (`cache-from`) makes earlier results available; cache export (`cache-to`) saves new results. Inline cache metadata can travel with an image, while a remote backend such as GitHub Actions cache stores results separately. A cache is an accelerator, not a release artifact or a security boundary. It can be deleted, scoped incorrectly, or populated by untrusted work. Architecture-specific output should not be reused blindly across platforms, and sensitive material must never be written into a cacheable layer.

The TaskOps [CI workflow](../../../Projects/1_project/taskops-cicd/.github/workflows/ci.yml) and [CD workflow](../../../Projects/1_project/taskops-cicd/.github/workflows/cd.yml) use `docker/setup-buildx-action@v3`, `cache-from: type=gha`, and `cache-to: type=gha,mode=max`. This is the repository's real remote-cache example. KubeOps sets up Buildx for image release but does not configure the GHA backend; its CI invokes `docker build` directly.

## Multi-Stage Design

The example above is conceptual. `AS builder` names a stage that creates wheels. `AS runtime` starts a fresh stage, and `COPY --from=builder` selects only wheel output. Compilers and build dependencies stay out of the runtime image, reducing size and attack surface. The separation also makes the build/runtime boundary reviewable.

Costs remain. More stages mean more Dockerfile logic, duplicated setup, and harder diagnosis. Copying an entire builder directory can still transfer source, caches, development packages, or secrets. A distroless image supplies only a narrow runtime userspace, while `scratch` begins empty; both may omit shells, certificates, timezone files, and diagnostic tools. The smallest image is not automatically the safest or easiest to operate. Measure vulnerabilities, patching, startup, transfer size, and supportability.

## Real Layer Map

TaskOps begins with `python:3.12-slim`. Environment metadata and `/app` follow. `requirements.txt` is copied before pip installation, so a normal source edit does not invalidate dependencies. User and `/data` setup come next. Application files and `wsgi.py` are copied late, followed by runtime metadata: `USER`, `VOLUME`, `EXPOSE`, `HEALTHCHECK`, and `CMD`. A requirements change invalidates dependency installation and everything after it; an application edit invalidates only the later copy and configuration results.

KubeOps uses the same dependency-first principle. Project 3 copies `requirements.txt`, installs it, then copies `main.py`. None of the three Dockerfiles contains `FROM ... AS ...` or `COPY --from`; multi-stage builds are not implemented here.

Efficient ordering does not itself make a build reproducible. Moving base tags and package indexes may still produce different bytes, and caches may disappear. Reproducibility needs controlled inputs, pinned dependencies where appropriate, and recorded output identity. Avoid cache poisoning, secrets in layers, incompatible cross-architecture cache scopes, build tools retained without purpose, and elaborate stage graphs without a clear boundary.

## Cache and Stage Review

For each instruction, record direct inputs and dependent steps. Ask what occurs when source, dependency files, base tags, arguments, or architecture change. CI cache scopes should separate repositories, platforms, and trust levels; untrusted contributors should not seed trusted releases without safeguards.

For multi-stage design, name the artifact crossing the boundary—wheel, binary, or static bundle—and list runtime libraries it needs and build tools it does not. Copy only selected output, test the final stage, and compare size, vulnerabilities, startup, patching, and diagnosis. A stage is useful when it creates a real boundary.

Reproducibility needs resolved base/dependency identities and output digests, not cache hits. Warm and cold builds should be equivalent; cache loss should slow a build, not alter correctness. Trace an unexpected miss to the earliest changed instruction. Trace excess image size to the introducing layer. Missing runtime files usually mean selected output or shared libraries were omitted.

## Design Trade-Off Record

Before changing stages or cache, record the slow steps, layer sizes, vulnerability sources, required platforms, and operational debugging needs. A proposed optimization should name the expected improvement and a verification method. Otherwise additional stages can increase maintenance without reducing runtime content.

Treat cache keys, scopes, and writers as supply-chain configuration. Release jobs should consume only cache appropriate to their trust level. Network package installation remains a changing input even when the Dockerfile is unchanged, so dependency locking and artifact repositories complement caching. After a builder update, compare image behavior and digest rather than assuming cached output remains valid.

Multi-stage tests should include missing shared libraries, certificate access, timezone behavior, signal handling, and non-root file access. The runtime stage must contain everything required—but nothing merely convenient from compilation. This balance is more useful than a size target alone.

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
