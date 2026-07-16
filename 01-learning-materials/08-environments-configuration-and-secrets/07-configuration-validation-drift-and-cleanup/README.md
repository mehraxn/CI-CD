# Configuration Validation, Drift, and Cleanup

## Declared vs. Actual

Configuration is a claim about how systems should be set up. Validation checks the claim's internal correctness; drift detection checks whether reality still matches it:

```text
Declared configuration
        ↓
Validation
        ↓
Deployment
        ↓
Actual environment state
        ↓
Drift detection
        ↓
Reconciliation or approved exception
```

## Validation: Catching Errors Before They Deploy

Validation layers, cheapest first:

- **Schema validation** — required keys, **type**, **range**, and **enum** checks against a JSON/YAML schema.
- **Tool-native validation** — Helm rendering and linting, `terraform validate` and **plan** (a **dry run** showing what would change before it does), Kubernetes admission controls rejecting bad resources at the API server.
- **Policy checks** — Policy as Code asserting rules like "no container runs privileged."
- **CI checks for missing variables** — fail the pipeline, not the deployment, when a required key is absent.
- **Startup validation** — the application refuses to start on missing/invalid config (the `os.environ["X"]` idiom from [lesson 03](../03-externalized-configuration-and-variables/)).
- **Smoke tests** — the last line: is the deployed thing actually alive with this config?

The anti-pattern all of these prevent: **silent fallback to unsafe defaults** — an app that quietly runs with `DEBUG=true` because the real config never arrived.

## Drift: When Reality Wanders

**Drift** is divergence between desired and actual state, and it comes in flavors:

| Drift type | Example |
|------------|---------|
| Application configuration drift | Staging uses a different variable name |
| Infrastructure drift | Resource changed manually outside IaC |
| Secret drift | Credential rotated in one environment only |
| Environment drift | Staging runtime differs from production |
| Documentation drift | README no longer matches real configuration |

Drift's usual source is manual change — `kubectl edit`, a console tweak, an SSH fix at 2 a.m. — and its usual amplifier is **UI-only configuration** nobody recorded. Defenses: a **configuration inventory** (what exists, where, owned by whom), **drift detection** (compare desired vs. actual on a schedule or continuously), and **reconciliation** — either revert reality to the declaration or update the declaration through review. A drift report ignored indefinitely is just decoration; every finding needs reconciliation or an approved, documented exception. **Configuration versioning** in Git plus **change review** is what makes "desired state" a real, diffable thing — and makes **configuration rollback** a `git revert` instead of archaeology.

## Cleanup: Retiring What No Longer Serves

Environments and configuration accumulate. Deliberate cleanup covers: destroying closed pull-request/preview environments, removing **stale variables**, revoking **unused secrets** (an unused credential is pure risk), deleting **orphaned environments**, stale DNS records, and orphaned storage — while preserving required audit evidence and protecting production resources. **Resource tagging** with **ownership** and **expiration/TTL** labels is what makes safe cleanup automatable; cleanup jobs themselves need scoped permissions (a reaper with admin rights is a disaster feature) and audit logs. The payoff is **cost control** and a smaller attack surface.

## Common Mistakes

- UI-only undocumented configuration.
- No validation before deployment.
- Silent fallback to unsafe defaults.
- Manual production changes outside the declared state.
- Drift reports ignored indefinitely.
- Deleting resources without checking ownership.
- Cleanup jobs with excessive permissions.
- Rotating secrets in only some environments (secret drift by procedure).
- Environment documentation never updated.

## Existing Repository Evidence

- **Real drift detection**: [KubeOps' Argo CD Application](../../../Projects/2_project/kubeops-gitops/argocd/application.yaml) is a working desired-state/actual-state loop — with manual sync active, Argo CD *reports* drift (`OutOfSync`) and waits; the commented-out `automated: prune / selfHeal` block is exactly the reconciliation switch this lesson describes (selfHeal reverts manual `kubectl edit` changes back to Git state). The file's own comments document both modes.
- **Real declarative validation**: [Terraform variables.tf](../../../Projects/3_project/terraform/variables.tf) carries `validation` blocks — non-empty project name, port ranges 1–65535, and a required-ports check — schema-style validation in IaC form.
- **Startup/deployment-time checks**: TaskOps' Compose `${FLASK_SECRET_KEY:?}` (aborts on missing secret) and both projects' container `HEALTHCHECK`s plus CD's post-deploy smoke test give the fail-fast and smoke-test layers.
- **Documentation as anti-drift**: the `.env.example` files and the heavily commented values files keep declared configuration discoverable.
- Not demonstrated: JSON-schema config validation, policy-as-code checks, CI missing-variable checks, preview cleanup (no previews exist), TTL tagging, or automated drift remediation (Argo CD's automation is present but deliberately disabled). These may arrive in later enhancement phases.

## Practical Exercise

Create a configuration inventory for KubeOps across its carriers (`.env.example`, ConfigMap, Helm values trio, Secret example, Argo CD app):

```text
Configuration source
Expected value type
Environment scope
Sensitive or non-sensitive
Validation method
Owner
Drift risk
Cleanup rule
```

Include at least `APP_ENV`, `LOG_LEVEL`, `APP_SECRET_KEY`, `replicaCount`, `image.tag`, and the Argo CD `targetRevision`. For each, state today's validation (often "none — startup behavior unknown") and the drift risk given manual sync. Finish with one sentence: what single Argo CD change would convert drift *detection* into drift *correction*, and what new risk would that introduce? Do not include real secret values. Target 25–35 minutes.

## Knowledge Check

1. What is the difference between validation and drift detection?
2. Why is silent fallback to defaults dangerous?
3. What are the two legitimate responses to detected drift?
4. What does Argo CD's `selfHeal` do, and why is it disabled here?
5. Why do cleanup jobs need scoped permissions?
6. Which repository file demonstrates declarative input validation?

<details>
<summary>View answers</summary>

1. Validation checks declared configuration's correctness before deployment; drift detection compares deployed reality against the declaration afterward.
2. The system runs in an unintended (possibly insecure) state while appearing healthy — the missing configuration produces no error, only wrong behavior.
3. Reconcile reality back to the declaration, or update the declaration through reviewed change — plus documented, approved exceptions.
4. It automatically reverts manual changes to match Git; it is commented out so a human syncs deliberately — safer for a demo, slower to correct drift.
5. A reaper with broad rights turns a cleanup bug into mass deletion; it should only be able to delete what its policy covers.
6. Project 3's Terraform `variables.tf`, with validation blocks for names, port ranges, and required ports.

</details>

## Navigation

- [Back to Environments, Configuration, and Secrets](../README.md)
- [Previous: Protected Environments, Approvals, and Release Controls](../06-protected-environments-approvals-and-release-controls/)
- [Back to All Learning Materials](../../README.md)
