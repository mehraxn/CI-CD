# Helm Charts, Values, and Releases

Helm packages templates, defaults, metadata, and helpers as a chart. `Chart.yaml` has chart version and appVersion—different concepts. `values.yaml` supplies defaults; environment values override them; templates render manifests. A Helm release is an installed chart instance/revision, not a software release by itself.

KubeOps chart contains Deployment, Service, Ingress, ConfigMap, Secret, and ServiceAccount templates plus dev/prod values. Production changes image, replicas, resources, ingress, and secret handling. `helm upgrade --install` and rollback are documented; rollback does not reverse data. No hooks or packaged chart registry exists.

## Rendering and Release Model

```text
Chart templates
      +
Default values
      +
Environment overrides
      |
Rendered Kubernetes manifests
```

`Chart.yaml` describes the chart package. `version` is the chart's package version; `appVersion` describes the application version it packages. They may change independently—for example, a template fix can increment the chart without changing application code. A dependency chart or subchart packages another component and can receive scoped values. Charts may also be stored as OCI artifacts, but this repository does not package or publish its chart.

`values.yaml` provides defaults. Later files and command-line overrides take precedence, so operators need a documented order. Templates use Go-template expressions and objects such as `.Values`, `.Release`, and `.Chart`. `.Release` describes the installed release instance; `.Chart` exposes metadata. Named templates in helper files centralize names and labels. Excessive conditional logic makes rendered behavior difficult to review.

This educational example uses a placeholder registry:

```yaml
replicaCount: 2
image:
  repository: ghcr.io/example/task-api
  tag: "1.4.0"
service:
  port: 80
```

```yaml
spec:
  replicas: {{ .Values.replicaCount }}
  template:
    spec:
      containers:
        - name: application
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
```

Rendering combines these into ordinary Kubernetes YAML. Linting checks chart structure and common template errors; template/dry-run output should be reviewed and schema-validated where possible. A `values.schema.json` can constrain types and required values, but KubeOps has no values schema.

Installing creates a named Helm release in a namespace. Upgrade renders a new revision and applies changes. History records revisions, and rollback reapplies an earlier release revision. It does not restore databases, external systems, or deleted data. Hooks can run lifecycle jobs, and test hooks can verify a release; hooks require ordering, cleanup, and failure policy. No hooks appear here.

Real secrets should never be placed in committed values. A chart can reference a pre-provisioned Secret, integrate with an external mechanism, or accept protected runtime values. Supplying a secret on a command line can leak through history or process inspection. Rendered output and release storage also need threat review.

## KubeOps Chart Map

KubeOps [Chart.yaml](../../../Projects/2_project/kubeops-gitops/helm/kubeops/Chart.yaml) defines an application chart named `kubeops`, version `0.1.0`, and appVersion `0.1.0`. [Defaults](../../../Projects/2_project/kubeops-gitops/helm/kubeops/values.yaml) specify two replicas, local image/tag, ClusterIP service, enabled Ingress, environment variables, a placeholder secret option, probes, requests/limits, security context, and ServiceAccount creation.

The [Deployment template](../../../Projects/2_project/kubeops-gitops/helm/kubeops/templates/deployment.yaml) maps `.Values.replicaCount` to replicas, repository/tag to `image`, service port settings, probes, resources, and security context. [Helpers](../../../Projects/2_project/kubeops-gitops/helm/kubeops/templates/_helpers.tpl) generate consistent names and labels. Service, Ingress, ConfigMap, Secret, and ServiceAccount each have templates.

[Development values](../../../Projects/2_project/kubeops-gitops/helm/kubeops/values-dev.yaml) retain two local replicas, enable debug logging, and use `kubeops.local`. [Production values](../../../Projects/2_project/kubeops-gitops/helm/kubeops/values-prod.yaml) request three replicas, a GHCR repository, `latest`, nginx Ingress, larger resources, and an existing Secret. The mutable tag is documented as needing immutable replacement in a real deployment.

Project scripts and docs show `helm upgrade --install`, rollback, linting, and template/dry-run guidance. Files do not prove any release exists. Hooks, test hooks, dependencies, subcharts, OCI chart publishing, packaged archives, and values schema are absent. Common mistakes include one enormous values file, committed secrets, confused versions, excessive logic, mutable images, unreviewed output, and assuming Helm rollback restores external data.

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
