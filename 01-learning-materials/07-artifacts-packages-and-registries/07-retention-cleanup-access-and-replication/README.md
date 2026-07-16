# Retention, Cleanup, Access, and Replication

## How Long Should Outputs Live?

Neither extreme works:

```text
Keep forever:
Usually inappropriate for every CI artifact.

Delete immediately:
Unsafe for release, audit, and rollback evidence.

Good retention:
Depends on artifact purpose, environment, risk, compliance, and cost.
```

A **retention policy** encodes that judgment per output type — by **artifact age**, **version count** (keep the last N), or protected status. Some retention is externally imposed: **legal and audit retention** requirements can mandate keeping security evidence for years, while a **rollback window** demands that recently deployed versions stay restorable.

| Output type | Example retention consideration |
|-------------|---------------------------------|
| Pull-request logs | Short-lived debugging value |
| Test reports | Useful for trends and investigations |
| Release artifacts | Keep for support and rollback |
| Production images | Keep while deployed or supported |
| Caches | Delete when stale or oversized |
| Security evidence | Keep according to audit policy |

## Safe Cleanup

Cleanup is a destructive operation against your own delivery history, so it needs the same care as a deployment:

- **Protect active production artifacts** — identify deployed versions before deleting anything; a **protected release** flag beats hoping the age filter misses it.
- **Preserve rollback versions** — the previous deployed identity is not garbage.
- **Dry-run first** — report what *would* be deleted; review before enabling.
- **Audit deletions** — who deleted what, when, under which policy.
- **Never delete by age alone** — a two-year-old image may be the currently deployed one.
- **Coordinate with deployments** — registry cleanup that races a deployment pulls the rug out mid-rollout.
- Registry-specific mechanics: deleting manifests leaves **orphaned layers** until **garbage collection** runs; storage **quotas** force the issue if policy doesn't.

## Access Control

Registry and artifact permissions follow least privilege, and the verbs matter: **read** (consumers, deploy targets), **write** (the publishing pipeline only), **delete** (almost nobody — CI rarely needs it, and a compromised pipeline with delete rights can erase your rollback path), and **administrative** (humans, few, audited). Public versus private visibility is a separate axis: public artifacts are a distribution choice; private artifacts still need internal least privilege — and secret-bearing debug bundles should never have been uploaded in the first place.

## Replication, Backup, and Availability

**Replication** copies artifacts across regions or registries for latency, availability, and **disaster recovery**. It is not the same as **backup**: replication faithfully copies your mistakes — a deletion or corruption replicates too. Backup means restorable point-in-time copies, and **restore** must be tested, not assumed. Plan for **registry outages** (can you deploy? can CI build?) — a pull-through cache or mirror keeps **dependency availability** when upstream is down. All of it costs money: **cost management** is retention policy's constant companion, since "keep everything replicated everywhere" is a bill, not a strategy.

## Common Mistakes

- Deleting deployed images.
- Letting every pipeline artifact live forever.
- Giving CI delete permission unnecessarily.
- Sharing private artifacts publicly.
- Retaining secret-bearing debug bundles.
- Cleanup without audit logs.
- No disaster-recovery plan for the registry.
- Assuming replication is the same as backup.
- Keeping vulnerable artifacts without clear status.

## Existing Repository Evidence

The repository has **no explicit retention configuration** — no GHCR cleanup policies, no artifact retention settings (there are no pipeline artifacts to retain), no replication. What exists implicitly: every SHA-tagged image pushed by [TaskOps CD](../../../Projects/1_project/taskops-cicd/.github/workflows/cd.yml) and [KubeOps image release](../../../Projects/2_project/kubeops-gitops/.github/workflows/image-release.yml) accumulates in GHCR indefinitely (one image per `main` commit), the BuildKit `type=gha` caches are managed by GitHub's automatic cache eviction, and the TaskOps [deploy script's](../../../Projects/1_project/taskops-cicd/scripts/deploy.sh) `.previous_tag` state file defines a minimal one-version rollback window that any cleanup policy would need to respect. Access follows the platform defaults: `GITHUB_TOKEN` receives write (never delete) via `permissions`, and image visibility is a GHCR setting not visible in source — so this material makes no claim about it.

## Practical Exercise

Propose retention categories for this repository's real outputs. For each — per-commit GHCR images (both projects), the `latest` tags, BuildKit caches, pip caches, job logs, and the `.previous_tag` rollback state — specify:

```text
Output
Proposed retention rule
What must be protected from the rule
Who should hold delete rights
What evidence a deletion should leave
```

Pay special attention to the images: propose a keep-last-N-plus-deployed rule and explain how "deployed" would be determined for TaskOps (hint: the state file) and for KubeOps (hint: what does values-prod reference?). Do not implement anything. Target 20–30 minutes.

## Knowledge Check

1. Why is "delete everything older than X" unsafe for images?
2. Why should CI publishing identities lack delete permission?
3. What is the difference between replication and backup?
4. What are orphaned layers?
5. What makes a cleanup process auditable?
6. What implicit retention behavior does this repository have today?

<details>
<summary>View answers</summary>

1. Age says nothing about deployment status — an old image may be the one currently running or the designated rollback target.
2. Publishing needs write only; delete rights turn a compromised pipeline into a tool for erasing rollback paths and history.
3. Replication copies current state (including mistakes) for availability; backup preserves restorable point-in-time copies.
4. Layer blobs left in registry storage after their referencing manifests are deleted, reclaimed only by garbage collection.
5. Dry-run reports before action, logged deletions with actor and policy, and protection rules for deployed/rollback artifacts.
6. Images accumulate in GHCR indefinitely (one per main commit), GitHub evicts BuildKit/pip caches automatically, and the deploy script keeps a one-version rollback record.

</details>

## Navigation

- [Back to Artifacts, Packages, and Registries](../README.md)
- [Previous: Immutability, Promotion, and Release Bundles](../06-immutability-promotion-and-release-bundles/)
- [Back to All Learning Materials](../../README.md)
