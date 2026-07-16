# Manifests, Deployments, Services, and Namespaces

Manifests use `apiVersion`, `kind`, `metadata`, and `spec`. A Deployment manages ReplicaSets/Pods; selector labels must match Pod-template labels. A Service gives stable discovery/routing to matching Pods. Ingress defines external HTTP routing through an installed controller. Namespace scopes names and some policy.

KubeOps [namespace](../../../Projects/2_project/kubeops-gitops/k8s/namespace.yaml), [deployment](../../../Projects/2_project/kubeops-gitops/k8s/deployment.yaml), [service](../../../Projects/2_project/kubeops-gitops/k8s/service.yaml), and [ingress](../../../Projects/2_project/kubeops-gitops/k8s/ingress.yaml) demonstrate the relationship. No PVC or StatefulSet exists. Deployment strategy is omitted, so platform defaults apply.

## Anatomy of a Manifest

`apiVersion` selects an API group/version, `kind` selects the resource type, `metadata` carries name, namespace, labels, and annotations, and `spec` declares desired behavior. Names identify objects inside their scope. Labels are queryable identity used by selectors; annotations carry non-identifying metadata. A manifest should be reviewed as an interconnected set rather than isolated YAML.

This conceptual relationship shows ownership and traffic:

```text
Namespace
  | Deployment selector == Pod-template labels
  |   -> ReplicaSet -> Pods (containerPort 8000)
  | Service selector == Pod labels
  |   -> Service port 80 -> targetPort 8000
  | Ingress backend -> Service port 80
```

A Deployment describes replicas, a label selector, and a Pod template. The selector is effectively part of its identity and must match template labels. A ReplicaSet maintains the requested Pod count. Rollout strategy may be `RollingUpdate` or `Recreate`; when omitted, Deployment defaults apply. Rolling updates create a controlled overlap based on surge/unavailable settings, while Recreate stops old Pods before new Pods. Neither guarantees zero downtime without readiness, capacity, compatible versions, and traffic behavior.

A container declaration includes image, name, ports, environment, volume mounts, probes, resources, and security context. `containerPort` is metadata for the process port; it does not publish externally. Pods receive changing IPs, so a Service supplies stable virtual addressing and discovery. Its selector must match intended Pods, and `targetPort` must reach the application. `ClusterIP` is internal by default. `NodePort` and `LoadBalancer` expose through node or provider mechanisms, but creating a Service does not guarantee an external load balancer in every environment.

Ingress defines host/path routing to Services. It requires an installed controller and usually separate DNS and TLS configuration. A Namespace scopes names and resources such as ConfigMaps and Secrets. Cross-namespace access and policy need deliberate design; namespaces alone do not provide full tenant isolation.

## Educational Manifest Fragments

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: task-api
  namespace: task-api
spec:
  replicas: 2
  selector:
    matchLabels:
      app: task-api
  template:
    metadata:
      labels:
        app: task-api
    spec:
      containers:
        - name: application
          image: ghcr.io/example/task-api:1.4.0
          ports:
            - containerPort: 8000
```

This is conceptual; `example` is a placeholder. A matching Service would use selector `app: task-api`, port 80, and `targetPort: 8000`. Hard-coded environment values should instead be classified into ConfigMaps or Secrets. An immutable image identity is preferable to a mutable production tag.

## KubeOps Relationship Map

The real [Namespace](../../../Projects/2_project/kubeops-gitops/k8s/namespace.yaml) is `kubeops-dev`. The [Deployment](../../../Projects/2_project/kubeops-gitops/k8s/deployment.yaml) requests two Pods, and its selector matches template label `app: kubeops`. It uses `kubeops:local`, `IfNotPresent`, port 8000, `envFrom`, probes, resources, and a security context. No explicit rollout strategy exists, so Kubernetes defaults apply.

The [Service](../../../Projects/2_project/kubeops-gitops/k8s/service.yaml) is `ClusterIP`, selects `app: kubeops`, and maps port 80 to 8000. The [Ingress](../../../Projects/2_project/kubeops-gitops/k8s/ingress.yaml) routes host `kubeops.local` and `/` to Service port 80. These selectors and ports align. The files do not prove an Ingress controller, DNS record, cluster, or healthy endpoint exists.

No PersistentVolumeClaim, StatefulSet, DaemonSet, NetworkPolicy, explicit strategy, or external LoadBalancer Service appears. The Helm chart templates similar resources, but raw YAML and Helm should not both own the same live objects without a clear rule.

Common mistakes are selector mismatches, direct bare Pods, `latest` images, wrong target ports, hard-coded environment data, assumptions that Ingress installs a controller, missing availability planning, and inconsistent labels copied across resources.

## Review and Troubleshooting

Validate manifests as a resource graph. Namespaces must agree across namespaced objects. A Deployment selector must match template labels, a Service selector must match those Pod labels, target ports must reach the process, and Ingress backends must name the Service and port. One copied label typo can leave a Service with no endpoints even while Pods are healthy.

Review image identity, pull policy, replicas, rollout strategy, probes, resources, configuration references, storage, and security context together. Server-side API validation and policy may reject fields that look like valid YAML, so syntax alone is insufficient. Rendered Helm output needs the same graph review as raw files.

During rollout, distinguish desired replicas, updated replicas, available replicas, and readiness. RollingUpdate capacity needs headroom for surge Pods. Recreate accepts downtime. A Pod may be ready before an Ingress route or DNS exists, and Ingress YAML cannot prove a controller is installed. Namespaces organize resources, but RBAC and network controls must be examined separately.

Evidence statements should remain bounded: committed files prove selectors and declared ports; only cluster observations can prove endpoints, controller behavior, and rollout success. This avoids turning an educational manifest into a production-readiness claim.

## Change Safety

Classify a change as in-place, rollout-triggering, replacement-requiring, or traffic-affecting. Image and Pod-template edits create a rollout; immutable fields may require replacement; Service selector changes can instantly redirect traffic; namespace/name changes create different objects. Review diffs with these consequences, not only YAML syntax.

Deletion and ownership matter when raw manifests, Helm, and Argo CD coexist. Two tools managing the same resource create drift and surprising rollback. Establish one owner and remove obsolete definitions through a reviewed plan. Labels used for operations, cost, and policy should be consistent without accidentally broadening Service selectors.

Availability review includes replica count, readiness, rollout surge/unavailable settings, disruption policy, topology, and capacity. KubeOps demonstrates only some of these. Absence should be recorded, not filled with claims about platform defaults beyond documented Kubernetes behavior.

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
