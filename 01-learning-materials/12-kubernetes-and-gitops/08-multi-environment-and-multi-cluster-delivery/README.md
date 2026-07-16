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
