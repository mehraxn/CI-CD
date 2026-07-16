# GitOps Principles and Reconciliation

GitOps uses declarative, version-controlled desired state, reviewed changes, and an automated reconciliation loop. Pull-based agents watch Git from the cluster; push-based CI directly holds cluster access. Pull reduces CI credentials but does not remove controller, repository, image, or approval risk.

Drift is difference between Git and cluster. Detection reports it; self-healing reverts it; pruning deletes resources removed from desired state and can be destructive. Git revert changes desired state, after which reconciliation performs the cluster action.

KubeOps documents both manual kubectl/Helm push paths and Argo CD pull-based GitOps. The Application defaults to manual sync, so detection is present conceptually but automatic reconciliation is disabled.

## Core Operating Model

```text
Git desired state
      |
GitOps controller compares
      |
Cluster actual state
      |
Difference detected
      |
Controller reports or reconciles
```

GitOps requires declarative desired state, version control, reviewable changes, and reconciliation. A pull request provides discussion and approval. Git history records who proposed and merged a change, though commit identity and branch controls still need protection. The controller continuously reads an authorized source and compares rendered resources with objects it owns in the cluster.

Drift is a difference between desired and actual state. Detection reports it. Sync applies desired state. Self-healing automatically restores fields changed outside Git. Pruning removes resources no longer present in desired state and can delete important objects. Manual sync requires an operator action; automated sync acts according to policy. Sync windows can restrict when changes occur. These mechanisms must align with approvals, on-call procedures, and maintenance windows.

Reverting Git creates a new desired-state change; it is not instantaneous application recovery. Reconciliation must still apply it, and older application code may not work with migrated data. Roll-forward is often safer when state is incompatible. Emergency break-glass changes need a documented identity, narrow permission, time limit, audit event, and a follow-up Git change; otherwise self-heal may undo them or permanent drift remains.

## Push and Pull

In push delivery, CI holds cluster credentials and runs commands such as `kubectl apply` or `helm upgrade`. It can be direct and simple, but compromises or configuration errors in CI reach the cluster. In pull-based GitOps, CI publishes an image and updates desired state; a cluster-side controller pulls Git changes. This reduces direct CI cluster access and works through outbound repository connections, but does not eliminate security risk. The controller has cluster permissions, repository credentials, and potentially broad impact.

An application repository may contain code and deployment files together. An environment repository may separate promotion and operations ownership. A monorepo centralizes visibility; polyrepos separate teams and permissions. There is no universally correct layout. Ownership, review boundaries, atomic changes, controller scope, and discovery matter more than fashion.

Secrets are a central challenge because Git history retains plaintext. Sealed-secret patterns store cluster-decryptable ciphertext; external-secret patterns store references and fetch from a manager. Both need key rotation and access policy. Neither is implemented here. Image-update automation can propose or commit new tags/digests, but it must preserve review and avoid moving unverified content. No such automation exists in KubeOps.

GitOps does not guarantee correct manifests, secure secrets, safe migrations, correct behavior, monitoring, appropriate permissions, or business approval. A controller can reconcile a perfectly declared outage. Health and observability remain separate feedback loops.

## KubeOps Flow

KubeOps [image release](../../../Projects/2_project/kubeops-gitops/.github/workflows/image-release.yml) publishes SHA and `latest` to GHCR but does not update a values file afterward. [Helm development values](../../../Projects/2_project/kubeops-gitops/helm/kubeops/values-dev.yaml) use `kubeops:local`; production values use GHCR `latest`. Therefore a complete automated image-to-Git promotion chain is absent.

The [Argo CD Application](../../../Projects/2_project/kubeops-gitops/argocd/application.yaml) watches repository path `helm/kubeops` at `main`, loads `values-dev.yaml`, and targets `kubeops-dev` in the cluster where Argo CD runs. Manual sync is active. The commented automated block explains prune and self-heal, but comments do not enable behavior. Project docs also present manual `kubectl` and Helm commands, which are push paths outside the Argo reconciliation model.

The real map is thus: image workflow -> GHCR; separately, Git chart/values -> Argo CD Application -> one dev namespace. The missing link is a reviewed update from newly published SHA/digest to the desired image value. No files prove installed Argo CD, repository credentials, cluster credentials, controller permissions, sync windows, sealed/external secrets, or live reconciliation.

Common mistakes include plaintext secrets, excessive controller permissions, automated prune without deletion review, unclear repository ownership, manual tag changes, assuming Git revert guarantees recovery, and emergency fixes never reconciled into Git.

## Governance and Failure Handling

Define who owns application code, desired-state repositories, environments, controller administration, and emergency access. Branch protection and review should match environment risk. Controller scope should be no broader than its owned resources and destinations. Repository and cluster credentials need rotation and audit independent of manifest review.

Before automated sync, decide how failed health, partial application, prune deletion, dependency ordering, and maintenance windows behave. Test drift detection with a harmless field and confirm whether policy reports or repairs it. Inventory resources that must never be pruned accidentally. A Git commit can be valid while rendered output violates cluster policy or application expectations.

Incident response should preserve Git revision, rendered diff, sync operation, resource status, and application signals. If break-glass changes are necessary, record them and reconcile the final state into Git. Otherwise self-heal may undo the fix or hidden drift becomes the new normal. Rollback through Git must respect data compatibility; roll-forward may be safer.

The audit trail is only as trustworthy as identities and controls. Shared accounts, rewritten history, unreviewed bot commits, or excessive controller permissions weaken it. GitOps is disciplined operations through reconciliation, not permissionless automation.

## Reconciliation Metrics

Useful operational measures include time from approved Git change to observed sync, duration OutOfSync, failed operations, repeated drift, prune events, and application verification after sync. Metrics should distinguish controller availability from application health. Alerting on every harmless generated-field difference creates noise; ignoring broad paths hides real change.

## Practical Exercise
Draw push and pull flows, identities, audit points, drift behavior, and failure modes.
## Knowledge Check
1. GitOps requirements? 2. Pull removes all risk? 3. Prune effect? 4. Git revert immediately changes cluster?
<details><summary>Answers</summary>
1. Declarative Git state plus reconciliation. 2. No. 3. Deletes removed resources. 4. Only after sync/reconciliation.
</details>
## Navigation
- [Back to Kubernetes and GitOps](../README.md)
- [Previous: Kustomize Bases and Overlays](../05-kustomize-bases-and-overlays/)
- [Next: Argo CD Applications, Sync, and Drift](../07-argo-cd-applications-sync-and-drift/)
- [Back to All Learning Materials](../../README.md)
