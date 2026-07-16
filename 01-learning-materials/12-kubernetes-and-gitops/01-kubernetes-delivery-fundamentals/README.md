# Kubernetes Delivery Fundamentals

A cluster contains a control plane and worker nodes. The API stores desired state; scheduler places Pods; controllers run reconciliation loops comparing actual state and creating/replacing resources. Pods are ephemeral and normally managed through Deployments/ReplicaSets rather than directly.

CI builds/verifies an image; delivery updates declarative image/configuration; Kubernetes pulls it and maintains replicas. Self-healing restarts/replaces resources but cannot prove business correctness. Namespaces organize names/access but are not complete isolation.

KubeOps is the repository example: raw YAML, Helm, and Argo CD target one in-cluster development namespace. No real cluster state is inferable from files.

## Cluster Components and Reconciliation

The Kubernetes API server is the entry point for desired state. Data is persisted by the control plane, and controllers watch resources for changes. The scheduler chooses a suitable worker node for an unscheduled Pod based on requests, constraints, and available capacity. A node agent then asks the container runtime to pull images and run containers. Users normally declare resources through YAML or API clients rather than choosing nodes directly.

A reconciliation loop compares desired and observed state. If a Deployment requests two replicas and only one suitable Pod exists, its controllers work through a ReplicaSet to create another. If a Pod disappears, a replacement may be created with a new identity. This is why long-lived workloads are normally managed by Deployments, StatefulSets, or other controllers rather than bare Pods.

```text
Desired Deployment
    | API server
Deployment controller
    | ReplicaSet
Pod template
    | scheduler selects node
Container runtime pulls image and starts containers
```

Declarative does not mean static. Operators change the declaration; controllers converge toward it. Actual state can lag during image pulls, scheduling, termination, or failure. Status fields and events describe observations, while `spec` expresses intent. Reconciliation is continuous, but a controller cannot know whether an incorrect desired replica count or broken application logic is business-correct.

## Delivery Responsibilities

CI should build, test, scan, and publish a traceable image. A delivery change should update a manifest, Helm value, or overlay to reference that accepted identity. Kubernetes then pulls it according to image and credential policy. Configuration and secrets are supplied separately. Readiness gates traffic, liveness handles stuck processes, and resource declarations help scheduling and containment.

```text
Source -> verified image -> reviewed desired-state change
       -> Kubernetes API -> Deployment -> ReplicaSet -> Pods -> Service
```

Build once remains important: rebuilding for each namespace or cluster creates different content. A tag can move, so production designs often record or pin a digest. The repository KubeOps production values still use `latest`; immutable promotion is a recommendation, not implemented behavior.

Pods are ephemeral scheduling units and can contain one or more tightly coupled containers sharing network and selected volumes. Containers in a Pod share the Pod IP. A Service provides stable discovery across changing Pod identities. Ingress describes HTTP routing, but an Ingress controller must exist separately. Persistent state requires PersistentVolumes, claims, or an external service; none is defined in KubeOps.

Namespaces scope names and many access/policy objects. They help organize development and production or teams, but they are not complete security boundaries. NetworkPolicy, RBAC, admission policy, node isolation, and credential design still matter. A cluster is control plane plus worker nodes; a namespace is not a miniature independent cluster.

## Repository Evidence and Limits

KubeOps [Deployment](../../../Projects/2_project/kubeops-gitops/k8s/deployment.yaml) requests two replicas in `kubeops-dev`, uses matching `app: kubeops` labels, and references `kubeops:local`. The [Service](../../../Projects/2_project/kubeops-gitops/k8s/service.yaml) selects those Pods and maps port 80 to 8000. The [namespace](../../../Projects/2_project/kubeops-gitops/k8s/namespace.yaml), configuration, placeholder Secret, probes, resources, and Ingress complete a learning set.

The [Helm chart](../../../Projects/2_project/kubeops-gitops/helm/kubeops/) can render equivalent objects from values. The [Argo CD Application](../../../Projects/2_project/kubeops-gitops/argocd/application.yaml) declares a pull-based source and destination, but manual sync is active. Files prove declared desired state, not that a cluster, controller, Pods, or successful endpoint currently exists. Project documentation includes manual `kubectl` and Helm paths as alternatives; do not confuse examples with observed deployment.

Common errors include managing bare Pods, mismatched labels, assuming self-healing fixes application bugs, using mutable images without traceability, placing secrets in plain configuration, omitting resources, and treating namespace separation as full tenancy security.

## Operational Reasoning

When a workload fails, separate declaration, scheduling, image pull, container startup, readiness, routing, and application behavior. A Pending Pod can indicate capacity or constraints; an image-pull error differs from a crashing process; a Running Pod can still be unready; a ready endpoint can still fail business tests. Controllers report and act on platform observations but do not replace layered diagnosis.

Delivery evidence should connect an image digest and Git revision to Deployment rollout status, Pod readiness, Service endpoints, and an external smoke test. Events and status are transient observations, so retain the relevant result with the pipeline or release record. Avoid editing live resources as the normal fix; update declarative state and let reconciliation establish a reviewable history.

Availability also depends on replicas, disruption, topology, resources, probes, and capacity. Two replicas in YAML do not prove they occupy separate failure domains or can both run during an update. Kubernetes supplies mechanisms, while the delivery design supplies correct values and verification.

## Delivery Decision Record

For each workload, document the managing controller, image identity, configuration sources, storage ownership, exposed Service, readiness contract, resource basis, and recovery path. This makes desired state reviewable as an operating model rather than a pile of YAML.

Controllers act asynchronously. A pipeline should wait for a bounded rollout outcome and then test user-visible behavior; merely accepting an API request is not delivery success. On timeout, retain events and status before a later reconciliation changes them. Manual live edits should be exceptional because they obscure which declaration is authoritative.

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
