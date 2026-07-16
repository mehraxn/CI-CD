# Build Caching

## Why Caching Exists

CI runners usually start fresh, so every run re-downloads dependencies and rebuilds unchanged layers. Caching keeps that repeated work: **dependency caches** (downloaded packages), **compiler caches** (object files, e.g. ccache), **build-output caches** (task results, as in Gradle or Bazel), and **Docker layer caches** (image layers reused when their inputs are unchanged, managed by BuildKit). Caches can be **local** to a runner, **remote** in a cache service, or **shared** across branches and jobs.

The defining property that separates a cache from everything else:

```text
Cache:
Reusable data that may be discarded and recreated.

Artifact:
A preserved output that may be required by another job, release, or audit process.
```

A pipeline must succeed (slower) with every cache empty. If losing the data breaks correctness, it is an artifact — or workspace state that should have been rebuilt — not a cache.

## Keys, Hits, and Invalidation

A **cache key** names an entry; the run **hits** if the key matches an existing entry and **misses** otherwise. **Cache invalidation** happens by *changing the key* — which is why keys must encode every input that affects compatibility:

```yaml
- name: Restore Python dependency cache
  uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements*.txt') }}
    restore-keys: |
      ${{ runner.os }}-pip-
```

Reading the parts:

- **`path`** — what gets saved and restored (pip's download cache).
- **`key`** — exact identity: OS plus a **hash of the dependency files**. Change a requirements file, the hash changes, the old cache no longer matches — invalidation by construction.
- **`restore-keys`** — a prefix fallback: on an exact miss, restore the newest partial match (older but mostly useful packages), then let the install fill the gap.
- The **OS is included** because cached binary packages are OS-specific; the same logic argues for including runtime version and architecture when they vary (branch-, OS-, and version-scoped caches).
- Stale-cache behavior must be considered: a `restore-keys` hit gives you an *old* cache — fine for pip downloads, dangerous for anything the build treats as authoritative.

This is a conceptual example — the repository does not use `actions/cache` directly. It uses the two other real mechanisms:

**Automatic caching via setup actions:**

```yaml
- uses: actions/setup-python@v5
  with:
    python-version: "3.12"
    cache: pip
```

**Docker layer caching via BuildKit and the GitHub Actions cache backend:**

```yaml
- name: Build image
  uses: docker/build-push-action@v6
  with:
    context: .
    push: false
    tags: example:test
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

`cache-from` restores previously built layers; `cache-to` saves them; `mode=max` caches intermediate layers too, not just the final ones.

## Cache Operations Concerns

Caches have life-cycle costs: **retention** limits (platforms evict old or large entries — GitHub evicts least-recently-used when a repository exceeds its quota), **size** (huge caches can take longer to restore than they save — measure), **eviction** (never assume presence), **warm-up** (the first run after a key change is slow by design), and **observability** — check hit rates in logs before celebrating a "fast pipeline," because a 100%-miss cache is pure overhead. Do not confuse caching with **workspace persistence**: jobs on fresh runners share nothing except what caches and artifacts explicitly move.

## Cache Security

A cache is executable input to your build, so treat it as an attack surface:

- **Cache poisoning** — if untrusted code (for example a fork PR) can write a cache that trusted runs later restore, the attacker's content executes in a trusted context. Platforms scope caches by branch to limit this; overly broad keys and shared scopes widen it.
- Executable content in caches (packages, compiled objects) makes poisoning consequential.
- **Secrets must never be written into cached paths** — caches are far less protected than secret stores.
- Overly broad keys restore incompatible or stale entries; incompatible cached dependencies produce baffling failures (the wrong-OS wheel problem).

## Common Mistakes

- A cache key that never changes — permanently stale content.
- A cache key that changes every run — permanent misses, pure overhead.
- Caching build output that should be an artifact.
- Assuming a cache is always available.
- Making the pipeline fail when the cache is missing.
- Caching directories that contain sensitive data.
- Using the same cache across incompatible platforms or runtime versions.
- Measuring pipeline speed without checking cache hit rates.

## Existing Workflow Evidence

- [TaskOps CI](../../../Projects/1_project/taskops-cicd/.github/workflows/ci.yml) demonstrates both real mechanisms: `actions/setup-python@v5` with `cache: pip` and `cache-dependency-path: requirements-dev.txt` (the dependency file *is* the key input), and `docker/build-push-action@v6` with `cache-from: type=gha` / `cache-to: type=gha,mode=max` for BuildKit layer caching.
- [TaskOps CD](../../../Projects/1_project/taskops-cicd/.github/workflows/cd.yml) uses the same two mechanisms, so CI and CD builds share warm layer caches.
- The [TaskOps Dockerfile](../../../Projects/1_project/taskops-cicd/Dockerfile) is deliberately ordered for layer caching — its comment says it: dependencies are copied and installed *before* application code, so code edits invalidate only the cheap later layers. [KubeOps](../../../Projects/2_project/kubeops-gitops/Dockerfile) documents the same pattern.
- [KubeOps CI](../../../Projects/2_project/kubeops-gitops/.github/workflows/ci.yml) uses `cache: pip` but builds its image with plain `docker build` — no layer cache backend, a real contrast worth noticing.
- Explicit `actions/cache` usage is not currently demonstrated.

## Practical Exercise

Analyze the real caching in TaskOps CI. For each of the two mechanisms (pip cache, BuildKit layer cache), record:

```text
Cached path
Cache backend
Cache key inputs
Invalidation trigger
Security considerations
Expected benefit
```

For the pip cache, identify exactly which file's change invalidates it. For the layer cache, use the Dockerfile ordering to state which change (requirements vs. app code) invalidates which layers. Do not modify anything. Target 20–30 minutes.

## Knowledge Check

1. What is the essential difference between a cache and an artifact?
2. How is a cache invalidated in key-based systems?
3. Why does the example key include the operating system?
4. What is cache poisoning?
5. Why does the TaskOps Dockerfile copy `requirements.txt` before the application code?
6. Why check hit rates instead of just timing the pipeline?

<details>
<summary>View answers</summary>

1. A cache may be discarded and recreated without breaking anything; an artifact is a preserved output that other jobs, releases, or audits require.
2. By changing the key — keys hash or encode the inputs, so changed inputs produce a new key and the old entry no longer matches.
3. Cached packages contain OS-specific binaries; restoring another OS's cache produces incompatible content.
4. Untrusted code writing cache entries that trusted runs later restore and execute, injecting attacker content into a trusted context.
5. So the expensive dependency-install layer is reused until requirements change; code edits invalidate only the cheap final layers.
6. A pipeline can look "cached" while missing every time; only hit rates show whether the cache does anything.

</details>

## Navigation

- [Back to Builds, Dependencies, and Caching](../README.md)
- [Previous: Version Pinning and Reproducible Builds](../03-version-pinning-and-reproducible-builds/)
- [Next: Build Metadata and Version Injection](../05-build-metadata-and-version-injection/)
- [Back to All Learning Materials](../../README.md)
