# SAST, Code Quality, and Secret Scanning

## Three Different Questions About Source

```text
Code-quality linting:
Looks for style, maintainability, or probable correctness problems.

SAST:
Analyzes source or compiled code for security-relevant weaknesses.

Secret scanning:
Looks for credentials, keys, tokens, and secret-like material.
```

All three read source without running it, and all three are routinely confused. A linter flagging an unused variable is not security analysis; a SAST tool flagging `subprocess` with `shell=True` is not a style opinion; and neither will notice an AWS key pasted into a config file — that is the secret scanner's job.

## SAST

**Static Application Security Testing** ranges from **pattern-based analysis** (match known-dangerous constructs) to **data-flow and taint analysis** (track untrusted input from *source* to dangerous *sink* — the technique behind tools like CodeQL and Semgrep's advanced modes). The trade-off is universal: static analysis sees all code paths but understands no runtime context, producing **false positives** (flagged but fine — the input was validated somewhere the tool can't see) and **false negatives** (missed weaknesses — novel patterns, logic flaws). That is why SAST practice needs machinery: **rule severity** tuning, narrow **suppressions** with reasons, **baselines** for legacy code, and a decision per rule class about **blocking** versus **non-blocking**. Results commonly flow as **SARIF** (a standard findings format) into **pull-request annotations** so findings land on the diff, not in a report nobody opens.

**Bandit** — the repository's real SAST tool — is the pattern-based kind for Python. Its honest scope:

- Python source-code security patterns (dangerous calls, hard-coded passwords, weak crypto usage).
- Rule-based detection with known false positives.
- **Not** dependency vulnerability scanning (that is pip-audit's job, next lesson).
- **Not** runtime security testing (that is DAST, lesson 07).

```bash
bandit -r app
```

## Secret Scanning

Secret scanners hunt committed credentials by **known-token patterns** (AWS keys, GitHub tokens have recognizable shapes) and **high-entropy detection** (random-looking strings that could be keys). They can run **pre-commit** (cheapest — the secret never lands), on **pull requests**, and — crucially — against **repository history**, because a secret removed from the latest commit still exists in every prior commit and clone. Gitleaks and TruffleHog are the common open-source tools; a conceptual invocation (no secret scanner exists in this repository):

```bash
gitleaks detect --source .
```

When detection fires, the response is an incident, not a cleanup:

```text
Secret committed
      ↓
Detection
      ↓
Revoke or rotate immediately
      ↓
Remove from current source
      ↓
Assess history and exposure
      ↓
Update affected systems
      ↓
Document incident
```

The order matters: **revocation first**. Deleting the file, force-pushing, even rewriting history does not un-expose the value — forks, clones, and caches keep it. Rotation is the only real remedy; **Git-history cleanup** is hygiene, not response.

## Common Mistakes

- Treating linting as SAST — Ruff finding bugs is not a security review.
- Treating SAST as complete security testing — it cannot see runtime, dependencies, or logic flaws.
- Ignoring findings without ownership.
- Broad suppressions (`# nosec` on whole files, category-wide disables).
- Secret scanner run only after merge, when the secret is already public history.
- Removing a secret from Git but not revoking it.
- Printing scanner reports that themselves contain the detected secrets.
- Scanning generated or vendored files without tuning — noise drowns signal.
- Blocking low-confidence findings without review, training people to bypass.
- No process for false positives, so they get re-triaged forever.

## Existing Repository Evidence

- **Bandit is real and blocking** in three workflows: [TaskOps CI](../../../Projects/1_project/taskops-cicd/.github/workflows/ci.yml) and [CD](../../../Projects/1_project/taskops-cicd/.github/workflows/cd.yml) run `bandit -r app`, as does [KubeOps CI](../../../Projects/2_project/kubeops-gitops/.github/workflows/ci.yml). A failing finding fails the step (non-zero exit), which fails the job and blocks the dependent `docker`/`deploy` jobs.
- **Tuning exists**: [TaskOps pyproject.toml](../../../Projects/1_project/taskops-cicd/pyproject.toml) sets `[tool.bandit] exclude_dirs = ["tests"]` — a scoped, reviewable exclusion (test code legitimately does things production code must not).
- **Version pinning**: TaskOps pins `bandit==1.7.9` in `requirements-dev.txt`, so local and CI scan with the same rules; KubeOps leaves it unpinned — a real drift risk between runs.
- Code-quality linting (Ruff, Black, isort) runs beside Bandit in the same jobs — same mechanism, different category, as covered in [Topic 06](../../06-automated-testing-and-quality/02-formatting-linting-and-static-analysis/).
- **Absent**: CodeQL, Semgrep, SARIF/PR annotations, and any secret-scanning tool (Gitleaks, TruffleHog, detect-secrets) — no pre-commit config exists. GitHub-side secret scanning is a platform setting not visible in source, so no claim is made about it. The repository's defense against committed secrets is currently procedural: `.env.example` placeholders and gitignored real files ([Topic 08](../../08-environments-configuration-and-secrets/04-secrets-management-and-injection/)).

## Practical Exercise

Map every source-analysis check that actually runs in [TaskOps CI](../../../Projects/1_project/taskops-cicd/.github/workflows/ci.yml):

```text
Tool
Input
Detection category (quality / SAST / secrets)
Pipeline stage
Blocking or non-blocking
Report format
Main limitation
```

Cover Ruff, Black, isort, and Bandit. Note explicitly which category has *no* tool (secret scanning) and write two sentences: where in the delivery flow would a secret scanner catch the most, and what would its first-run baseline problem be on an existing repository? Do not run any scanner. Target 20–30 minutes.

## Knowledge Check

1. What distinguishes SAST from code-quality linting?
2. What can taint analysis find that pattern matching cannot?
3. Why must a leaked secret be revoked even after the commit is deleted?
4. What does Bandit not cover, despite being a security tool?
5. What is a baseline for, in SAST adoption?
6. What is this repository's only current defense against committed secrets?

<details>
<summary>View answers</summary>

1. SAST looks for security-relevant weaknesses (injection, dangerous calls, weak crypto); linting looks for style, maintainability, and probable correctness problems.
2. Untrusted data flowing from an input source to a dangerous sink across functions — a relationship, not a single suspicious line.
3. History, clones, forks, and caches retain the value; only rotation/revocation ends the exposure.
4. Dependency vulnerabilities (pip-audit's domain) and runtime behavior (DAST's domain) — it reads only the project's Python source patterns.
5. Recording existing findings so enforcement can start immediately, failing only on newly introduced issues.
6. Procedure: committed `.env.example` placeholders with real files gitignored — no automated secret scanner runs.

</details>

## Navigation

- [Back to DevSecOps and Supply-Chain Security](../README.md)
- [Previous: DevSecOps Fundamentals and Security by Design](../01-devsecops-fundamentals-and-security-by-design/)
- [Next: Dependency, License, and Software Composition Analysis](../03-dependency-license-and-software-composition-analysis/)
- [Back to All Learning Materials](../../README.md)
