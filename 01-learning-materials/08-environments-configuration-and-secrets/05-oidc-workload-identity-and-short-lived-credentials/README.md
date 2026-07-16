# OIDC, Workload Identity, and Short-Lived Credentials

## The Problem with Stored Cloud Keys

The previous lesson's secrets all share a weakness: a **long-lived credential** sits in a store, waiting. It can leak, it outlives its purpose, and rotating it is manual work that tends not to happen. **Workload identity** attacks the root cause: instead of *storing* a credential, the workload (a CI job, a pod) *proves who it is* and receives **short-lived credentials** on the spot. Humans have **human identities**; services traditionally had **service accounts** with stored keys; workload identity gives them federated, verifiable, keyless identity.

## How the OIDC Flow Works

**OIDC** (OpenID Connect) is the federation mechanism most CI platforms use. The CI platform acts as an **identity provider**, issuing signed **ID tokens** about its own runs; a cloud provider is configured to trust those tokens under conditions:

```text
CI job requests an OIDC identity token
              ↓
Cloud provider validates issuer and claims
              ↓
Trust policy allows or denies the request
              ↓
Cloud provider issues short-lived credentials
              ↓
Job performs authorized operation
              ↓
Credentials expire automatically
```

The token carries **claims**: the **issuer** (which CI platform), the **subject** (which repository/workflow/branch/environment), and the **audience** (who the token is intended for). The cloud side defines a **trust policy** — which claims, with which values, may perform **role assumption** into which **cloud role** — and issues **session credentials** with a bounded **token lifetime**.

Read carefully what this does and does not mean:

- **OIDC does not mean "no authentication"** — the signed token *is* authentication, verified cryptographically.
- **A trust policy is still required** — and it is now the security boundary; **incorrect trust conditions can grant excessive access** (trusting a whole organization, or any branch, means any workflow there can assume the role).
- The CI platform token is **exchanged** for temporary cloud credentials — the cloud never sees a stored secret.
- **Short-lived credentials reduce but do not eliminate risk** — during their lifetime they are as powerful as their role; **token replay** within the window and over-broad roles remain threats.
- **Permissions still require least privilege** — OIDC changes how you authenticate, not what the role may do.

The wins: near-zero **credential rotation** burden, nothing to leak from a secret store, and strong **auditability** (every role assumption logs which repo/branch/run asked).

## In GitHub Actions Terms

The workflow must be allowed to request an ID token:

```yaml
permissions:
  contents: read
  id-token: write
```

`id-token: write` allows *requesting an OIDC token*; it grants no cloud permissions by itself — those come from the cloud role that the trust policy maps the token to.

A cloud-login step, shown as **pseudocode** (each provider ships its own real action; do not copy this as executable):

```yaml
- name: Configure cloud credentials
  uses: cloud-provider/configure-credentials@version
  with:
    role-to-assume: example-role
```

## Restricting the Trust Policy

The trust policy should pin every claim it can:

```text
Repository
Branch or tag
Workflow
Environment
Audience
Organization
```

A production-deployment role should typically require: this exact repository, the default branch (or a protected environment claim), the expected audience — and nothing broader. Pull-request-triggered runs deserve special suspicion: **untrusted PRs must not be able to request privileged credentials**, which is achieved by never granting `id-token: write` to PR-triggered workflows that run untrusted code, and by trust conditions that exclude PR contexts.

## Common Mistakes

- Trusting every repository in an organization.
- Trusting every branch.
- Granting administrator cloud permissions to the assumed role.
- Allowing untrusted pull requests to request privileged credentials.
- Not validating the audience.
- Assuming token expiration prevents all misuse.
- Keeping the old long-lived credentials around after OIDC is introduced.
- No audit or alerting on role assumption.

## Existing Repository Evidence

The repository does **not** use OIDC: no workflow declares `id-token: write`, and no cloud-credential actions exist. All examples above are conceptual. What the repository does have is the contrast case: [TaskOps CD](../../../Projects/1_project/taskops-cicd/.github/workflows/cd.yml) authenticates to its deployment server with a **stored long-lived SSH key** (`secrets.DEPLOY_SSH_KEY`) — a perfectly common pattern, and exactly the kind of stored credential workload identity replaces where the target supports it. (For GHCR, the ephemeral `GITHUB_TOKEN` already behaves like a short-lived, automatically scoped credential — the platform-native version of the same idea.) OIDC-based cloud deployment may be introduced in a later project-enhancement phase.

## Practical Exercise

Design a trust policy on paper for a hypothetical cloud-deploying version of TaskOps CD:

1. List the claims you would require and their exact values (repository, ref, audience; would you use an environment claim?).
2. Define the cloud role's permissions for "push an image and update one service" — least privilege, name the operations.
3. State which workflow triggers may request the token, and why `pull_request` is excluded.
4. Write the decommissioning step for the now-redundant stored credential.
5. Name two log events you would alert on.

Do not modify any workflow or settings. Target 20–30 minutes.

## Knowledge Check

1. What problem does workload identity solve that a secret manager does not?
2. What does `id-token: write` grant, exactly?
3. Where does the security boundary move to under OIDC?
4. Why must the audience claim be validated?
5. Do short-lived credentials eliminate the need for least privilege?
6. What stored long-lived credential does this repository currently rely on?

<details>
<summary>View answers</summary>

1. The existence of stored long-lived credentials at all — the workload proves identity per run and receives expiring credentials, so there is nothing durable to leak or rotate.
2. Only the ability to request an OIDC ID token from the platform; cloud permissions come entirely from the role the trust policy maps that token to.
3. To the trust policy — its claim conditions decide who may assume the role, so loose conditions are the new leaked key.
4. It binds the token to its intended consumer; without it, a token minted for one integration could be replayed against another.
5. No — during their lifetime they carry the role's full power; the role must still be minimal.
6. The SSH deploy key stored as `DEPLOY_SSH_KEY` in TaskOps CD.

</details>

## Navigation

- [Back to Environments, Configuration, and Secrets](../README.md)
- [Previous: Secrets Management and Injection](../04-secrets-management-and-injection/)
- [Next: Protected Environments, Approvals, and Release Controls](../06-protected-environments-approvals-and-release-controls/)
- [Back to All Learning Materials](../../README.md)
