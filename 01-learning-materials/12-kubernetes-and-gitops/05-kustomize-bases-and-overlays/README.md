# Kustomize Bases and Overlays

Kustomize composes ordinary YAML through a base and overlays declared in `kustomization.yaml`; it applies patches, name prefixes, labels, namespaces, and image changes without template expressions. Helm renders parameterized templates. Neither is universally better; deep overlays or complex values both become hard to understand.

No Kustomize file exists in this repository. KubeOps uses raw manifests plus Helm values-dev/values-prod, so all examples here are conceptual. An overlay proposal could reuse a base Deployment/Service and patch replicas, namespace, image identity, resources, and ingress per environment—never secret values.

## Composition Model

A base holds reusable resources without assuming one environment. An overlay references that base and applies a small set of transformations for development, staging, or production. `kustomization.yaml` is a declarative inventory and transformation file. Rendering produces ordinary YAML; it does not install a release object.

Conceptual layout—no such files exist in this repository:

```text
base/
|-- deployment.yaml
|-- service.yaml
`-- kustomization.yaml
overlays/
|-- staging/kustomization.yaml
`-- production/kustomization.yaml
```

Conceptual base:

```yaml
resources:
  - deployment.yaml
  - service.yaml
```

Conceptual production overlay:

```yaml
resources:
  - ../../base
namespace: production
images:
  - name: ghcr.io/example/task-api
    newTag: "1.4.0"
patches:
  - path: replicas.yaml
```

`resources` composes files or another kustomization. Name prefixes/suffixes, common labels, namespace, and image overrides can transform resources consistently. Patches express targeted differences. Strategic-merge style patches match Kubernetes object structure, while JSON patch operations address precise paths; current Kustomize syntax should be validated for the installed version before use. Deep patches tied to fragile array positions are hard to maintain.

ConfigMap and Secret generators create resources from literals or files. Generated name hashes help trigger workload updates when content changes. Real secret input must still come from a protected source; a generator does not make committed plaintext safe. `kubectl kustomize` renders, while `kubectl apply -k` renders and applies. These commands are concepts only here and were not run.

## Helm Comparison

| Area | Helm | Kustomize |
|------|------|-----------|
| Main method | Templates and values | Bases and patches |
| Packaging | Versioned chart | Directory composition |
| Logic | Template functions | Declarative transformations |
| Release tracking | Helm release objects | External tooling/controller |

Helm suits reusable parameterized packages and release history. Kustomize suits composition of recognizable YAML with focused environment changes. Neither is universally superior. Some systems render Helm and then apply Kustomize, but mixed ownership should be explicit so operators know where each field originates and which tool records lifecycle.

## Conceptual KubeOps Split

Repository search finds no `kustomization.yaml`; Kustomize is absent. KubeOps instead has [raw manifests](../../../Projects/2_project/kubeops-gitops/k8s/) plus a [Helm chart](../../../Projects/2_project/kubeops-gitops/helm/kubeops/). A conceptual base could contain the Deployment, Service, ConfigMap, and Ingress structure. A dev overlay could set namespace `kubeops-dev`, local image, two replicas, debug logging, and `kubeops.local`. A production overlay could set a production namespace, accepted GHCR identity, three replicas, resource changes, nginx host/class, and an external Secret reference.

The base should not contain dev-specific namespace names, `kubeops:local`, or real credentials. Overlays should patch only differences, not copy every manifest. Image override is essential for promotion. Rendered dev and prod output should be reviewed for selectors, namespace consistency, secret references, probes, and immutable image identity.

This design is deliberately not implemented because the task prohibits creating Kustomize files and the project already uses Helm values for environment variation. It teaches the alternative without implying repository support.

Common mistakes include duplicating full manifests, fragile patches, committed secret-generator input, environment data in the base, forgotten image overrides, deep overlay inheritance, never reviewing output, and mixing Helm/Kustomize without clear ownership. Drift is still possible if rendered resources are changed manually or the GitOps controller does not reconcile them.

## Practical Exercise
Design a file-only KubeOps base/dev/prod overlay tree and map what would remain common versus patched. Do not create it.
## Knowledge Check
1. Templates in Kustomize? 2. Base purpose? 3. Overlay risk? 4. Implemented here?
<details><summary>Answers</summary>
1. No template expressions. 2. Shared resources. 3. Patch-depth confusion. 4. No.
</details>
## Navigation
- [Back to Kubernetes and GitOps](../README.md)
- [Previous: Helm Charts, Values, and Releases](../04-helm-charts-values-and-releases/)
- [Next: GitOps Principles and Reconciliation](../06-gitops-principles-and-reconciliation/)
- [Back to All Learning Materials](../../README.md)
