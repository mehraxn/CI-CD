# Kustomize Bases and Overlays

Kustomize composes ordinary YAML through a base and overlays declared in `kustomization.yaml`; it applies patches, name prefixes, labels, namespaces, and image changes without template expressions. Helm renders parameterized templates. Neither is universally better; deep overlays or complex values both become hard to understand.

No Kustomize file exists in this repository. KubeOps uses raw manifests plus Helm values-dev/values-prod, so all examples here are conceptual. An overlay proposal could reuse a base Deployment/Service and patch replicas, namespace, image identity, resources, and ingress per environment—never secret values.

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
