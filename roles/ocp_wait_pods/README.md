# Role: ado.openshift.wait_for_pods_running

Wait until matching Pods are **Running** and **Ready** in an OpenShift namespace.

- Read-only: polls the API, does not mutate pod specs
- Works with kubeconfig **or** host+token authentication
- Designed for CI: clear success/fail outcomes with timeout

---

## Requirements

- OpenShift/Kubernetes API access (via kubeconfig or env vars)
- `kubernetes.core` collection installed

---

## Role Variables

| Variable | Description |
|---------|-------------|
| `name_space` | Namespace to watch. **Required.** |
| `validate_certs` | TLS verification for API calls (`true` with a trusted CA; set `false` for lab/self-signed). |

### Auth via environment (optional)

| Variable | Description |
|---------|-------------|
| `KUBECONFIG` | Path to kubeconfig (alternative to host+token). |
| `K8S_AUTH_HOST` | API server URL, e.g. `https://api.cluster:6443`. |
| `K8S_AUTH_API_KEY` | Bearer token for the API. |
| `K8S_AUTH_VERIFY_SSL` | `true`/`false` TLS verify toggle. |
| `K8S_AUTH_SSL_CA_CERT` | Path to CA bundle file when verifying TLS. |

---

## Examples

### Wait for two pods with label `app=hello` to be Ready
```yaml
- hosts: localhost
  gather_facts: false
  roles:
    - role: ado.openshift.wait_for_pods_running
      vars:
        name_space: my-app
        validate_certs: true

```

---

## Behavior Notes

- Uses `kubernetes.core.k8s_info` to poll matching Pods until criteria are met.
- Success when:
  - The **count** of matched pods equals `expected_pods` (if set), **and**
  - Every container in each pod reports `Ready=true`.
- If `expected_pods` is **not** set, the role requires a **non-empty** matched set, and all containers Ready.
- Fails on timeout or when no pods match.
- Emits **no changes** (idempotent "wait").

---

## Molecule Testing

A default Molecule scenario is provided that:
```
dependency → lint → syntax → create → converge → idempotence → verify → destroy
```
- Creates a fixture Deployment (`app=hello`, 2 replicas) in a test namespace.
- Runs this role to wait for the pods to become Ready.
- Verifies with `k8s_info`, then cleans up the namespace.

> If your cluster uses a self-signed cert, provide a CA file and keep `validate_certs: true`, or temporarily set `K8S_AUTH_VERIFY_SSL=false` for tests.

---

## Author
- Chad Elliott (<chelliot@redhat.com>)

---

## Repository layout (role)

```text
roles/
└─ wait_for_pods_running/
   ├─ README.md                 # ← this file
   ├─ defaults/
   │  └─ main.yml
   ├─ tasks/
   │  ├─ main.yml
   │  └─ wait_for_pods.yml
   ├─ molecule/
   │  └─ default/
   │     ├─ converge.yml
   │     ├─ destroy.yml
   │     ├─ molecule.yml
   │     ├─ verify.yml
   │     ├─ README.md
   │     └─ TEST.md
   ├─ vars/
   │  └─ main.yml               # (optional)
   ├─ handlers/
   │  └─ main.yml               # (optional)
   └─ tests/
      ├─ inventory
      └─ test.yml
```
