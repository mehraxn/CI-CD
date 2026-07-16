# Database Migrations and Stateful Changes

## State Outlives a Deployment

A database migration changes schema, data, seed data, or reference data. Forward migrations move toward a desired design; down migrations attempt reversal, but cannot restore deleted information automatically. Stateful changes require ownership, backup, restore testing, verification, and monitoring separate from application rollout.

```text
1. Expand:
   Add new schema without removing old schema.

2. Migrate:
   Backfill data and support both formats.

3. Switch:
   Move application reads and writes to the new schema.

4. Contract:
   Remove the old schema only after old versions are gone.
```

```text
Old application + new application
              ↓
Both must work during rolling deployment
              ↓
Database schema must support both temporarily
```

Expand-and-contract uses additive changes and temporary backward/forward compatibility. A column rename becomes: add new nullable column, dual-write, backfill in controlled batches, verify, switch reads, stop old writes, then remove the old column after all old versions are gone. Dual read may ease transition; dual write needs consistency handling.

| Change | Typical risk |
|--------|--------------|
| Add nullable column | Usually lower |
| Add required column without default | High |
| Rename column immediately | High |
| Drop column used by old code | High |
| Add new table | Usually lower |
| Large data backfill | Operationally risky |

Destructive changes make application rollback hard. Large-table and online migrations must consider locks, transactions, load, time, and restartability. A down migration does not resurrect dropped data.

## Execution Options

A dedicated migration job centralizes execution; a pipeline-controlled job orders it with deployment; application-startup migration is convenient but risks every replica racing; operator control adds judgment but less automation; GitOps hooks can order lifecycle work. No option universally wins. Migration jobs need concurrency control, idempotency or locking, failure separation, and clear database ownership.

Migration ordering depends on compatibility. Expand schema before code needs it; deploy dual-compatible code; backfill; verify; switch behavior; only then contract. Forward compatibility lets old code tolerate data/schema written by new code, while backward compatibility lets new code work before migration completes. Rolling deployments need both for the overlap window.

Large-table migrations can hold locks, consume I/O, grow logs, and delay requests. Online techniques use small batches, resumable checkpoints, throttling, and observation. Transactions can make a small change atomic but one huge transaction may increase locks and recovery time. Backfill verification checks counts, nulls, samples, and business invariants before switching reads.

Backups protect pre-change state, but restoring them can overwrite new writes. A rollback plan must distinguish schema reversal, application rollback, and data repair. A down migration may remove new structures but cannot recreate information discarded by a destructive step. Prefer roll-forward repair when irreversible state has already changed.

## Existing Repository Evidence

TaskOps [database.py](../../../Projects/1_project/taskops-cicd/app/database.py) runs `CREATE TABLE IF NOT EXISTS tasks` during initialization and uses a persistent Compose volume. This is initialization, not formal versioned migration tooling. [backup_db.sh](../../../Projects/1_project/taskops-cicd/scripts/backup_db.sh) provides a backup mechanism. KubeOps uses in-memory application storage and has no migration tool or stateful workload. No Alembic, migration job, expand-and-contract workflow, or restore automation is demonstrated.

## Common Mistakes

- Destructive change before new code is stable.
- Every replica running migration concurrently.
- No backup, backfill verification, or lock analysis.
- Mixed versions with incompatible schema.
- Assuming down migration restores data.
- Mixing app and migration failure handling.
- Having no monitoring owner.

## Practical Exercise

Design a hypothetical `title` → `summary` rename for TaskOps using expand, dual-write/backfill, switch, and contract. State compatibility, locking, backup, verification, rollback/roll-forward, ownership, and when removal becomes safe. Do not run it.

## Knowledge Check

1. Why is adding nullable data usually safer than dropping a column?
2. What does expand-and-contract preserve?
3. Why should every replica not migrate independently?
4. Can a down migration restore deleted values?
5. What database behavior exists in TaskOps?

<details><summary>View answers</summary>

1. Old versions can ignore an addition; they fail if required data disappears.
2. Compatibility while old and new versions overlap.
3. Concurrent changes can race, lock, or partially apply.
4. No; restoration needs backup or dedicated repair.
5. SQLite table initialization with persistent storage, not formal versioned migrations.

</details>

## Navigation

- [Back to Deployment Strategies and Recovery](../README.md)
- [Previous: Rollback, Roll-Forward, and Failure Recovery](../06-rollback-roll-forward-and-failure-recovery/)
- [Back to All Learning Materials](../../README.md)
