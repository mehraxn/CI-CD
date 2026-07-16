# Kubernetes and GitOps

Kubernetes reconciles declarative desired state for container workloads. GitOps stores that state in Git and uses a controller to compare and reconcile clusters.

```text
Verified image → reviewed manifests/chart → Git desired state → controller reconciliation → observed workload
```

## Lessons

| # | Lesson |
|---|--------|
| 01 | [Kubernetes Delivery Fundamentals](./01-kubernetes-delivery-fundamentals/) |
| 02 | [Manifests, Deployments, Services, and Namespaces](./02-manifests-deployments-services-and-namespaces/) |
| 03 | [ConfigMaps, Secrets, Probes, and Resources](./03-configmaps-secrets-probes-and-resources/) |
| 04 | [Helm Charts, Values, and Releases](./04-helm-charts-values-and-releases/) |
| 05 | [Kustomize Bases and Overlays](./05-kustomize-bases-and-overlays/) |
| 06 | [GitOps Principles and Reconciliation](./06-gitops-principles-and-reconciliation/) |
| 07 | [Argo CD Applications, Sync, and Drift](./07-argo-cd-applications-sync-and-drift/) |
| 08 | [Multi-Environment and Multi-Cluster Delivery](./08-multi-environment-and-multi-cluster-delivery/) |

## Learning Objectives

Explain desired state, workload/network/config resources, probes/resources/security, Helm and Kustomize, pull-based GitOps, Argo CD, drift, and environment/cluster organization.

## Study Order and Project Connections

Follow the lessons. [KubeOps raw manifests](../../Projects/2_project/kubeops-gitops/k8s/) demonstrate Namespace, Deployment, Service, Ingress, ConfigMap, placeholder Secret, probes, resources, and security context. Its [Helm chart](../../Projects/2_project/kubeops-gitops/helm/kubeops/) templates the same application. [Argo CD Application](../../Projects/2_project/kubeops-gitops/argocd/application.yaml) is manual-sync by default; automated prune/self-heal are commented examples. Kustomize, AppProject, ApplicationSet, PVC, and multi-cluster delivery are absent.

## Completion Checklist
- [ ] I can map Kubernetes resources and selectors.
- [ ] I can distinguish config, secrets, probes, requests, and limits.
- [ ] I can compare Helm and Kustomize.
- [ ] I can explain pull reconciliation and drift.

## Navigation
- [Back to Learning Materials](../README.md)
- [Previous: Docker in CI/CD](../11-docker-in-cicd/)
- [Next: Infrastructure as Code and Automation](../13-infrastructure-as-code-and-automation/)
