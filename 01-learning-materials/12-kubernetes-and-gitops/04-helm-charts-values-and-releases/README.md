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

## Chart Review Workflow

Review begins with chart metadata and declared dependencies, then default values, environment overrides, and every template consumer. Trace each important value to rendered YAML and identify unused or misspelled values. Render each supported environment and compare resource names, namespaces, selectors, images, Secret behavior, probes, and resources. A values schema can catch type errors before cluster submission.

Release planning records chart version, application/image identity, values revision, namespace, and rendered diff. An upgrade can replace workload objects while leaving external data unchanged. Hook jobs and CRDs need special lifecycle rules. Rollback reuses a prior Helm revision but does not reverse database migrations, external APIs, or secret rotation.

Avoid passing sensitive values through source control or observable command lines. Prefer references to provisioned Secrets or an integrated protected mechanism. Remember Helm release data may contain rendered configuration. Review RBAC around release storage and access.

GitOps changes ownership: Argo CD can render the chart from Git, while direct `helm upgrade` becomes an out-of-band change that may be reported or reverted. Pick one normal owner. Repository docs show both learning paths, but the Application is the declared GitOps path for dev.

## Values and Ownership Discipline

Every value should have a type, safe default, owner, and documented environment behavior. Avoid exposing raw Kubernetes structure as values without a stable contract; consumers then depend on template internals. Helpers should centralize repeated naming and labels, not hide major control flow.

Before release, compare rendered output against the prior revision and validate API compatibility. After release, pair Helm status with Kubernetes rollout and application checks. A successful Helm operation can still produce an unhealthy application. Store enough evidence to connect release revision, chart version, app/image version, values revision, and rendered digest.

If Argo CD owns the Helm source, changes should flow through Git. Direct Helm commands may create drift and conflicting history. Emergency use needs reconciliation back into the declared source and clear ownership of the resulting release state.

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
