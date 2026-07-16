# Argo CD Applications, Sync, and Drift

An Argo CD Application maps source repo/revision/path to destination cluster/namespace and sync policy. `Synced` describes desired/actual comparison; health describes resource condition—neither alone proves application correctness. AppProjects constrain sources/destinations/resources; ApplicationSets generate Applications. Both are absent here.

KubeOps Application tracks `main`, `helm/kubeops`, `values-dev.yaml`, in-cluster server, and `kubeops-dev`. `CreateNamespace=true` is active. Automated `prune` and `selfHeal` are commented out, so sync is manual. Files cannot prove Argo CD installation or cluster state.

Prune can delete; self-heal can revert manual emergency changes. Sync ordering, hooks, waves, and rollback need deliberate policy.

## Application Anatomy

An Application is a custom resource mapping a source to a destination. `repoURL`, `targetRevision`, and `path` identify desired state. Helm-specific fields select values. `destination.server` or a registered name identifies a cluster, and `destination.namespace` selects the target namespace. The Application object itself normally lives in the Argo CD namespace; that is different from where workloads are deployed.

Conceptual example—the URL is intentionally invalid and fields do not describe this repository:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: task-api
  namespace: argocd
spec:
  source:
    repoURL: https://example.invalid/repository.git
    targetRevision: main
    path: k8s/overlays/production
  destination:
    server: https://kubernetes.default.svc
    namespace: task-api
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

`prune: true` may delete managed resources removed from Git. `selfHeal: true` may revert manual changes. Both should be enabled deliberately after ownership, deletion, and emergency procedures are understood. `CreateNamespace=true` lets Argo CD create a missing destination namespace during sync; it does not configure all namespace policy.

An AppProject constrains allowed sources, destinations, and resource kinds. ApplicationSet generates Applications from lists, clusters, or repository data. Neither appears here. Repository credentials and cluster credentials are external protected state and must not be embedded in an Application. RBAC should limit who can view, refresh, diff, sync, or change projects.

## Status, Diff, and Ordering

`Synced` means live state matches desired state under comparison rules; `OutOfSync` means a difference exists. Health is separate: resources may be `Healthy`, `Degraded`, `Missing`, or `Unknown`. A Synced application can be unhealthy because desired state itself fails. A Healthy workload can be OutOfSync after a manual change. Neither status proves business transactions work.

Refresh asks Argo CD to compare current source/live state; a hard refresh also clears relevant cached source/render information. Diff shows intended changes. Ignore-differences rules can suppress known controller-generated fields but can also hide important drift if broad. Resource tracking determines which objects belong to an Application. Application history supports inspection and rollback of prior desired revisions, subject to the same data-compatibility limits as any rollback.

Sync waves and hooks can order resources such as namespaces, migrations, and workloads. Hook failure and cleanup need design. Argo CD notifications can report state changes. Custom resources may need health assessment; absent checks can produce `Unknown` or misleading status. These capabilities are conceptual here.

## Real Application Annotation

KubeOps [application.yaml](../../../Projects/2_project/kubeops-gitops/argocd/application.yaml) creates Application `kubeops` in namespace `argocd` and uses built-in project `default`. Its source repository is the KubeOps GitHub URL, target revision is `main`, path is `helm/kubeops`, and Helm loads `values-dev.yaml`. The destination server `https://kubernetes.default.svc` means the cluster in which Argo CD runs, and the workload namespace is `kubeops-dev`.

The active `syncPolicy` contains `CreateNamespace=true`. The `automated` block, `prune: true`, and `selfHeal: true` are commented out. Therefore the declared behavior is manual sync with namespace creation during a sync—not automated reconciliation. The file comments mention UI or `argocd app sync kubeops`, but no command was run and no live state is proven.

No AppProject manifest beyond use of `default`, ApplicationSet, sync waves, hooks, ignore-differences rules, notifications, custom health configuration, repository credential, or additional cluster registration is present. No production Application exists. The Application uses development values; calling it production would be inaccurate.

Common mistakes include pointing production at a development path, overly broad permissions, auto-prune without review, plaintext secrets, unrelated resources under one Application, unexpected target branches, missing custom health logic, hotfixes outside Git, and confusing sync with health. Access to sync is itself a production permission and should follow least privilege.

## Practical Exercise
Annotate every real Application field and mark active, commented, external, and unverifiable behavior.
## Knowledge Check
1. Sync versus health? 2. Is auto-sync active? 3. `selfHeal` effect? 4. AppProject present?
<details><summary>Answers</summary>
1. Drift status versus resource condition. 2. No. 3. Reverts drift. 4. No.
</details>
## Navigation
- [Back to Kubernetes and GitOps](../README.md)
- [Previous: GitOps Principles and Reconciliation](../06-gitops-principles-and-reconciliation/)
- [Next: Multi-Environment and Multi-Cluster Delivery](../08-multi-environment-and-multi-cluster-delivery/)
- [Back to All Learning Materials](../../README.md)
