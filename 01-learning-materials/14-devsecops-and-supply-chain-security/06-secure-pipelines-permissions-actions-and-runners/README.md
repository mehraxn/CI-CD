# Secure Pipelines, Permissions, Actions, and Runners

## The Pipeline Is an Attack Surface

A CI/CD pipeline executes code with credentials. That single sentence is the **pipeline threat model**:

```text
Untrusted source change
        ↓
Pipeline executes code
        ↓
Runner permissions and secrets determine impact
```

Whoever can make the pipeline run their code — a contributor, a fork, a compromised dependency, a malicious action — gets everything the job can reach. Pipeline security is therefore about shrinking "everything the job can reach."

## Permissions: The Blast-Radius Dial

The workflow's `GITHUB_TOKEN` permissions set the ceiling:

```yaml
permissions:
  contents: read
```

A publishing workflow adds exactly what publishing needs:

```yaml
permissions:
  contents: read
  packages: write
```

The rules: default to read-only, add **write** scopes (`packages`, `contents`, `pull-requests`) only where required, prefer **job-level** grants over workflow-wide ones, and treat `id-token: write` (OIDC) as a privilege — any job holding it can request cloud credentials the trust policy allows. **Secrets** follow the same shape: repository and environment secrets should reach only the jobs that need them, and reusable workflows should receive named secrets, never blanket inheritance.

## Untrusted Input and Injection

Workflow files interpolate expressions *into* scripts before the shell runs, so untrusted input — PR titles, branch names, issue bodies, **workflow inputs** — pasted into `run:` via `${{ }}` is **expression/shell injection** ([Topic 04](../../04-pipeline-as-code-and-platforms/03-variables-contexts-expressions-and-outputs/) covers the mechanism). The safe pattern routes input through `env` and validates:

```yaml
env:
  SAFE_INPUT: ${{ inputs.environment }}

steps:
  - name: Validate input
    run: |
      case "$SAFE_INPUT" in
        development|staging|production) ;;
        *) echo "Invalid input"; exit 1 ;;
      esac
```

Fork pull requests are the sharpest case: they carry untrusted code, so platforms strip their secret access — and `pull_request_target`, which restores privileges while checking out attacker-influenced context, is the classic self-inflicted vulnerability when misused.

## Third-Party Actions

Every `uses:` executes someone else's code inside your job:

```yaml
uses: actions/checkout@v4
```

```yaml
uses: organization/action@full-commit-sha
```

Trade-offs: **major-version tags** are readable and receive patches, but the publisher can move them; **full commit SHAs** are immutable, but still require initial publisher and code review, and need update automation to stay patched. Beyond pinning: prefer trusted publishers, read small actions' source, own and review internal actions, and remember **Marketplace risk** and **CI dependency confusion** (a typo in an action name can resolve to an attacker's repository). **Reusable workflows** deserve the same trust analysis — they run with your permissions and whatever secrets you forward.

## Runners

- Never run untrusted fork code on **privileged self-hosted runners** — the runner's network position and local credentials belong to whatever code executes.
- **Persistent runners** accumulate credentials, caches, and possibly attacker modifications; **ephemeral runners** reset the board every job.
- **Docker socket** access is effective host control.
- Runner **labels are routing, not security boundaries** ([Topic 04](../../04-pipeline-as-code-and-platforms/05-runners-and-execution-environments/)).
- Internal-network runners raise impact; runner images and tools need patching like any fleet.

Two poisoning paths complete the picture: **cache poisoning** (untrusted writes restored into trusted runs) and **artifact poisoning** (downloading artifacts from untrusted runs and executing or trusting their contents). Both are trust-boundary violations wearing convenience clothing. Governance closes the loop: **branch protection** and required review on workflow changes (a workflow edit is a privileged code change), **CODEOWNERS** for `.github/`, and **workflow approval** for first-time contributors.

## Common Mistakes

- Workflow-wide write permissions.
- Secrets available to every job.
- Untrusted input inserted directly into shell commands.
- Floating action branches (`@main`).
- Privileged runner used for public pull requests.
- Reusable workflow receives all secrets (`secrets: inherit` by reflex).
- Cache shared across trust boundaries.
- Artifact downloaded without verifying its source.
- `pull_request_target` used without understanding its risk.
- OIDC role trusting every branch.

## Existing Repository Evidence

- **Least privilege, partially applied**: [KubeOps CI](../../../Projects/2_project/kubeops-gitops/.github/workflows/ci.yml) sets workflow-level `contents: read` explicitly; [KubeOps image-release](../../../Projects/2_project/kubeops-gitops/.github/workflows/image-release.yml) adds `packages: write`; [TaskOps CD](../../../Projects/1_project/taskops-cicd/.github/workflows/cd.yml) grants `packages: write` at the **job** level (tighter). [TaskOps CI](../../../Projects/1_project/taskops-cicd/.github/workflows/ci.yml) declares **no permissions block at all** — it runs with the repository default, the one real least-privilege gap in the set.
- **Action pinning**: everything is tag-pinned (`@v4`, `@v5`, `@v3`, `@v6`; `appleboy/*` by version tag), with `aquasecurity/trivy-action@0.28.0` pinned to an exact release. No SHA pinning anywhere; no floating branches either.
- **Trigger trust**: publishing and deployment run only from `push` to `main`; the fork-facing trigger (`pull_request` in both CI workflows) holds no write permissions and no deployment secrets. No `pull_request_target`, no reusable workflows, no self-hosted runners exist.
- **Secrets scoping**: the deployment secrets (`DEPLOY_*`, `FLASK_SECRET_KEY`) appear only in TaskOps CD's deploy job steps.
- Absent and conceptual: SHA pinning with update automation, CODEOWNERS, OIDC, and any self-hosted runner hardening story.

## Practical Exercise

Audit [TaskOps CI](../../../Projects/1_project/taskops-cicd/.github/workflows/ci.yml) as a security reviewer:

```text
Trigger trust level
Permissions
Secrets
Third-party actions
Action version references
Runner type
Untrusted inputs
Artifacts and caches
OIDC
Main risks
```

Conclude with the two highest-value hardening changes (hint: one is a missing block this lesson names; consider what the BuildKit cache shares across `pull_request` and `main` runs for the second) and the exact YAML each would need — written in notes only. Do not modify the workflow. Target 25–35 minutes.

## Knowledge Check

1. What single question does the pipeline threat model reduce to?
2. Why is job-level `packages: write` better than workflow-level?
3. What makes `pull_request_target` dangerous?
4. Compare tag pinning and SHA pinning for actions.
5. What is cache poisoning?
6. What is the one explicit least-privilege gap among this repository's workflows?

<details>
<summary>View answers</summary>

1. What can code reach when the pipeline executes it — permissions, secrets, network, and host access define the blast radius.
2. Only the publishing job holds write rights; a compromise of any other job in the workflow gets read-only.
3. It runs with base-repository privileges (secrets, write token) in a context influenced by the untrusted PR — misused, it hands attackers privileged execution.
4. Tags are readable and auto-receive patches but are mutable by the publisher; SHAs are immutable but need review anyway plus automation to stay updated.
5. Untrusted code writing cache entries that trusted runs later restore and execute — attacker content crossing a trust boundary via the cache.
6. TaskOps CI has no `permissions:` block, so its token runs with repository defaults instead of explicit read-only.

</details>

## Navigation

- [Back to DevSecOps and Supply-Chain Security](../README.md)
- [Previous: SBOM, Signing, Provenance, and Attestations](../05-sbom-signing-provenance-and-attestations/)
- [Next: DAST, API Security, and Runtime Validation](../07-dast-api-security-and-runtime-validation/)
- [Back to All Learning Materials](../../README.md)
