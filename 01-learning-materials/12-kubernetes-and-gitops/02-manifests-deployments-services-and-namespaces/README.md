# Manifests, Deployments, Services, and Namespaces

Manifests use `apiVersion`, `kind`, `metadata`, and `spec`. A Deployment manages ReplicaSets/Pods; selector labels must match Pod-template labels. A Service gives stable discovery/routing to matching Pods. Ingress defines external HTTP routing through an installed controller. Namespace scopes names and some policy.

KubeOps [namespace](../../../Projects/2_project/kubeops-gitops/k8s/namespace.yaml), [deployment](../../../Projects/2_project/kubeops-gitops/k8s/deployment.yaml), [service](../../../Projects/2_project/kubeops-gitops/k8s/service.yaml), and [ingress](../../../Projects/2_project/kubeops-gitops/k8s/ingress.yaml) demonstrate the relationship. No PVC or StatefulSet exists. Deployment strategy is omitted, so platform defaults apply.

## Practical Exercise
Map names, namespace, labels/selectors, replicas, ports, image, and routing for KubeOps.
## Knowledge Check
1. Service purpose? 2. Selector mismatch result? 3. Does Ingress install controller? 4. Namespace a full security boundary?
<details><summary>Answers</summary>
1. Stable routing/discovery. 2. No endpoints. 3. No. 4. No.
</details>
## Navigation
- [Back to Kubernetes and GitOps](../README.md)
- [Previous: Kubernetes Delivery Fundamentals](../01-kubernetes-delivery-fundamentals/)
- [Next: ConfigMaps, Secrets, Probes, and Resources](../03-configmaps-secrets-probes-and-resources/)
- [Back to All Learning Materials](../../README.md)
