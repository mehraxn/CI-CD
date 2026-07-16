# Kubernetes and GitOps

Kubernetes reconciles declarative desired state for container workloads. GitOps stores that state in Git and uses a controller to compare and reconcile clusters.

```text
Verified image → reviewed manifests/chart → Git desired state → controller reconciliation → observed workload
```

## Delivery and Reconciliation Model

Kubernetes accepts API objects that describe desired state. Controllers observe actual state and repeatedly act to reduce differences. A Deployment does not run application code itself; it manages ReplicaSets, which maintain Pods created from a template. A Service selects Pods and provides stable routing. Configuration, secrets, storage, policy, and ingress are separate resources that must agree with workload labels, ports, and namespaces.

GitOps adds a version-controlled source of desired state and a controller that compares it with a cluster. A reviewed Git change becomes the delivery request. Pull-based reconciliation reduces the need for CI to hold direct cluster credentials, but the in-cluster controller still needs protected repository access and appropriately limited cluster permissions. Manual and automated sync are policy choices; automation does not remove approvals or make an unsafe manifest correct.

```text
Verified image
    |
Reviewed manifest or chart change
    |
Git desired state
    |
GitOps controller compares with cluster
    |
Report drift or reconcile
    |
Observe workload health and behavior
```

Kubernetes self-healing means controllers replace or restart resources to match declarations. It cannot prove business correctness, data integrity, safe migrations, or useful application responses. Likewise, GitOps provides review and reconciliation mechanics but does not guarantee secure secrets, correct permissions, monitoring, or recovery.

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

After completing this topic, you should be able to:

- explain desired state, reconciliation, Pods, Deployments, and Services;
- map namespaces, labels, selectors, ports, ConfigMaps, Secrets, probes, and resources;
- distinguish readiness, liveness, and startup behavior;
- explain Helm charts, values, templates, releases, and rollback limits;
- compare Helm templating with Kustomize bases and overlays;
- distinguish push-based deployment from pull-based GitOps;
- interpret Argo CD source, destination, sync, drift, and health fields; and
- design promotion across environments and clusters without inventing repository behavior.

## Study Order and Project Connections

Follow the numbered lessons: begin with controllers, then learn resources and operational settings, package them, compare customization methods, and finish with reconciliation and promotion.

[KubeOps raw manifests](../../Projects/2_project/kubeops-gitops/k8s/) demonstrate a Namespace, two-replica Deployment, ClusterIP Service, Ingress, ConfigMap, placeholder Secret, liveness/readiness probes, resource requests/limits, and restrictive security context. The image is `kubeops:local`; no real cluster state follows from committed YAML.

Its [Helm chart](../../Projects/2_project/kubeops-gitops/helm/kubeops/) templates Deployment, Service, Ingress, ConfigMap, Secret, and ServiceAccount resources. Defaults plus dev/prod values change replicas, image, environment, ingress, resources, and secret strategy. [Argo CD Application](../../Projects/2_project/kubeops-gitops/argocd/application.yaml) tracks `main`, path `helm/kubeops`, and `values-dev.yaml`, targeting the in-cluster server and `kubeops-dev`. Sync is manual; automated prune and self-heal are commented examples.

Kustomize, AppProject, ApplicationSet, startup probes, PersistentVolumeClaims, Helm hooks, automated image-to-Git updates, multiple Application resources, and multi-cluster registration are absent. TaskOps uses server-side Compose rather than Kubernetes, and Project 3 provides Terraform/Ansible/Compose observability examples but no Kubernetes delivery files.

## Study Guidance

Treat committed declarations as evidence of intent, not proof of live cluster state. Pair Git review with observed rollout status, controller events, and application tests when working on a real system. Preserve one accepted image identity through promotion, and assign an owner to controller permissions, deletion policy, secret delivery, drift handling, and recovery. The examples here are safe to inspect without running cluster commands.

## Completion Checklist
- [ ] I can map Kubernetes resources and selectors.
- [ ] I can distinguish config, secrets, probes, requests, and limits.
- [ ] I can compare Helm and Kustomize.
- [ ] I can explain pull reconciliation and drift.
- [ ] I can state which cluster and GitOps features are conceptual here.

## Navigation
- [Back to Learning Materials](../README.md)
- [Previous: Docker in CI/CD](../11-docker-in-cicd/)
- [Next: Infrastructure as Code and Automation](../13-infrastructure-as-code-and-automation/)
