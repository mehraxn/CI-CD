# ConfigMaps, Secrets, Probes, and Resources

ConfigMaps carry non-sensitive configuration; Secrets carry sensitive data but Base64 is encoding, not encryption. RBAC, encryption at rest, narrow mounts, and external managers may be required. Requests influence scheduling/guaranteed capacity; limits cap use and can throttle/terminate workloads.

Liveness asks whether to restart, readiness whether to send traffic, startup whether initialization completed. KubeOps separates `/health` and `/ready`, has requests/limits and a non-root read-only security context. No startup probe exists. Its committed Secret is placeholder-only; production Helm values reference an out-of-band Secret.

## Configuration and Secret Delivery

A ConfigMap stores non-sensitive key/value or file-like configuration. A Secret represents sensitive data, but its common Base64 representation is encoding, not encryption. Protection requires RBAC, encryption at rest in the cluster data store, limited mounts, careful logs, and credential rotation. External secret managers and controllers can deliver values without committing plaintext, but no such integration exists here.

`env` defines individual variables and can use `valueFrom` key references. `envFrom` imports all keys from a ConfigMap or Secret. Volume sources can project keys as files; mounts should be read-only and limited to processes that need them. Both resources are namespace-scoped, so references normally resolve in the Pod's namespace. Updates may not restart applications, and environment variables do not update in a running process; rotation needs an application reload or rollout strategy.

Educational examples—`example-placeholder` is not a real credential:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: task-api-config
data:
  LOG_LEVEL: INFO
---
apiVersion: v1
kind: Secret
metadata:
  name: task-api-secrets
type: Opaque
stringData:
  DATABASE_PASSWORD: example-placeholder
```

Never commit a real value. Secret generators also become unsafe if their inputs are committed plaintext.

## Probes

Readiness asks whether a container should receive Service traffic. Liveness asks whether it should be restarted. Startup gives slow initialization time before liveness/readiness evaluation. HTTP probes call a path, TCP probes test connection establishment, and exec probes run a command. Choose the cheapest check that represents the intended condition.

```yaml
readinessProbe:
  httpGet:
    path: /ready
    port: 8000
  initialDelaySeconds: 5
  periodSeconds: 10
livenessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 15
  periodSeconds: 20
```

`initialDelaySeconds`, `periodSeconds`, `timeoutSeconds`, and `failureThreshold` determine when checks begin and when failure is acted upon. Aggressive liveness can create restart loops during slow startup or dependency failure. Readiness may reasonably fail when the instance cannot serve traffic; liveness should not depend on every external service if that would restart a healthy process endlessly. A startup probe is preferable to a huge liveness delay for predictably slow initialization.

## Resources and Security

Requests guide scheduling and represent capacity Kubernetes plans for. Limits constrain maximum use. CPU over a limit is generally throttled; memory beyond a limit can cause out-of-memory termination. Requests and limits influence Quality of Service classification, but arbitrary copied values are not appropriate. Measure workload behavior and leave headroom.

```yaml
resources:
  requests:
    cpu: 100m
    memory: 128Mi
  limits:
    cpu: 500m
    memory: 512Mi
```

A security context can require a non-root UID, disallow privilege escalation, and set a read-only root filesystem. Applications then need writable temporary or persistent paths explicitly. A PersistentVolumeClaim requests storage with a lifecycle beyond an individual Pod; none exists here.

## KubeOps Audit

The real [ConfigMap](../../../Projects/2_project/kubeops-gitops/k8s/configmap.yaml) contains `APP_ENV` and `LOG_LEVEL`. The [Secret example](../../../Projects/2_project/kubeops-gitops/k8s/secret.example.yaml) is explicitly placeholder material. The [Deployment](../../../Projects/2_project/kubeops-gitops/k8s/deployment.yaml) imports both with `envFrom`, so every key becomes an environment variable. It defines `/health` liveness and `/ready` readiness with initial delays and periods. Timeout and failure threshold use platform defaults; no startup probe is present.

The Deployment requests 100m CPU/128Mi memory and limits 500m/256Mi. It runs UID 1000, disallows privilege escalation, and uses a read-only root filesystem. Helm [defaults](../../../Projects/2_project/kubeops-gitops/helm/kubeops/values.yaml) template equivalent settings. Production values disable rendered Secret creation and reference `kubeops-secret`, indicating out-of-band provisioning, but they do not show how it is created or rotated.

Absent features include PVCs, volume-based ConfigMap/Secret injection, external secret operators, startup probes, network policy, and documented rotation/reload automation. Common mistakes are treating Base64 as encryption, using ConfigMaps for secrets, identical probe semantics, premature liveness, no requests, unrealistic limits, broad secret exposure, and rotation without reload.

## Operational Review

Classify every configuration key by sensitivity, owner, source, rotation frequency, and reload behavior. Non-sensitive log levels fit a ConfigMap; credentials do not. For `envFrom`, check for key collisions and broad exposure. For volumes, check file permissions and which containers mount them. A Secret name in YAML proves a reference, not secure provisioning.

Probe review starts with intent. Readiness should represent ability to serve traffic, liveness should identify a process that cannot recover without restart, and startup should cover initialization. Calculate the effective failure window from delays, periods, timeouts, and thresholds. Ensure probes use named or correct ports and do not overload dependencies. Repeated liveness restarts can hide the original fault.

Resource review compares observed CPU/memory with requests and limits under startup and peak load. Low CPU limits cause latency through throttling; low memory limits cause termination; excessive requests waste scheduling capacity. Quality of Service is a consequence, not a goal by itself. Document how values were measured and revisit them.

Finally combine security context and filesystem behavior. A read-only root is useful only when required writable paths use appropriate temporary or persistent volumes. Non-root UID must match image ownership. Admission and runtime policy may add constraints not visible in workload YAML.

## Change and Rotation Safety

Changing a ConfigMap or Secret does not universally restart Pods. Environment-variable consumers need replacement; projected volumes update eventually, while applications may still need reload. Use an explicit rollout or checksum mechanism when required and test rotation without exposing values. Keep old and new credentials valid long enough for controlled transition when the backing system permits it.

Probe and resource changes are production behavior changes. Tightening liveness or memory limits can create an outage without changing application code. Roll them out gradually and observe restart count, latency, throttling, OOM events, readiness duration, and capacity. Version-control the reasoning as well as the numbers.

A secret audit records names and references, not contents. Verify RBAC and encryption configuration through authorized platform evidence; manifest files cannot prove them. External-manager claims require a real controller/reference, which this repository lacks.

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
