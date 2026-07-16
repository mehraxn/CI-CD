# Deploying Container Images

Deployment should pull an already verified image, inject environment configuration/secrets, start it with resource/storage/network policy, check readiness and health, and record exact identity. Rebuilding on the target breaks chain of custody.

TaskOps CD deploys the commit-SHA tag over SSH; its script optionally logs in with password-stdin, writes protected environment configuration, pulls through Compose, starts nginx/app, smoke-tests, and records the previous tag. KubeOps manifests/Helm reference an image repository/tag; production values use `latest`, not a digest. Private Kubernetes pulls would require an imagePullSecret or workload integration, but none is configured.

Container writable layers are ephemeral; TaskOps uses a named volume for SQLite. Rollback must retain the old image and compatible state. Deployment by digest is strongest but absent.

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
