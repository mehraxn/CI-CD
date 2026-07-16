# Multi-Environment and Multi-Cluster Delivery

| Approach | Strength | Main risk |
|----------|----------|-----------|
| Directory per environment | Clear differences | Duplication |
| Values per environment | Good with Helm | Values complexity |
| Overlay per environment | Patch reuse | Overlay depth |
| Branch per environment | Separation | Merge/drift problems |
| Repository per environment | Ownership separation | More management |

Promote by changing Git to an approved tag/digest, never rebuilding per cluster. Controlled pull requests record environment versions. Multi-cluster delivery adds registrations/credentials, policies, RBAC, CRD differences, region dependencies, shared services, tenant/namespace isolation, availability, disaster recovery, and fleet blast radius.

```text
One reviewed version → cluster group A → observe → group B → observe → remaining production
```

ApplicationSet and cluster selectors can generate fleet Applications; sync waves order dependencies. They are conceptual here. KubeOps has values-dev/prod but one Application targeting one in-cluster dev namespace. No staging directory, cluster fleet, regional rollout, or DR validation exists.

## Organizing Environments

Development, test, staging, and production should identify the same accepted application content while varying necessary configuration and policy. Promotion changes Git to an approved tag or digest; it should not rebuild per environment or cluster. A pull request records the old and new identity, reviewers, timing, and associated evidence.

Directory-per-environment makes differences visible but can duplicate manifests. Helm values-per-environment reuse templates but may grow into large, hard-to-understand matrices. Kustomize overlay-per-environment keeps patches focused but deep inheritance is confusing. Branch-per-environment creates simple names yet encourages merge divergence and unclear truth. Repository-per-environment can isolate ownership and credentials at the cost of cross-repository coordination.

An environment repository separates application builds from operational promotion. A combined application repository makes code and manifests atomic but may grant developers broader delivery influence. The choice should follow team ownership, review, audit, and failure boundaries. Regardless of layout, record which image identity, chart version, configuration revision, and secret reference each environment uses.

## Multi-Cluster Delivery

A cluster must be registered with the GitOps controller through a protected credential or workload identity. ApplicationSet can generate one Application per selected cluster, and cluster labels can select region, environment, or rollout ring. This improves fleet consistency but expands permission and blast-radius concerns. One controller credential should not casually control every cluster.

```text
One reviewed application version
        |
Cluster group A
        | observe
Cluster group B
        | observe
Remaining production clusters
```

Progressive fleet delivery begins with a limited ring, observes technical and business signals, then advances. Regional rollout accounts for latency, dependencies, data location, and provider incidents. Sync waves can order shared prerequisites and applications, but dependency ordering is not readiness. Shared services, CRD versions, admission policies, network rules, storage classes, and external endpoints may differ between clusters.

Namespace isolation organizes tenants but is not complete isolation. RBAC, NetworkPolicy, admission policy, quotas, nodes, credentials, and sometimes separate clusters are needed. Disaster recovery requires tested restoration of Git access, controller state/configuration, cluster resources, external data, and secrets. Merely declaring a second region is not validated recovery.

Risks include environment-specific manual changes, inconsistent secrets, one fleet-wide credential, a bad change targeting every cluster, chart-structure drift, different CRDs, region-specific dependencies, and untested failover. Policy can restrict destinations and resources, while staged pull requests and rollout rings reduce blast radius.

## Image Promotion Example

A conceptual promotion begins when CI publishes `ghcr.io/example/kubeops:sha-abc123` and records its digest. Development values are updated through review and reconciled. After observation, staging and then production Git references are updated to that same digest. The image is never rebuilt. Each promotion is reversible at the configuration level, though database and external-state compatibility still determine safe recovery.

Automated image updaters can propose changes, but must select only verified images, preserve review for production, avoid tag races, and record identity. No image updater is configured here.

## Actual KubeOps Structure

KubeOps has [values-dev.yaml](../../../Projects/2_project/kubeops-gitops/helm/kubeops/values-dev.yaml) and [values-prod.yaml](../../../Projects/2_project/kubeops-gitops/helm/kubeops/values-prod.yaml) beside shared defaults and templates. This is a real values-per-environment approach for development and production. Dev uses a local image, two replicas, debug logging, and `kubeops.local`. Prod requests three replicas, a GHCR `latest` image, nginx Ingress, higher resources, and an existing Secret.

Only one [Argo CD Application](../../../Projects/2_project/kubeops-gitops/argocd/application.yaml) exists. It selects dev values and targets `kubeops-dev` in the in-cluster destination. There is no production Application, staging values, environment directory tree, ApplicationSet, cluster selector, second cluster credential, region, rollout ring, fleet policy, or disaster-recovery validation. The two values files do not prove either environment is deployed.

A conceptual improvement could retain the Helm chart, add reviewed immutable image values for dev/staging/prod, and declare separate Applications or an ApplicationSet with narrowly scoped destinations. That is a design exercise only; no such executable files were created.

## Promotion Record and Safety Checks

Each promotion record should identify source environment, target environment, image digest, chart/configuration revision, approval, observation window, and result. Cluster fan-out should be explicit: which ring receives the change, what signals pause advancement, and who authorizes continuation. Reusing the same digest makes differences attributable to configuration or platform rather than rebuilt content.

Before fleet rollout, compare Kubernetes versions, CRDs, policies, storage classes, ingress, secrets, and regional dependencies. Validate controller permissions and cluster selectors so a label error cannot target the wrong fleet. Limit credentials and controller scope to contain blast radius. Shared services and data replication need their own recovery plan.

Environment drift can exist in Git structure, rendered manifests, or live clusters. Review all three. A successful dev sync does not prove production values or cluster integrations. Disaster recovery claims require exercises that restore both declarative resources and external state; a second values file is not recovery evidence.

## Ownership at Scale

Assign owners for the shared chart/base, each environment's overrides, cluster registration, fleet policy, secrets, and promotion approval. ApplicationSet generation reduces repetition but can multiply a mistake; generated output and selectors need review like handwritten Applications. A cluster removed from a generator also needs an intentional decommission policy.

## Practical Exercise
Design a KubeOps directory/values promotion proposal and label real versus conceptual resources, credentials, policies, and clusters.
## Knowledge Check
1. Rebuild per cluster? 2. Main branch-per-env risk? 3. Multi-cluster concern? 4. How many real targets here?
<details><summary>Answers</summary>
1. No. 2. Merge/drift. 3. Credentials/policy/blast radius. 4. One declared in-cluster dev destination.
</details>
## Navigation
- [Back to Kubernetes and GitOps](../README.md)
- [Previous: Argo CD Applications, Sync, and Drift](../07-argo-cd-applications-sync-and-drift/)
- [Back to All Learning Materials](../../README.md)
