# ConfigMaps, Secrets, Probes, and Resources

ConfigMaps carry non-sensitive configuration; Secrets carry sensitive data but Base64 is encoding, not encryption. RBAC, encryption at rest, narrow mounts, and external managers may be required. Requests influence scheduling/guaranteed capacity; limits cap use and can throttle/terminate workloads.

Liveness asks whether to restart, readiness whether to send traffic, startup whether initialization completed. KubeOps separates `/health` and `/ready`, has requests/limits and a non-root read-only security context. No startup probe exists. Its committed Secret is placeholder-only; production Helm values reference an out-of-band Secret.

## Practical Exercise
Audit keys, sensitivity, injection, probes, resources, and security context without reading values.
## Knowledge Check
1. ConfigMap for password? 2. Base64 encryption? 3. Request versus limit? 4. Readiness effect?
<details><summary>Answers</summary>
1. No. 2. No. 3. Scheduling baseline versus cap. 4. Removes Pod from traffic.
</details>
## Navigation
- [Back to Kubernetes and GitOps](../README.md)
- [Previous: Manifests, Deployments, Services, and Namespaces](../02-manifests-deployments-services-and-namespaces/)
- [Next: Helm Charts, Values, and Releases](../04-helm-charts-values-and-releases/)
- [Back to All Learning Materials](../../README.md)
