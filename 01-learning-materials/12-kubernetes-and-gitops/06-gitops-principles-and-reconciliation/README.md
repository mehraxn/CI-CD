# GitOps Principles and Reconciliation

GitOps uses declarative, version-controlled desired state, reviewed changes, and an automated reconciliation loop. Pull-based agents watch Git from the cluster; push-based CI directly holds cluster access. Pull reduces CI credentials but does not remove controller, repository, image, or approval risk.

Drift is difference between Git and cluster. Detection reports it; self-healing reverts it; pruning deletes resources removed from desired state and can be destructive. Git revert changes desired state, after which reconciliation performs the cluster action.

KubeOps documents both manual kubectl/Helm push paths and Argo CD pull-based GitOps. The Application defaults to manual sync, so detection is present conceptually but automatic reconciliation is disabled.

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
