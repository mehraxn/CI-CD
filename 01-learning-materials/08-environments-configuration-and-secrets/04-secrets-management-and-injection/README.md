# Secrets Management and Injection

## What Counts as a Secret

A **secret** is any value whose disclosure could cause harm: **passwords**, **API keys**, **access and refresh tokens**, **private keys and certificates**, **database credentials**, **registry credentials**, **cloud credentials**. The defining property is consequence, not format — and the defining rule is that secrets get *stronger* handling than configuration: encrypted storage, scoped access, injection only where needed, rotation, and audit.

## Where Secrets Live

A **secret manager** stores secrets encrypted (**at rest** and **in transit**), controls access, logs it (**audit log**), and supports **rotation**, **revocation**, and **expiration**. Conceptually in this family: HashiCorp Vault, AWS Secrets Manager, Azure Key Vault, Google Secret Manager — plus platform-native stores: **GitHub Actions secrets** (repository, organization, and environment scoped), **Kubernetes Secrets** (with external-secret integrations syncing from managers), **Docker secrets**, **Ansible Vault** (encrypted variable files), and Terraform's **sensitive values** marking. The lifecycle every store should support:

```text
Secret manager
      ↓
Authorized workload retrieves or receives secret
      ↓
Secret is injected only where required
      ↓
Application uses secret
      ↓
Secret is rotated or revoked
```

These mechanisms do not offer identical guarantees. A Kubernetes Secret is an API object whose Base64 representation is not encryption; cluster encryption at rest and access controls must be configured separately. Docker secrets are mounted for services rather than baked into image layers. Ansible Vault encrypts committed variable content but still requires careful vault-password delivery. Terraform's `sensitive` marking hides values from normal display, yet secret values can still enter state, so the state backend itself needs encryption and strict access. A dedicated manager can centralize lifecycle controls, but workloads still need narrowly scoped authorization to retrieve values.

**Least privilege and scope** apply twice: which identities may *read* a secret, and which jobs/steps/services it is *injected into*. Add **break-glass access** (documented emergency retrieval, logged), **secret scanning** (tools that detect committed secrets), and an **incident-response** rule everyone must know: **removing a secret from Git does not revoke it** — history retains it and clones already have it; a committed secret is a *rotated* secret, immediately.

Rotation replaces a credential without avoidable downtime: issue the replacement, update consumers, verify them, then revoke the old value. Immediate revocation comes first when compromise is suspected. Certificates, refresh tokens, and database credentials may require different overlap procedures, but every secret needs an owner, expiration expectation, and tested incident path.

## Injection Mechanisms

Secrets reach workloads by **environment-variable injection**, **file-based injection / mounted volumes** (Kubernetes Secrets as files; often preferable since files don't leak into `ps` output or child processes as easily), or **runtime retrieval** (the application asks the manager directly).

A conceptual GitHub Actions injection:

```yaml
jobs:
  publish:
    runs-on: ubuntu-latest

    steps:
      - name: Publish
        env:
          REGISTRY_TOKEN: ${{ secrets.REGISTRY_TOKEN }}
        run: |
          echo "Authenticate without printing the token"
```

Note what it deliberately does *not* do: display the token, or pass it as a command-line argument (arguments appear in process lists and logs; environment variables scoped to one step are the safer carrier).

A Kubernetes Secret shape:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: task-api-secrets
type: Opaque
stringData:
  DATABASE_PASSWORD: example-placeholder
```

The placeholder must never be replaced with a real value in committed documentation or manifests — committed manifests are Git content, and Git is not a secret store.

## Why Masking Is Not Enough

- **Masking is redaction, not encryption** — the platform hides *known exact values* from logs; the secret itself is present in the job.
- **Masking may fail for transformed values** — base64-encoded, split, concatenated, or case-changed secrets are not recognized.
- **Base64 is not encryption** — Kubernetes Secrets' encoding is transport formatting, not protection.
- Secrets leak through **command arguments**, **caches and artifacts** (never cache or upload secret-bearing paths), and **debug output** (`env | sort` in a debug step prints everything).
- **Forked pull requests** run untrusted code; platforms restrict their secret access by default — do not weaken that.
- **A private repository does not make committed secrets safe** — every clone, every past contributor, every future leak of the repo carries them.

## Common Mistakes

- Secrets in Git (any visibility).
- Secrets baked into Docker images or passed as build arguments (both persist in layers/metadata).
- Secrets printed in logs.
- Secrets stored as ordinary variables.
- One credential shared by many services — no blast-radius control, impossible rotation.
- No expiration or rotation.
- CI credentials with administrator permissions.
- Secret-bearing artifacts.
- Long-lived personal tokens doing service work.
- Failing to revoke leaked credentials because "we deleted the file."

## Existing Repository Evidence

- **GitHub Actions secrets, properly injected**: [TaskOps CD](../../../Projects/1_project/taskops-cicd/.github/workflows/cd.yml) references `secrets.DEPLOY_HOST`, `DEPLOY_USER`, `DEPLOY_SSH_KEY`, `DEPLOY_PORT`, `FLASK_SECRET_KEY`, and `secrets.GITHUB_TOKEN` — always as action inputs or step `env`, never echoed or passed on command lines. Values are, correctly, invisible in source.
- **The copy-and-gitignore pattern**: KubeOps' [secret.example.yaml](../../../Projects/2_project/kubeops-gitops/k8s/secret.example.yaml) is a placeholder-only example whose header instructs copying to a gitignored `secret.yaml` — committed shape, uncommitted value.
- **Out-of-band production secrets**: [values-prod.yaml](../../../Projects/2_project/kubeops-gitops/helm/kubeops/values-prod.yaml) sets `secret.create: false` with `existingSecret: kubeops-secret` — production expects the Secret provisioned outside the chart, so no real value ever transits Git or Helm rendering.
- **Required-secret validation**: [docker-compose.prod.yml](../../../Projects/1_project/taskops-cicd/docker-compose.prod.yml) aborts if `FLASK_SECRET_KEY` is unset; the [.env.example](../../../Projects/1_project/taskops-cicd/.env.example) documents how to generate one and warns never to commit the real `.env`.
- **Runtime key delivery for Ansible**: [inventory.example.ini](../../../Projects/3_project/ansible/inventory.example.ini) comments out the SSH key path — "supply a real key at runtime instead of committing it here."
- Not demonstrated: dedicated secret managers, Ansible Vault, environment-scoped GitHub secrets, secret rotation automation, and secret scanning — conceptual here, candidates for a later enhancement phase.

## Practical Exercise

Build a secret-reference inventory for the repository — names and flow only, never values. For each secret reference you can find (the six in TaskOps CD, `APP_SECRET_KEY` in KubeOps' three carriers, the Ansible SSH key), record:

```text
Secret name
Store (GitHub secrets / gitignored file / out-of-band Secret / runtime)
Scope (workflow, job, step, cluster namespace)
Injection mechanism (action input, step env, envFrom secretRef, .env file)
Consumer
Rotation story (documented, possible, or absent)
```

Conclude with the two secrets whose leak would hurt most, and what the current revocation path for each would be. Target 25–35 minutes.

## Knowledge Check

1. What distinguishes a secret from configuration?
2. Why is masking insufficient protection?
3. Is base64 encoding protection? Why or why not?
4. Why does removing a committed secret from Git not end the incident?
5. Why should secrets not travel as command-line arguments?
6. How does KubeOps keep production secret values out of Git entirely?

<details>
<summary>View answers</summary>

1. Consequence of disclosure — secrets can cause harm if revealed, so they need encrypted storage, scoped access, rotation, and audit that configuration does not.
2. It redacts known exact values from logs only; transformed values escape it, and the secret is still present in the job to leak by other routes.
3. No — it is reversible encoding for transport, not encryption; anyone with the value decodes it.
4. History and clones retain the value; the credential must be rotated/revoked immediately — deletion changes nothing about exposure.
5. Arguments are visible in process lists and can be captured in logs; step-scoped environment variables or files are safer carriers.
6. The chart references an `existingSecret` provisioned out-of-band in production, and the committed example file carries only a placeholder with copy-and-gitignore instructions.

</details>

## Navigation

- [Back to Environments, Configuration, and Secrets](../README.md)
- [Previous: Externalized Configuration and Variables](../03-externalized-configuration-and-variables/)
- [Next: OIDC, Workload Identity, and Short-Lived Credentials](../05-oidc-workload-identity-and-short-lived-credentials/)
- [Back to All Learning Materials](../../README.md)
