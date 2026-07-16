# Release Readiness and Post-Release Verification

## Release Readiness Checklist

- [ ] Exact artifact identity recorded
- [ ] Required tests passed
- [ ] Security checks reviewed
- [ ] Configuration validated
- [ ] Secrets and permissions available
- [ ] Database change is compatible
- [ ] Monitoring and alerts are ready
- [ ] Rollback or roll-forward plan exists
- [ ] Responsible owner is identified

Deployment readiness covers pre-deployment mechanics: artifact verification, target configuration, secret availability, database compatibility, capacity, and dependencies. Release readiness adds change-risk review, runbook, monitoring and alert readiness, business expectations, and ownership.

```text
Deploy
  ↓
Readiness and health checks
  ↓
Smoke tests
  ↓
Metrics, logs, and traces
  ↓
Business validation
  ↓
Accept, roll forward, or roll back
```

A successful command proves only that the command returned success. During a defined verification window, combine shallow health, synthetic checks, error rate, latency, logs, metrics, traces, and business KPIs. Add a deployment marker so changes correlate with telemetry. Then record release acceptance, failure, rollback, roll-forward, or incident declaration.

Artifact verification confirms the expected digest/checksum and source lineage before deployment. Configuration validation checks required keys, types, and target scope without exposing values. Secret availability checks access, not secret contents. Capacity and dependency checks ensure the environment can support the transition, including surge or duplicated capacity.

Database compatibility must cover old and new versions during overlap and recovery. Rollback readiness means the previous artifact is retained, configuration is recoverable, and state remains compatible. A runbook should name commands conceptually, owners, evidence, stop conditions, and communications; its usefulness should be tested in a drill.

Monitoring readiness means dashboards answer release questions and alerts are enabled with useful thresholds. Synthetic checks exercise a user path, while business KPIs reveal harm that infrastructure metrics miss. Verification windows should reflect traffic volume and delayed effects. “No alerts in five minutes” is not acceptance when the service receives one request per hour.

## Existing Repository Evidence

- [TaskOps CD](../../../Projects/1_project/taskops-cicd/.github/workflows/cd.yml) verifies tests and security, deploys, then runs [smoke_test.sh](../../../Projects/1_project/taskops-cicd/scripts/smoke_test.sh) against production `/health`.
- [TaskOps health](../../../Projects/1_project/taskops-cicd/app/routes.py) checks application and database availability; Compose also uses it.
- [KubeOps deployment](../../../Projects/2_project/kubeops-gitops/k8s/deployment.yaml) separates liveness `/health` and readiness `/ready`; [check-health.ps1](../../../Projects/2_project/kubeops-gitops/scripts/check-health.ps1) performs a manual smoke check.
- [Project 3 monitoring](../../../Projects/3_project/monitoring/prometheus.yml) and [dashboard](../../../Projects/3_project/monitoring/grafana-dashboard.json) provide monitoring examples, but no release marker or automated acceptance exists.

## Common Mistakes

- Verifying nothing after deployment or only process existence.
- Omitting business validation and rollback identity.
- Disabling alerts during deployment.
- Having no deployment marker or verification owner.
- Declaring success immediately or monitoring only infrastructure.

## Practical Exercise

Map every `/health`, `/ready`, Docker health check, Kubernetes probe, smoke script, and monitoring file to pre-deployment, readiness, smoke, technical observation, or business validation. Identify missing traces, business KPI, marker, verification window, and owner.

## Knowledge Check

1. Why is command success insufficient?
2. How does release readiness exceed deployment readiness?
3. What is a deployment marker for?
4. When should an incident be declared?
5. What post-deploy evidence does TaskOps have?

<details><summary>View answers</summary>

1. Users, dependencies, configuration, and business behavior may still fail.
2. It adds operational evidence, business risk, communication, and recovery ownership.
3. To correlate telemetry changes with the deployment.
4. When impact or recovery criteria cross the agreed threshold.
5. A retrying smoke test against the deployed `/health` endpoint.

</details>

## Navigation

- [Back to Continuous Delivery and Releases](../README.md)
- [Previous: Approvals, Release Windows, and Change Controls](../05-approvals-release-windows-and-change-controls/)
- [Next: Release Automation, Communication, and Audit](../07-release-automation-communication-and-audit/)
- [Back to All Learning Materials](../../README.md)
