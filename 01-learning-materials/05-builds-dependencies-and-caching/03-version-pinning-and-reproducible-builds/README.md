# Version Pinning and Reproducible Builds

## Pinning Is Bigger Than Dependencies

The previous lesson pinned packages. A build has more moving inputs, and each can be pinned or left floating:

- **Runtime versions** — `python-version: "3.12"` rather than "whatever is installed."
- **Toolchain versions** — compilers, linters, packaging tools.
- **Operating-system images** — `runs-on: ubuntu-latest` floats; a dated image label pins.
- **Action versions** — `uses: actions/checkout@v4` (tag) versus a commit SHA.
- **Base images** — `FROM python:3.12-slim` (tag) versus a digest.

Tags are readable but usually **mutable**: the publisher can move `v4` or rebuild `python:3.12-slim` tomorrow. **Immutable references** — commit SHAs for actions, digests for images, **checksums** for downloads — guarantee the bytes cannot change underneath you. Tags improve readability and receive maintenance updates; digests maximize immutability and maintenance burden. Neither is universally right, and no project must rush to digest-pin everything — the point is to *choose knowingly*.

## Four Related Words

```text
Repeatable build:
The same process can be run again successfully under the expected conditions.

Reproducible build:
Independent builds from the same inputs produce equivalent output.

Deterministic build:
The build process consistently produces the same output for the same inputs.

Hermetic build:
The build uses explicitly controlled inputs and avoids undeclared external dependencies.
```

These overlap but are not identical: a build can be repeatable (it runs again fine) without being reproducible (the second run bundles newer transitive packages). Determinism is about the process introducing no variation of its own; hermeticity is about closing the doors through which variation enters. The practical recipe:

```text
Source revision
+ exact dependency graph
+ exact toolchain
+ controlled environment
+ declared build command
= more reproducible output
```

## Where Variation Sneaks In

Even with pinned inputs, builds diverge through: **timestamps** embedded in outputs, **randomness** (unseeded generators, hash ordering), **locale and time zones** changing formatted text, **file ordering** differences between filesystems, uncontrolled **network access** fetching "latest" anything, **generated files** with volatile content, **compiler versions** that differ silently, **environment variables** leaking into outputs, absolute **build paths** baked into binaries, and building from a **dirty working tree** (uncommitted changes) so the output matches no commit at all. **Dependency mirrors** and archived toolchains matter for the long game: **rebuilding an old release** requires the old inputs to still exist somewhere.

Containers help — a Dockerfile declares much of the environment — but a container build is *not automatically reproducible*: `FROM python:3.12-slim` floats with rebuilds, `RUN pip install` without pins fetches today's packages, and `apt-get update` fetches today's index.

## Trade-offs

Pinning trades **automatic updates for stability**. Fully pinned builds don't absorb security patches until someone updates the pins — so pinning without a maintenance habit converts "unpredictable builds" into "predictably vulnerable builds." Teams manage the burden with automated-update tools (Renovate, Dependabot) that open pull requests per update, keeping changes small, reviewed, and CI-verified. The spectrum, honestly stated:

- Floating references: least maintenance, least predictability.
- Tag pinning: readable, mostly stable, trusts the publisher.
- Commit/digest pinning: strongest immutability, most maintenance.

**Build provenance** — attested records of what inputs and process produced an artifact — extends this story into supply-chain security territory, covered later in Topic 14.

## Common Mistakes

- Using `latest` as the only release reference.
- Depending on floating tool versions that change under the pipeline.
- Rebuilding the same release differently in each environment.
- Generating versions manually and inconsistently.
- Embedding uncontrolled timestamps in outputs.
- Assuming a container automatically guarantees reproducibility.
- Never documenting the build environment.
- Pinning forever without security updates.

## Existing Repository Evidence

- Actions are **tag-pinned** everywhere: `actions/checkout@v4`, `actions/setup-python@v5`, `docker/build-push-action@v6` in [TaskOps CI](../../../Projects/1_project/taskops-cicd/.github/workflows/ci.yml), with `aquasecurity/trivy-action@0.28.0` pinned to an exact release tag — a deliberate step up in precision. No workflow uses commit-SHA pinning.
- Runtime versions are pinned in CI (`python-version: "3.12"`) and in images: [TaskOps](../../../Projects/1_project/taskops-cicd/Dockerfile) and [KubeOps](../../../Projects/2_project/kubeops-gitops/Dockerfile) use `FROM python:3.12-slim`, [Project 3](../../../Projects/3_project/app/Dockerfile) uses `FROM python:3.13-slim` — all tag-pinned, none digest-pinned.
- Dependency pinning varies by project exactly as the previous lesson described, so TaskOps images rebuild much more consistently than KubeOps images.
- `runs-on: ubuntu-latest` floats in all workflows — normal practice, but worth naming as a floating input.
- The repository does not demonstrate digest pinning, hashed requirements, Renovate/Dependabot automation, or provenance attestations; these remain conceptual and may be added in a later enhancement phase.

## Practical Exercise

Audit version references in TaskOps (Project 1). Build a two-column list — **pinned** vs. **floating** — covering: base image tag, each action reference in both workflows, the Python version in CI, each package in both requirements files, and the runner label. For each floating entry, note what could change without any commit to the repository. Do not modify anything. Target 20–30 minutes.

## Knowledge Check

1. What is the difference between a repeatable and a reproducible build?
2. Why is a Docker build not automatically reproducible?
3. What does tag pinning trust that digest pinning does not?
4. Name three sources of variation besides dependency versions.
5. What is the danger of pinning everything and never updating?
6. Why does building from a dirty working tree undermine traceability?

<details>
<summary>View answers</summary>

1. Repeatable means the process can run again successfully; reproducible means independent builds from the same inputs produce equivalent output.
2. Its base-image tag can be rebuilt, and unpinned package installs or index updates fetch whatever is current at build time.
3. The publisher — tags are mutable references the publisher can move or rebuild; a digest identifies exact bytes.
4. Timestamps, randomness or hash ordering, locale/time zone, file ordering, build paths, environment variables, network access during the build.
5. Security patches never arrive; the build becomes predictably vulnerable until pins are deliberately maintained.
6. The output corresponds to no commit, so no one can check out the exact source that produced it.

</details>

## Navigation

- [Back to Builds, Dependencies, and Caching](../README.md)
- [Previous: Dependency Management and Lockfiles](../02-dependency-management-and-lockfiles/)
- [Next: Build Caching](../04-build-caching/)
- [Back to All Learning Materials](../../README.md)
