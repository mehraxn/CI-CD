# Deploying Container Images

Deployment should pull an already verified image, inject environment configuration/secrets, start it with resource/storage/network policy, check readiness and health, and record exact identity. Rebuilding on the target breaks chain of custody.

TaskOps CD deploys the commit-SHA tag over SSH; its script optionally logs in with password-stdin, writes protected environment configuration, pulls through Compose, starts nginx/app, smoke-tests, and records the previous tag. KubeOps manifests/Helm reference an image repository/tag; production values use `latest`, not a digest. Private Kubernetes pulls would require an imagePullSecret or workload integration, but none is configured.

Container writable layers are ephemeral; TaskOps uses a named volume for SQLite. Rollback must retain the old image and compatible state. Deployment by digest is strongest but absent.

## From Registry to Runtime

A deployment consumes an image; it should not recreate one. The target authenticates for pull when necessary, resolves an approved reference, downloads missing layers, injects environment-specific configuration, attaches storage and networks, starts the process, waits for health/readiness, and performs verification. Recording the digest, source revision, deployment time, target, and result creates an audit path.

```text
Verified registry image
    | approved tag or digest
Deployment target pulls
    | injects configuration and secrets
Starts workload
    | health and smoke verification
Records exact identity and outcome
```

Mutable tags are convenient but can resolve differently across restarts. A commit-SHA tag improves traceability if it cannot be overwritten; a digest pins exact content. Pull policy also matters: cached local content and a mutable tag can surprise operators. A verified identity should be promoted across environments without rebuilding per environment.

Configuration belongs outside the image so one artifact can move from test to production. Secret values need a protected delivery mechanism and must not appear in logs or documentation. The runtime user, filesystem permissions, capabilities, resource policy, ports, and network exposure should match the workload. Private registries require a pull identity such as host login, Kubernetes `imagePullSecrets`, or platform workload integration. Least privilege and rotation still apply.

Container writable layers are not durable storage. Named volumes, Kubernetes persistent volumes, or external services preserve state, but each needs backup and compatibility planning. Rollback of image configuration does not roll back databases. A previous image may also be incompatible with a forward-only migration, so roll-forward, restore, and migration policy must be coordinated.

## Deployment Target Comparison

| Target | Strength | Main operational concern |
|--------|----------|--------------------------|
| Single host with Compose | Simple and inspectable | Host availability and manual capacity |
| Kubernetes Deployment | Reconciliation and replica rollout | Cluster policy and manifest correctness |
| Managed container service | Reduced control-plane work | Provider configuration and identity |

These are delivery models, not quality levels. Each should pull the accepted image, monitor startup, route traffic only when appropriate, and preserve evidence. Rebuilding on any target breaks the verified chain.

## Repository Evidence

TaskOps [CD](../../../Projects/1_project/taskops-cicd/.github/workflows/cd.yml) builds and scans the SHA-tagged image, pushes it to GHCR, copies Compose and scripts over SSH, and passes `IMAGE_TAG=${{ github.sha }}` to the server. The [deployment script](../../../Projects/1_project/taskops-cicd/scripts/deploy.sh) writes a protected `.env`, optionally logs in to GHCR with password-stdin, pulls the Compose image, brings up the stack, verifies health, and records the tag. [Production Compose](../../../Projects/1_project/taskops-cicd/docker-compose.prod.yml) pulls the supplied repository/tag, injects configuration, persists `/data`, checks app health, and routes through nginx. The workflow then runs an external smoke test.

TaskOps [rollback](../../../Projects/1_project/taskops-cicd/scripts/rollback.sh) selects the recorded previous tag and recreates the stack, while [backup](../../../Projects/1_project/taskops-cicd/scripts/backup.sh) handles SQLite data separately. This demonstrates why image rollback and data recovery are distinct. File evidence cannot prove the remote host exists or a deployment succeeded.

KubeOps raw [Deployment](../../../Projects/2_project/kubeops-gitops/k8s/deployment.yaml) uses `kubeops:local`, while [production Helm values](../../../Projects/2_project/kubeops-gitops/helm/kubeops/values-prod.yaml) use a GHCR repository with mutable `latest`. Neither pins a digest. No `imagePullSecrets` appears in raw or templated resources, so private-image authentication is not demonstrated. Argo CD points at the dev values file and manual sync; it does not create a direct CI push deployment.

Project 3 Compose builds locally rather than consuming a published application image, and no executable workflow publishes it. That is a learning gap, not evidence of registry delivery.

Common failures include target-side rebuilding, deploying an unverified tag, missing pull credentials, baked configuration, writable-layer data, no readiness gate, no post-deploy test, and rollback without state compatibility. Deployment success means both infrastructure transition and meaningful application verification, not merely a running process.

## Deployment Evidence and Failure Handling

A deployment record should include target, approved tag and digest, configuration revision, secret references by name, storage changes, start time, readiness result, smoke-test result, and rollback identity. Logs must not contain credential values. A restart using the same record should resolve the same content; otherwise the release is not reproducible.

On failure, distinguish image pull/authentication, process startup, readiness, routing, application behavior, and data compatibility. Rolling back the image addresses only some categories. Preserve diagnostic logs before replacement and avoid rebuilding on the target. If a mutable tag moved, determine the resolved digest rather than assuming the label still identifies the failed bytes.

## Practical Exercise

Trace TaskOps image from source through GHCR to Compose and rollback. Record identity, credentials by name only, configuration, volume, health, and gaps.

## Knowledge Check

1. Build on target? 2. Why external config? 3. Where is TaskOps state? 4. Does KubeOps prod pin digest?

<details><summary>Answers</summary>

1. No. 2. Same image across environments. 3. Named volume. 4. No.

</details>

## Navigation
- [Back to Docker in CI/CD](../README.md)
- [Previous: Publishing Images and Registry Workflows](../07-publishing-images-and-registry-workflows/)
- [Back to All Learning Materials](../../README.md)
