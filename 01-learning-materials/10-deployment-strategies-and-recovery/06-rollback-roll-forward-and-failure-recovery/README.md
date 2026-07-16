# Rollback, Roll-Forward, and Failure Recovery

## Recovery Actions

```text
Rollback:
Return to a previously known version or state.

Roll-forward:
Deploy a corrective change that fixes the current version.

Git revert:
Create a source-control commit that reverses earlier source changes.

Artifact rollback:
Redeploy a previously verified artifact.
```

Git revert changes source history; production changes only after a deployment or reconciliation. Rollback may restore a previous artifact, switch blue-green traffic, or disable a flag. Data restoration is separate and needs backups and a tested restore plan.

| Situation | Possible response |
|-----------|-------------------|
| New code has a simple isolated bug | Roll forward |
| New version fails immediately and old version is compatible | Roll back |
| Feature causes harm but deployment is otherwise healthy | Disable feature flag |
| Database schema is incompatible with old code | Roll forward may be safer |
| Data was corrupted | Restore or repair data using a dedicated recovery plan |

Recovery criteria consider blast radius, severity, recovery time, error budget, compatibility, confidence, and partial-failure state. Declare an incident when agreed impact thresholds are crossed; freeze further ordinary change, communicate ownership and status, and record every action. Idempotent deployment and reconciliation make retries safer. Recovery drills test runbooks before pressure.

Rollback may fail because migration or data is irreversible, infrastructure vanished, configuration or external APIs changed, the old artifact expired, background work already acted, or the old image is vulnerable. Roll-forward must also be verified.

A deployment failure means the intended technical change did not complete; a release failure means user or business acceptance failed, even if deployment succeeded. Partial failure requires reconciling which instances, resources, configuration, and data actually changed before acting. Repeating a non-idempotent deploy blindly can worsen it.

Rollback criteria favor a known-compatible old artifact, rapid broad impact, and low state-change risk. Roll-forward criteria favor an isolated understood defect, a small tested fix, or state already incompatible with old code. Error budget and blast radius can define when experimentation stops and incident recovery begins. A freeze prevents unrelated changes from obscuring recovery.

Backups are useful only with restore tests and recovery-time expectations. Data restoration may discard valid writes after the backup, so it needs a separate business decision. Audit records should include observations, decisions, actors, commands/results, artifact identities, communication, and final verification. Recovery drills reveal expired images, missing access, stale runbooks, and unrealistic timings.

## Existing Repository Evidence

[TaskOps deploy.sh](../../../Projects/1_project/taskops-cicd/scripts/deploy.sh) records the previous image tag. [rollback.sh](../../../Projects/1_project/taskops-cicd/scripts/rollback.sh) rewrites `IMAGE_TAG`, redeploys with Compose, and checks health. It is an artifact-tag rollback, not Git revert, and it assumes the old image and database remain compatible. [KubeOps GitOps documentation](../../../Projects/2_project/kubeops-gitops/docs/gitops.md) describes Git revert/Argo history; [Helm documentation](../../../Projects/2_project/kubeops-gitops/docs/helm.md) documents `helm rollback`. Documentation does not prove these recovery paths were drilled.

## Common Mistakes

- Assuming rollback always works or deleting prior artifacts.
- Rolling back code but not configuration.
- Reverting Git without deploying.
- Skipping verification, communication, or audit.
- Restoring an old vulnerable image.

## Practical Exercise

Define TaskOps rollback and roll-forward criteria: symptoms, decision owner, compatible database/config checks, old identity, verification, maximum recovery time, communication, and when the previous image must not be restored. Do not execute recovery.

## Knowledge Check

1. Why is Git revert not production rollback?
2. When may roll-forward be safer?
3. What does TaskOps rollback preserve?
4. Why test restores?
5. Can flag disablement repair corrupted data?

<details><summary>View answers</summary>

1. It changes source only; production must be redeployed or reconciled.
2. When state/schema is incompatible with the old version.
3. The previously deployed image tag.
4. An untested backup may be incomplete or unusable.
5. No; it can stop further feature exposure but needs data repair/restoration.

</details>

## Navigation

- [Back to Deployment Strategies and Recovery](../README.md)
- [Previous: Health Checks, Zero Downtime, and Traffic Management](../05-health-checks-zero-downtime-and-traffic-management/)
- [Next: Database Migrations and Stateful Changes](../07-database-migrations-and-stateful-changes/)
- [Back to All Learning Materials](../../README.md)
