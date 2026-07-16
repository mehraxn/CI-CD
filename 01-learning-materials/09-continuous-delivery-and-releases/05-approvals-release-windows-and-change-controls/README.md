# Approvals, Release Windows, and Change Controls

## Different Controls

```text
Automated gate:
Evaluates measurable evidence.

Manual approval:
Records a human decision.

Release window:
A planned period when production changes are allowed.

Deployment freeze:
A period when ordinary production changes are restricted.
```

```text
Verified candidate
      ↓
Automated evidence
      ↓
Risk classification
      ↓
Approval when required
      ↓
Release window check
      ↓
Production deployment
```

Release approval decides availability; deployment approval authorizes an environment change. A required reviewer can enforce separation of duties. A change-management process should record risk, candidate identity, evidence, decision, approver, time, and result. Approval timeout and rejection must have explicit outcomes; bypass must be narrow and audited.

Approvals help with regulated changes, destructive operations, major database or infrastructure changes, coordinated launches, and emergency exceptions. Maintenance windows reduce operational conflicts. Release trains and scheduled releases coordinate timing. A deployment freeze needs an emergency-release/hotfix and break-glass process.

Approvals harm when applied to every low-risk change, lack criteria, create queues, encourage large batches, duplicate decisions, or ask people without evidence. This is approval fatigue. Automated gates handle measurable correctness; humans weigh business and exceptional risk. Neither substitutes for the other.

A risk assessment can consider blast radius, reversibility, data changes, customer visibility, compliance, novelty, and time pressure. Low-risk, reversible changes may proceed automatically after gates. High-risk changes may require a reviewer, maintenance window, enhanced monitoring, or rehearsed recovery. The rule should be predictable so teams do not negotiate it during every release.

Approval evidence binds the decision to an immutable candidate and states acceptance criteria. A rejected approval should record why and leave the candidate unchanged. Timeout should fail or pause safely rather than default to approval. Production access and bypass rights should be narrower than ordinary pipeline permissions.

An emergency release or hotfix is faster, not uncontrolled. Break-glass should authenticate the actor, limit scope and duration, preserve logs, notify responders, and require retrospective review. A release freeze without a documented exception path encourages hidden changes; an unrestricted exception makes the freeze meaningless.

## Existing Repository Evidence

TaskOps [CD](../../../Projects/1_project/taskops-cicd/.github/workflows/cd.yml) has automated verification, main-branch trigger, and serialized deployment, but no `environment:` gate, approval, schedule, release window, or change record. KubeOps [Argo CD Application](../../../Projects/2_project/kubeops-gitops/argocd/application.yaml) defaults to manual sync, but source does not prove reviewer requirements or a recorded approval policy.

## Common Mistakes

- Treating approval as testing or approving a mutable artifact.
- Attaching no evidence.
- Allowing unrestricted bypass.
- Combining build, approval, and administration in regulated work.
- Having no emergency policy or freeze exception.
- Encouraging larger releases through slow approval queues.

## Practical Exercise

Classify five scenarios—documentation-only change, routine TaskOps image, destructive schema change, coordinated launch, and urgent vulnerable-image replacement—as `Automated only`, `Manual approval`, `Scheduled window`, `Emergency process`, or `Not enough information`. Explain risk, evidence, production access, and audit needs.

## Knowledge Check

1. Does approval prove correctness?
2. When is separation of duties valuable?
3. Why can approvals increase risk?
4. What must break-glass preserve?
5. Does manual Argo sync prove required reviewers exist?

<details><summary>View answers</summary>

1. No; it records a decision based on evidence.
2. In high-risk or compliance-controlled changes.
3. Queues encourage batching and fatigue encourages rubber-stamping.
4. Narrow authorization, evidence, audit trail, communication, and follow-up.
5. No. The repository shows manual sync only, not external reviewer settings.

</details>

## Navigation

- [Back to Continuous Delivery and Releases](../README.md)
- [Previous: Versioning, Tags, Changelogs, and Release Notes](../04-versioning-tags-changelogs-and-release-notes/)
- [Next: Release Readiness and Post-Release Verification](../06-release-readiness-and-post-release-verification/)
- [Back to All Learning Materials](../../README.md)
