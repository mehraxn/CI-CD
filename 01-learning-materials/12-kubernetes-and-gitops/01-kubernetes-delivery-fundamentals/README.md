# Kubernetes Delivery Fundamentals

A cluster contains a control plane and worker nodes. The API stores desired state; scheduler places Pods; controllers run reconciliation loops comparing actual state and creating/replacing resources. Pods are ephemeral and normally managed through Deployments/ReplicaSets rather than directly.

CI builds/verifies an image; delivery updates declarative image/configuration; Kubernetes pulls it and maintains replicas. Self-healing restarts/replaces resources but cannot prove business correctness. Namespaces organize names/access but are not complete isolation.

KubeOps is the repository example: raw YAML, Helm, and Argo CD target one in-cluster development namespace. No real cluster state is inferable from files.

## Practical Exercise
Draw source → image → manifest/chart → API → Deployment → ReplicaSet → Pod → Service.

## Knowledge Check
1. Desired versus actual? 2. Who places Pods? 3. Why not manage Pods directly? 4. Does self-heal prove correctness?
<details><summary>Answers</summary>
1. Declared versus observed state. 2. Scheduler. 3. Controllers replace them. 4. No.
</details>
## Navigation
- [Back to Kubernetes and GitOps](../README.md)
- [Next: Manifests, Deployments, Services, and Namespaces](../02-manifests-deployments-services-and-namespaces/)
- [Back to All Learning Materials](../../README.md)
