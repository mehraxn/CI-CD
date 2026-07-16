# Dependency Management and Lockfiles

## Dependencies

A **dependency** is code your project uses but does not contain. **Direct dependencies** are the ones you declare; **transitive dependencies** are what your dependencies need — usually the far larger group, and just as capable of breaking or compromising a build. Dependencies also split by purpose: **runtime dependencies** ship with the application; **development dependencies** (test frameworks, linters, formatters) are needed to build and verify it but not to run it; **optional dependencies** enable extra features (the `uvicorn[standard]` extra syntax in Python is an example).

A **dependency manager** (pip, npm, Maven, Cargo, Go modules) resolves declarations against a **package repository / index** (PyPI, npm registry) into a concrete **dependency graph**, downloads the packages, and installs them. **Dependency resolution** is where declared flexibility becomes an exact answer — and where two runs can get *different* answers if the declarations allow it.

## Manifest, Lockfile, Constraints

```text
Manifest:
Describes requested dependencies and allowed versions.

Lockfile:
Records exact resolved versions and often integrity information.

Constraints file:
Restricts versions without necessarily declaring the complete dependency set.
```

A manifest with **version ranges** (semantic-version aware):

```text
requests>=2.31,<3
pytest>=8,<9
```

The same dependencies with **exact versions**:

```text
requests==2.32.3
pytest==8.3.5
```

A JavaScript manifest using a caret range:

```json
{
  "dependencies": {
    "express": "^4.21.0"
  }
}
```

Note the crucial gap: even the exactly pinned Python list above pins only *direct* dependencies. A true lockfile (`package-lock.json`, `poetry.lock`, `Cargo.lock`, `go.sum`) records the **entire resolved graph** — every transitive package — and usually **checksums / integrity hashes** so a tampered package fails installation. A plain `requirements.txt` with `==` pins is a *pinned list*, not automatically a complete lockfile; transitive versions can still drift between installs. (Python teams that want full locking generate hashed requirements with tools like pip-tools, or use Poetry/uv lockfiles.)

## Installation in CI

Conceptually: `pip install -r requirements.txt` installs whatever the file resolves to right now. `npm install` may update the lockfile to satisfy the manifest; **`npm ci`** installs *exactly* what the lockfile says and fails if manifest and lockfile disagree — which is why clean, lockfile-aware installation (`npm ci` and its equivalents) is preferred in CI: the build gets the reviewed graph, not today's resolution.

| Approach | Strength | Risk |
|----------|----------|------|
| Wide version ranges | Easier updates | Build may change unexpectedly |
| Exact pinning | More predictable resolution | Updates require deliberate maintenance |
| Lockfile | Exact dependency graph | Must remain current and reviewed |
| Vendoring | Strong control | Larger repository and maintenance cost |

**Vendoring** — copying dependency source into your repository — trades registry trust for repository size and update labor; it survives registry outages and deletions but must be maintained by hand.

## Dependency Risk

Dependencies are the largest untrusted input to most builds:

- **Dependency confusion** — an attacker publishes a public package with the same name as your internal one, and a misconfigured resolver prefers it.
- **Typosquatting** — malicious packages named one keystroke from popular ones.
- **Abandoned packages** — no maintainer means no security fixes.
- **License concerns** — a dependency's license binds your distribution.
- **Private dependencies** need **authenticated registry access** — with credentials handled as secrets, never committed.
- **Vulnerability scanning** (this repository uses `pip-audit` for Python dependencies and Trivy for image contents) catches *known* vulnerabilities; a successful install proves availability, not safety.

**Updates** are the counterweight to pinning: **dependency conflicts** (two packages demanding incompatible versions of a third) and vulnerable versions both get fixed by updating — deliberately, one reviewed change at a time, not by blanket-updating everything the night before a release.

## Common Mistakes

- Deleting lockfiles casually to "fix" resolution errors.
- Using one dependency file for incompatible purposes (production install pulling in dev tools).
- Installing development tools in production images unnecessarily.
- Ignoring transitive dependencies because "we didn't choose them."
- Depending on untrusted or unnecessary package sources.
- Never updating pinned packages — pinned vulnerabilities are still vulnerabilities.
- Blindly updating all packages together, making regressions undiagnosable.
- Committing credentials for private registries.
- Assuming a successful install means the dependencies are secure.

## Existing Repository Evidence

The three projects deliberately sit at three points on the spectrum:

- [TaskOps requirements.txt](../../../Projects/1_project/taskops-cicd/requirements.txt) — **exact pins** (`Flask==3.1.3`, `gunicorn==23.0.0`) of direct runtime dependencies; [requirements-dev.txt](../../../Projects/1_project/taskops-cicd/requirements-dev.txt) includes it via `-r requirements.txt` and pins the dev tools (`pytest==8.2.2`, `ruff==0.5.6`, …) — a clean runtime/development split, and a pinned list rather than a full lockfile (no transitive pins, no hashes).
- [KubeOps requirements.txt](../../../Projects/2_project/kubeops-gitops/requirements.txt) — **unpinned** names (`fastapi`, `uvicorn[standard]`, `pydantic`): every install takes the latest resolution, maximally convenient and minimally predictable.
- [Project 3 requirements.txt](../../../Projects/3_project/app/requirements.txt) — **ranges** (`Flask>=3.0,<4.0`): a manifest style that accepts patch and minor updates while excluding the next major version.

No project currently uses a full lockfile (Poetry, pip-tools hashes, npm) or a constraints file. TaskOps CI runs [`pip-audit -r requirements.txt`](../../../Projects/1_project/taskops-cicd/.github/workflows/ci.yml) as a dependency-vulnerability gate.

## Practical Exercise

Classify every dependency file in the repository:

```text
Manifest
Pinned list
Lockfile
Constraints file
Unknown or mixed purpose
```

Cover both TaskOps files, both KubeOps files, and Project 3's file. For each, note: does it pin direct dependencies? Transitive ones? Does it carry integrity hashes? Then write one sentence per project predicting how its style behaves when a dependency releases a breaking version. Do not modify any file. Target 20–30 minutes.

## Knowledge Check

1. What is the difference between a direct and a transitive dependency?
2. Why is an exactly pinned `requirements.txt` still not a complete lockfile?
3. What does `npm ci` do differently from `npm install`, and why does CI prefer it?
4. What is dependency confusion?
5. Which repository project has the least predictable installs, and why?
6. Does a successful dependency install prove the dependencies are safe?

<details>
<summary>View answers</summary>

1. Direct dependencies are declared by your project; transitive dependencies are required by your dependencies and are resolved automatically.
2. It pins only the packages listed — the transitive graph can still resolve differently between installs, and there are no integrity hashes.
3. `npm ci` installs exactly the lockfile's graph and fails on manifest/lockfile mismatch, giving CI the reviewed resolution instead of a fresh one.
4. An attacker publishes a public package matching an internal package name, hoping resolvers fetch the public one.
5. KubeOps — its `requirements.txt` is unpinned, so every install takes whatever versions resolve that day.
6. No — installation proves availability and compatibility of the resolution, not the absence of vulnerabilities or malicious code; scanning and review address safety.

</details>

## Navigation

- [Back to Builds, Dependencies, and Caching](../README.md)
- [Previous: Build Lifecycle and Build Tools](../01-build-lifecycle-and-build-tools/)
- [Next: Version Pinning and Reproducible Builds](../03-version-pinning-and-reproducible-builds/)
- [Back to All Learning Materials](../../README.md)
