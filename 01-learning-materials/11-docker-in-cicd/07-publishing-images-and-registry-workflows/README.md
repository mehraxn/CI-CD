# Publishing Images and Registry Workflows

Publication authenticates to a registry with least privilege, builds verified content, assigns traceable tags, pushes manifest/layers, records digest, and retains evidence. Pull needs read access; push needs write; ordinary publishing should not need delete/admin.

TaskOps CD and KubeOps image-release use `docker/login-action@v3`, Buildx, `GITHUB_TOKEN`, and `packages: write` to GHCR. Both lowercase the owner and push SHA plus `latest`. No QEMU, multi-architecture index, digest capture, signing, SBOM, or provenance exists. TaskOps scans before push; KubeOps after.

Private images still need scanning and controlled deployment credentials. Never print tokens or put them in command arguments. Protect release tags and publish only from trusted triggers.

## Practical Exercise

Annotate one workflow: trigger, permissions, login, image name, tags, scan point, cache, digest gap, and consumer.

## Knowledge Check

1. Minimum publisher right? 2. Why record digest? 3. Private means safe? 4. Is multi-arch present?

<details><summary>Answers</summary>

1. Scoped write. 2. Exact content identity. 3. No. 4. No.

</details>

## Navigation
- [Back to Docker in CI/CD](../README.md)
- [Previous: Container Testing, Health Checks, and Scanning](../06-container-testing-health-checks-and-scanning/)
- [Next: Deploying Container Images](../08-deploying-container-images/)
- [Back to All Learning Materials](../../README.md)
