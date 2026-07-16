# Cross-Platform and Multi-Architecture Builds

## Two Different Axes

Software runs on combinations of **operating system** (Linux, Windows, macOS) and **CPU architecture** (`amd64` — the common x86-64 servers; `arm64` — Apple Silicon, AWS Graviton, Raspberry Pi). A **cross-platform build** targets multiple operating systems; **cross-compilation** produces output for an architecture different from the build machine's. Both multiply the build:

```text
Source code
├── Linux amd64 build
├── Linux arm64 build
├── Windows build
└── macOS build
```

A **native build** runs on the target architecture itself (fast, faithful). An **emulated build** uses translation — commonly **QEMU** — to build for a foreign architecture on available hardware (convenient, slower, and subtly different from real hardware). In CI, a **build matrix** or per-platform **runner selection** assigns each target to an appropriate machine; expect **build duration** to grow with each added platform, and keep **caches separated by OS and architecture** — a cache of `amd64` binaries restored onto an `arm64` build is a bug generator.

## Multi-Platform Container Images

A multi-platform image is really several images plus an **image manifest** (a manifest list) that maps each platform to its variant; `docker pull` transparently selects the right one. Conceptually, with Buildx:

```yaml
- name: Set up QEMU
  uses: docker/setup-qemu-action@v3

- name: Set up Docker Buildx
  uses: docker/setup-buildx-action@v3

- name: Build multi-platform image
  uses: docker/build-push-action@v6
  with:
    context: .
    platforms: linux/amd64,linux/arm64
    push: false
```

This example is conceptual — no repository workflow builds multi-platform images. And a warning that survives every toolchain: **building successfully for an architecture does not prove correct runtime behavior there.** Emulated builds especially need **architecture-specific tests** on real (or at least representative) hardware; libraries with native extensions, atomics, and performance characteristics all differ.

## Portability Traps

Code and pipelines that only ever ran on one OS accumulate silent assumptions:

- **Path separators** — `/` versus `\`, and hard-coded absolute paths.
- **Shell differences** — bash scripts fail on Windows runners unless a shell is specified; PowerShell quoting differs.
- **File permissions and executable bits** — Windows filesystems do not track the Unix executable bit; a script committed from Windows may not be executable on Linux.
- **Case sensitivity** — `Config.py` and `config.py` are one file on Windows/macOS defaults, two on Linux.
- **Line endings** — CRLF versus LF breaks shell scripts and checksums (this repository visibly deals with LF/CRLF conversion warnings on Windows).
- **Platform-specific dependencies** — packages with compiled components need per-platform wheels or a compiler present.

A **platform support policy** keeps this honest: name the OS/architecture combinations you actually support and test, and refuse the rest deliberately rather than accidentally.

## Common Mistakes

- Assuming Linux behavior matches Windows.
- Sharing incompatible caches across OS or architecture.
- Ignoring line-ending differences until a script breaks.
- Building with emulation but never testing natively.
- Publishing architecture labels or manifests incorrectly.
- Supporting too many platforms without a real requirement.
- Forgetting architecture-specific dependencies.

## Existing Repository Evidence

The repository is deliberately single-platform: every workflow job runs on `runs-on: ubuntu-latest` (which GitHub currently provisions as amd64 for standard runners), and every Docker build — [TaskOps CI](../../../Projects/1_project/taskops-cicd/.github/workflows/ci.yml), [TaskOps CD](../../../Projects/1_project/taskops-cicd/.github/workflows/cd.yml), [KubeOps image release](../../../Projects/2_project/kubeops-gitops/.github/workflows/image-release.yml) — builds for the runner's native platform with no `platforms:` input, no QEMU setup, and no manifest lists. The [TaskOps Makefile](../../../Projects/1_project/taskops-cicd/Makefile) does contain one real cross-platform accommodation: it switches the virtualenv path between `.venv/bin` and `.venv/Scripts` when `$(OS)` is `Windows_NT`, acknowledging Windows developers. Multi-architecture builds are not currently demonstrated and may be added in a later enhancement phase.

## Practical Exercise

Document the repository's platform assumptions versus explicit support. Answer with file references:

1. Which OS and architecture do the CI builds actually run on?
2. Which platform will the published KubeOps image run on, and where is that decided (or defaulted)?
3. Find the one explicit cross-platform accommodation in the TaskOps Makefile.
4. List two things that would need to change to publish an `arm64` variant of the TaskOps image — and what testing gap would remain even after the build succeeded.

Do not modify anything. Target 15–25 minutes.

## Knowledge Check

1. What is the difference between cross-platform and cross-compilation?
2. What does a multi-platform image manifest do?
3. Why is a successful emulated build not sufficient evidence of correctness?
4. Why must caches be separated by architecture?
5. Name three portability traps between Windows and Linux.

<details>
<summary>View answers</summary>

1. Cross-platform targets multiple operating systems; cross-compilation produces output for a CPU architecture different from the build machine's.
2. It maps each supported platform to its image variant so clients automatically pull the right one from a single reference.
3. Emulation differs subtly from real hardware, and building proves compilability, not runtime behavior — architecture-specific tests are still needed.
4. Cached binaries are architecture-specific; restoring another architecture's cache produces incompatible content and confusing failures.
5. Path separators, shell availability and syntax, executable bits/permissions, filesystem case sensitivity, and CRLF/LF line endings (any three).

</details>

## Navigation

- [Back to Builds, Dependencies, and Caching](../README.md)
- [Previous: Build Metadata and Version Injection](../05-build-metadata-and-version-injection/)
- [Back to All Learning Materials](../../README.md)
