# DAST, API Security, and Runtime Validation

## Testing from the Outside

Everything so far analyzed artifacts at rest. **Dynamic Application Security Testing (DAST)** attacks the *running* application the way an attacker would — over the network, with no knowledge of the source:

```text
SAST:
Analyzes code without running the application.

DAST:
Tests a running application from the outside.

API security test:
Validates interface security behavior, authentication, authorization, and input handling.

Runtime monitoring:
Observes real behavior after deployment.
```

DAST finds what static tools structurally cannot: real **security headers** and **TLS** behavior, actual **authentication and session management**, deployed-configuration mistakes, and injectable endpoints as they actually respond. It cannot see unexecuted code paths, and it cannot judge whether *this user seeing that record* is a business-rule violation — **broken access control**, the top of the **OWASP Top 10**, needs targeted tests, not just a scanner.

## How a DAST Run Works

A scanner (OWASP ZAP is the common open-source reference) performs **endpoint discovery** (crawling, or better, an API schema), then **passive scanning** (inspect responses without attacking — headers, cookies, information leaks) and **active scanning** (send attack payloads — injection, **XSS**, **SSRF** probes). A **baseline scan** is the light, CI-friendly passive mode. **Authenticated scans** matter enormously: an unauthenticated scan sees the login page; the application lives behind it. For APIs specifically, add **schema validation** (does the API reject what the contract forbids?), **rate-limit** behavior, and the **OWASP API Security Top 10** concerns — object-level authorization above all, tested for *forbidden* requests, not just successful ones.

```text
Deploy test environment
        ↓
Wait for readiness
        ↓
Run authenticated and unauthenticated security checks
        ↓
Collect findings
        ↓
Destroy temporary environment
```

## Safety Rules

DAST is controlled attacking, so the controls are not optional:

- Scanners send unusual and potentially harmful requests — run them **only against authorized targets** with explicit **scope control** (never third-party systems that happen to be linked).
- **Destructive scans must not reach production** — a form-submitting crawler against a live database is an incident, not a test.
- Test accounts and generated **test data** need cleanup; scanner **credentials** are secrets like any other.
- Respect **rate limits** and environment capacity.
- Findings are leads, not verdicts — **false positives** are common, and DAST does not prove access-control correctness for every business case.

## Common Mistakes

- Scanning production without authorization.
- Scanner scope including third-party systems.
- No authenticated testing — scanning only the outside of the front door.
- Default scanner credentials committed to the repository.
- Findings treated as automatically exploitable.
- DAST used *instead of* unit and integration security tests.
- No evidence retained.
- Temporary environment not destroyed.
- API authorization tested only for successful requests.
- No ownership for findings.

## Existing Repository Evidence

**No DAST exists in this repository** — no ZAP, no API security scanner, no scheduled dynamic testing; everything above is conceptual. The nearest real relatives are worth placing precisely on the spectrum:

- The **runtime smoke checks** are real but are *availability* validation, not security testing: [TaskOps CI](../../../Projects/1_project/taskops-cicd/.github/workflows/ci.yml) polls the container's `/health`; [TaskOps CD](../../../Projects/1_project/taskops-cicd/.github/workflows/cd.yml) runs `scripts/smoke_test.sh` post-deploy. Both are production-safe (read-only GET) — a property a DAST plan must deliberately engineer.
- Real **API security tests at the unit/integration level** exist: [TaskOps `test_security.py`](../../../Projects/1_project/taskops-cicd/tests/test_security.py) verifies CSRF rejection, and KubeOps' `test_validation.py` exercises input validation — the in-process complement DAST would confirm from outside.
- The ephemeral container in TaskOps CI (start → verify → always-destroy) is structurally the disposable target environment a baseline DAST scan would want.

DAST may be added in a later project-enhancement phase; do not add workflow files or execute scans now.

## Practical Exercise

Design a safe DAST plan for TaskOps:

```text
Authorized target
Environment
Authentication
Excluded paths
Test data
Maximum duration
Finding severity
Cleanup
Owner
```

Anchor it in reality: the target should be the CI-built container (as TaskOps CI already runs it), state whether your first iteration is passive/baseline or active and why, define which finding severity blocks versus reports, and specify the cleanup step's condition (`if: always()` — and why). Explicitly name the one environment this plan must never point at. Do not implement or run anything. Target 20–30 minutes.

## Knowledge Check

1. What can DAST find that SAST cannot, and vice versa?
2. Why are authenticated scans essential?
3. Why must active scanning never accidentally target production?
4. Why does broken access control resist generic scanning?
5. Are this repository's smoke tests DAST? Why or why not?
6. What is a baseline scan?

<details>
<summary>View answers</summary>

1. DAST sees deployed reality — headers, TLS, auth flows, actual responses to attacks; SAST sees all code paths including unexecuted ones. Each is blind where the other sees.
2. Most of the application's attack surface lies behind login; unauthenticated scans test only the public edge.
3. Active scans submit attack payloads and forms — against production they corrupt data, trigger side effects, and constitute a self-inflicted incident.
4. Whether a specific user may access a specific object is a business rule the scanner cannot know; it must be tested with explicit forbidden-request cases.
5. No — they are read-only availability checks (does `/health` return ok), sending no attack traffic and evaluating no security behavior.
6. A light, typically passive scan (inspecting responses without attack payloads) suitable for fast CI feedback.

</details>

## Navigation

- [Back to DevSecOps and Supply-Chain Security](../README.md)
- [Previous: Secure Pipelines, Permissions, Actions, and Runners](../06-secure-pipelines-permissions-actions-and-runners/)
- [Next: Vulnerability Management, Exceptions, and Response](../08-vulnerability-management-exceptions-and-response/)
- [Back to All Learning Materials](../../README.md)
