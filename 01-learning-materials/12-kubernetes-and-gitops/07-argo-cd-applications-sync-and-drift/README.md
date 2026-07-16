# Argo CD Applications, Sync, and Drift

An Argo CD Application maps source repo/revision/path to destination cluster/namespace and sync policy. `Synced` describes desired/actual comparison; health describes resource condition—neither alone proves application correctness. AppProjects constrain sources/destinations/resources; ApplicationSets generate Applications. Both are absent here.

KubeOps Application tracks `main`, `helm/kubeops`, `values-dev.yaml`, in-cluster server, and `kubeops-dev`. `CreateNamespace=true` is active. Automated `prune` and `selfHeal` are commented out, so sync is manual. Files cannot prove Argo CD installation or cluster state.

Prune can delete; self-heal can revert manual emergency changes. Sync ordering, hooks, waves, and rollback need deliberate policy.

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
