# Build Lifecycle and Build Tools

## What a Build Is

A build transforms **inputs** — source files, dependency declarations, configuration, toolchain versions — into **outputs**: a package, a bundle, a binary, or a container image. Between input and output sits a lifecycle:

```text
Source files
    ↓
Dependency preparation
    ↓
Compilation or packaging
    ↓
Generated output
    ↓
Verification
    ↓
Release artifact
```

The middle step takes different forms per ecosystem: **compilation** (source to machine code or bytecode), **transpilation** (source to different source, as in TypeScript to JavaScript), **linking** (combining compiled units), **bundling** (merging modules and assets for delivery), **packaging** (arranging files plus metadata into a distributable format), **code generation** (producing source from schemas or templates), **asset generation** (images, stylesheets, translations), and **container-image builds** (assembling filesystem layers plus an image manifest). A Python web service like this repository's projects skips compilation entirely: its "build" is dependency installation plus container-image assembly.

A **clean build** starts from nothing and rebuilds everything; an **incremental build** reuses previous outputs for unchanged parts. Incremental builds are faster and are the default for local development; CI leans toward clean (or carefully cached) builds because stale leftover output is a classic source of "passes locally, fails in CI" — and worse, "passes in CI but shouldn't."

## Build Tools

Build tools coordinate the lifecycle — ordering steps, tracking **build dependencies** (which outputs need which inputs), and rerunning only what changed:

- **Make** — the classic rule-based tool: targets, prerequisites, commands.
- **CMake** — generates build configurations, common in C and C++.
- **Maven** and **Gradle** — JVM lifecycle and dependency tools.
- **npm scripts** — task entries in `package.json` for JavaScript projects.
- **Python packaging tools** — `pip`, `build`, `setuptools`, Poetry, and similar.
- **Go tooling** — `go build` and friends, integrated into the language.
- **Cargo** — Rust's combined build and dependency tool.
- **Docker BuildKit** — the modern engine behind `docker build`, with layer caching and multi-platform support.
- **Bazel** — a large-scale, hermetic-leaning build system for monorepos.

You do not need depth in all of these; you need to recognize which tool owns the lifecycle in any project you open, and where its commands are defined.

## Builds Fail Loudly (or Should)

A build step is a command, and commands report **exit codes**: 0 for success, non-zero for failure. CI treats a non-zero exit as a failed job, so build scripts must not swallow errors — a script that continues past a failed compile produces output that *looks* built. **Build logs** are the primary diagnosis evidence; a good build prints what it is doing and preserves errors near the failure point. **Build verification** (tests, smoke checks against the output) turns "it produced a file" into "it produced a working thing." Finally, **build cleanup** — removing temporary and stale output — protects the next build, especially on reused machines.

## Local Builds vs. CI Builds

The same project builds in two places: a developer's machine and a CI runner. They should run **the same commands**; divergence breeds "works on my machine." A CI build must not depend on:

- Undocumented local tools.
- Files outside the repository.
- Manual configuration steps.
- Uncommitted local changes.
- A developer's personal environment.
- Hidden credentials.
- Previously generated output that cannot be recreated.

A conceptual minimal build-and-verify script (not necessarily this repository's exact commands):

```bash
set -e

python -m pip install -r requirements.txt
python -m pytest
python -m build
```

`set -e` makes the script exit on the first failing command — a small line that prevents the "kept going after failure" class of broken builds. **Build isolation** (fresh virtual environments, containers, or clean runners) and **environment consistency** (same tool versions locally and in CI) close most of the remaining gap.

## Common Mistakes

- "Works on my machine" builds relying on undocumented local state.
- Undocumented build prerequisites discovered only when a new person joins.
- Different commands locally and in CI, so local green means nothing.
- Stale output left in the workspace corrupting the next build.
- Building differently for each environment instead of building once.
- Ignoring warnings until one becomes an outage.
- Building production output multiple times and hoping the copies match.
- Mixing build and deployment responsibilities in one opaque script.

## Existing Workflow Evidence

- The [TaskOps Makefile](../../../Projects/1_project/taskops-cicd/Makefile) is the project's build-tool layer: `make install`, `make test`, `make lint`, `make check` (which chains lint, format-check, test, security, and audit), `make docker-build`, and `make clean` (explicit stale-output cleanup). Its targets run essentially the same commands as the [CI workflow](../../../Projects/1_project/taskops-cicd/.github/workflows/ci.yml) — the local/CI consistency this lesson recommends.
- The [TaskOps Dockerfile](../../../Projects/1_project/taskops-cicd/Dockerfile) is the container-build lifecycle in miniature: dependency layer first, application code after, then a `HEALTHCHECK` as built-in verification.
- [KubeOps](../../../Projects/2_project/kubeops-gitops/Makefile) follows the same Makefile-plus-Dockerfile pattern; [Project 3](../../../Projects/3_project/app/Dockerfile) shows the minimal version.
- No project here compiles code; the repository does not demonstrate Maven, Gradle, Bazel, or compiled-language lifecycles — those remain conceptual.

## Practical Exercise

Create a build map for TaskOps (Project 1) without changing anything:

```text
Inputs
Dependency files
Build command
Test command
Output
Container build
CI workflow
```

Fill each line with the exact file paths and commands you find in the Makefile, Dockerfile, and CI workflow. Note one place where the local command and the CI command match, and any place they differ. Target 20–30 minutes.

## Knowledge Check

1. What are the inputs and outputs of a build?
2. Why do CI systems prefer clean or carefully cached builds over ad-hoc incremental ones?
3. What does a non-zero exit code mean to CI, and why must build scripts not swallow it?
4. Why should local and CI builds run the same commands?
5. Does a Python web service have a build even without compilation?

<details>
<summary>View answers</summary>

1. Inputs: source files, dependency declarations, configuration, and toolchain versions. Outputs: a package, bundle, binary, or container image, plus logs and reports.
2. Leftover state from previous builds can hide failures or corrupt output; a clean start makes results depend only on declared inputs.
3. Non-zero means failure and fails the job; a script that continues past an error can produce output that looks built but is broken.
4. So a local success predicts a CI success; divergent commands make local verification meaningless and hide prerequisites.
5. Yes — dependency installation, packaging or assembly, container-image creation, and verification are all build steps; compilation is just one possible middle step.

</details>

## Navigation

- [Back to Builds, Dependencies, and Caching](../README.md)
- [Next: Dependency Management and Lockfiles](../02-dependency-management-and-lockfiles/)
- [Back to All Learning Materials](../../README.md)
