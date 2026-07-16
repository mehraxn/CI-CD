# Helm Charts, Values, and Releases

Helm packages templates, defaults, metadata, and helpers as a chart. `Chart.yaml` has chart version and appVersion—different concepts. `values.yaml` supplies defaults; environment values override them; templates render manifests. A Helm release is an installed chart instance/revision, not a software release by itself.

KubeOps chart contains Deployment, Service, Ingress, ConfigMap, Secret, and ServiceAccount templates plus dev/prod values. Production changes image, replicas, resources, ingress, and secret handling. `helm upgrade --install` and rollback are documented; rollback does not reverse data. No hooks or packaged chart registry exists.

## Practical Exercise
Trace five values from values-prod into templates and resulting resources.
## Knowledge Check
1. Chart version versus appVersion? 2. Values purpose? 3. Helm rollback data rollback? 4. Hooks present?
<details><summary>Answers</summary>
1. Package versus application identity. 2. Template inputs. 3. No. 4. No.
</details>
## Navigation
- [Back to Kubernetes and GitOps](../README.md)
- [Previous: ConfigMaps, Secrets, Probes, and Resources](../03-configmaps-secrets-probes-and-resources/)
- [Next: Kustomize Bases and Overlays](../05-kustomize-bases-and-overlays/)
- [Back to All Learning Materials](../../README.md)
