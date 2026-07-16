# Preview and Ephemeral Environments

## Environments That Live as Long as a Change

A **preview environment** (GitLab calls them **review apps**) is a temporary, per-change deployment: open a pull request, get a running instance of your branch; close it, the instance disappears. The broader term **ephemeral environment** covers any deliberately short-lived environment — per-PR, per-branch, or per-test-run.

```text
Pull request opened
       ↓
Temporary environment created
       ↓
Application deployed
       ↓
Review and automated checks
       ↓
Pull request merged or closed
       ↓
Environment destroyed
```

They shine for **UI review** (reviewers click the change instead of imagining it), **API integration** checks, **acceptance testing**, **stakeholder review** (a URL in the PR comment beats a meeting), and **infrastructure validation** (does the change even deploy?).

## Lifecycle Mechanics

Creation, update (each new commit redeploys), and — the part teams forget — **destruction**. Every resource needs uniqueness and isolation:

- **Unique naming** per change: a namespace, hostname, and resource prefix like:

```text
pr-184-task-api
```

- **Isolated data** — a temporary database with **seed data**, never a shared one: previews sharing a database corrupt each other's state and reviews.
- **DNS and TLS** — each preview needs a resolvable, ideally certificate-backed URL; wildcard DNS and certificates make this tractable.
- **PR comments with deployment URLs** close the loop for reviewers.
- **Environment ownership** links the resources and URL to the pull request, author, and team responsible for cleanup.
- **Concurrency and collision** — two pushes to the same PR must not fight over one environment; updates should supersede, not overlap.

**Branch names are untrusted input.** A branch called `feature/Fix#1; rm -rf /` must be sanitized before it becomes a DNS label, a Kubernetes namespace, a path, or — worst — part of a shell command. Lowercase, strip or replace invalid characters, truncate, and add the PR number for uniqueness; never interpolate raw branch names into commands.

## The Costs and Limits

- **Cost and quotas** — every open PR is a running stack; **resource quotas**, **idle timeouts**, and TTLs keep the bill bounded.
- **Slow provisioning** — a preview that takes 30 minutes to build defeats its purpose.
- **Shared external dependencies** — previews often still point at shared third-party sandboxes, reintroducing coupling.
- **Data setup** — realistic seed data is work; empty databases review poorly.
- **Secret exposure** — previews run *unreviewed branch code*; they must receive scoped preview credentials, never production secrets, and **fork PRs** deserve extra caution (untrusted code + any credentials = incident).
- **Cleanup reliability** — destruction must trigger on close *and* merge *and* staleness; **orphaned environments** and leftover DNS records are the default failure mode without a scheduled reaper.
- **Incomplete parity** — a preview validates the change, not production behavior; it complements, not replaces, staging.

Access should be deliberate even for disposable systems. A deployment URL may need authentication, IP restrictions, or private networking; temporary does not mean harmless. Teardown should remove the namespace or compute, database, storage, DNS record, certificate material, and any preview-scoped credentials. A scheduled inventory that compares open pull requests with live previews catches cleanup events that were missed.

## Common Mistakes

- No automatic destruction.
- Sharing one database across all previews.
- Giving preview environments production credentials.
- Creating public URLs without access controls.
- No quota or idle timeout.
- Using raw branch names in DNS, namespaces, paths, or commands.
- Leaving DNS records behind after teardown.
- Treating a preview environment as production validation.

## Existing Repository Evidence

The repository does **not** implement preview or ephemeral environments — no per-PR deployments, no review apps, no teardown workflows. The nearest real relatives, useful as building blocks for the exercise: [TaskOps CI](../../../Projects/1_project/taskops-cicd/.github/workflows/ci.yml) already creates an *ephemeral container* per run (starts the built image, smoke-tests it, destroys it with `if: always()` — a preview environment's lifecycle in miniature, minus the URL), and KubeOps' [Helm chart](../../../Projects/2_project/kubeops-gitops/helm/kubeops/) is parameterized (namespace, hostname, values) exactly the way per-PR installs would need. Preview environments may be added in a later project-enhancement phase.

## Practical Exercise

Design (do not implement) an ephemeral-environment lifecycle for KubeOps:

1. Naming: derive namespace and hostname from a PR number and sanitized branch name; state your sanitization rules.
2. Creation: which Helm values would a `values-preview.yaml` override, and what image tag should a PR build use?
3. Data and secrets: what seed data, and which credentials must previews *not* receive?
4. Access: who can reach the preview URL?
5. Destruction: list all three teardown triggers and every resource that must be reaped (include DNS).
6. Cost: one quota and one timeout rule.

Target 25–35 minutes.

## Knowledge Check

1. What is a preview environment and when is it destroyed?
2. Why must previews not share a database?
3. Why are raw branch names dangerous in environment naming?
4. Why must previews never hold production credentials?
5. What existing repository behavior most resembles an ephemeral environment?
6. Why is a green preview not production validation?

<details>
<summary>View answers</summary>

1. A temporary per-change deployment created when a PR opens and destroyed when it is merged, closed, or goes stale.
2. Concurrent previews would corrupt each other's state, making reviews unreliable and failures unreproducible.
3. They are untrusted, arbitrarily formatted input; unsanitized use breaks DNS/namespace rules and can inject into shell commands.
4. Previews run unreviewed (possibly forked) branch code; any credential they hold is exposed to that code.
5. TaskOps CI's docker job: build, run, smoke-test, and always-destroy an ephemeral container per run.
6. Previews validate the change in a small, non-production-parity context; capacity, real data, and production configuration remain unexercised.

</details>

## Navigation

- [Back to Environments, Configuration, and Secrets](../README.md)
- [Previous: Environment Strategy and Parity](../01-environment-strategy-and-parity/)
- [Next: Externalized Configuration and Variables](../03-externalized-configuration-and-variables/)
- [Back to All Learning Materials](../../README.md)
