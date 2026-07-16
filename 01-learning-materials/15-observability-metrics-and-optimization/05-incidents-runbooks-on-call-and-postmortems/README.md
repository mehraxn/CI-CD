# Incidents, Runbooks, On-Call, and Postmortems

## Three Artifacts of Operational Maturity

```text
Runbook:
Instructions for a known operational task or response.

Incident:
An event that significantly affects service or requires coordinated response.

Postmortem:
A structured review of what happened, why, and how to improve.
```

Not every **alert** or **event** is an incident — an incident earns the name through impact (an **outage** or serious **degradation**) or the need for coordinated response, graded by **severity**. **On-call** is the staffing model that guarantees someone answers, with **escalation** paths when they need help.

## Running an Incident

```text
Alert or report
      ↓
Validate impact
      ↓
Assign coordination and responders
      ↓
Mitigate
      ↓
Communicate
      ↓
Restore service
      ↓
Review and improve
```

Roles keep it sane: an **incident commander** coordinates (decides, delegates, communicates) while **responders** investigate and fix — merging the roles is how incidents drown their own coordinator. **Mitigation** (stop the bleeding: roll back, feature-off, scale up) precedes root-causing; **containment** limits spread; **resolution and recovery** restore normal service. Throughout: **status updates** on a cadence, a **timeline** recorded as events happen (memory rewrites itself within hours — and every change made during the incident goes in it), and deployment/artifact identities noted, because "which version were we even running?" is a terrible question to ask afterward.

## Runbooks

A runbook is pre-decided thinking for a known situation: symptom, checks, actions, verification, escalation. The best runbooks are executable or near-executable — a script *is* a runbook with the judgment already encoded. Every paging alert should link to one (**playbooks** and troubleshooting guides are the same family, broader in scope; **rollback and restore procedures** are the most safety-critical members). Runbooks rot: **recovery drills** and **game days** — practicing failure on purpose — are how you find out the restore procedure stopped working *before* 3 a.m. does.

## Postmortems

A **blameless postmortem** examines systems, decisions, and conditions — not culprits:

```markdown
# Incident Postmortem

## Summary

## Impact

## Detection

## Timeline

## Contributing Factors

## What Worked

## What Did Not Work

## Resolution

## Corrective Actions

| Action | Owner | Due date |
|--------|-------|----------|
```

Blameless does not mean consequence-free: accountability remains, actions still get **owners and due dates**, and reasonable decisions that turned out badly are not punished — because punishing them teaches people to hide the next one. "**Human error**" is where analysis starts, not ends: *why* was the erroneous action possible, plausible, and unchecked? Note the plural — **contributing factors**, not a single **root cause**; real failures are conjunctions. Corrective actions split usefully into **recurrence prevention** and **detection improvement** (could we have noticed in one minute instead of forty?).

## Common Mistakes

- Alerts with no runbook.
- No incident owner — everyone responding, no one coordinating.
- Changes made during the incident but never recorded.
- Postmortems only for severe outages (near-misses teach cheaper).
- "Human error" as the final explanation.
- Action items without owners (they evaporate).
- Permanent temporary fixes.
- No follow-up on last quarter's actions.
- No deployment or artifact identity in the timeline.
- Sensitive data copied into widely shared incident documents.

## Existing Repository Evidence

The repository's operational scripts are **runbooks in executable form**: [deploy.sh](../../../Projects/1_project/taskops-cicd/scripts/deploy.sh) encodes the deployment procedure including health verification and recording the previous tag; [rollback.sh](../../../Projects/1_project/taskops-cicd/scripts/rollback.sh) encodes recovery to that recorded identity; [backup_db.sh](../../../Projects/1_project/taskops-cicd/scripts/backup_db.sh) covers data protection; [smoke_test.sh](../../../Projects/1_project/taskops-cicd/scripts/smoke_test.sh) is the verification step both CD and a human responder would run. KubeOps adds [check-health.ps1](../../../Projects/2_project/kubeops-gitops/scripts/) and operational documentation in [docs/monitoring.md](../../../Projects/2_project/kubeops-gitops/docs/monitoring.md) (logs, describe, events, probe behavior — troubleshooting-guide material). No written incident process, on-call arrangement, or postmortem exists — expected for a portfolio repository, and exactly what the exercise drafts.

## Practical Exercise

Write a one-page conceptual runbook: **"TaskOps production deployment failed its smoke test."** Include:

1. Symptom and how it announces itself (which workflow step, what evidence).
2. First checks, in order (think: container logs, image identity via the SHA tag, server state).
3. Decision point: retry, roll back (name the exact script and what it relies on), or investigate live.
4. Verification after action (which endpoint, what response).
5. Escalation and communication (adapt honestly to a one-person project).
6. What to record for the postmortem, including artifact identities.

Ground every step in files that exist. Target 20–30 minutes.

## Knowledge Check

1. What distinguishes an incident from an alert?
2. Why separate the incident commander from the responders?
3. Why record the timeline during, not after, the incident?
4. What does blameless mean — and not mean?
5. Why is "human error" an insufficient root cause?
6. What are this repository's de facto runbooks?

<details>
<summary>View answers</summary>

1. Impact and coordination: an incident significantly affects service or requires organized response; an alert is just a signal that may or may not indicate one.
2. Coordination (deciding, delegating, communicating) and investigation are both full-time jobs during an incident; one person doing both does both badly.
3. Memory reconstructs and reorders within hours; contemporaneous notes are the only reliable record, including changes made under pressure.
4. It means analyzing systems and conditions rather than punishing reasonable decisions; it does not remove accountability or ownership of corrective actions.
5. It describes *that* something went wrong, not *why it was possible* — the fixable conditions (missing validation, confusing interface, absent check) lie underneath.
6. The TaskOps scripts — deploy, rollback, backup, smoke test — plus KubeOps' health-check script and troubleshooting documentation.

</details>

## Navigation

- [Back to Observability, Metrics, and Optimization](../README.md)
- [Previous: DORA Metrics and Delivery Performance](../04-dora-metrics-and-delivery-performance/)
- [Next: Pipeline Duration, Queues, Caches, and Bottlenecks](../06-pipeline-duration-queues-caches-and-bottlenecks/)
- [Back to All Learning Materials](../../README.md)
