# Role: ado.openshift.operatorgroup

Create, reconcile, or remove an **OperatorGroup** in OpenShift.

- Supports **Single Namespace** mode (default) and **All Namespaces** mode.
- Idempotent: safely skips/updates when objects already match the desired state.
- Delete path is **namespace-aware** (won’t fail if the namespace is already gone).


---

## Requirements

- OpenShift/Kubernetes API access (env or kubeconfig).
- `kubernetes.core` collection.

---

## Variables

| Variable | Description |
|---------|-------------|
| `name_space` | Target application namespace (required for single-namespace mode). |
| `all_namespaces_install` | `false` = Single Namespace (default); `true` = All Namespaces (installs in `openshift-operators`). |
| `operatorgroup` / `operatorgroup_name` | OperatorGroup name. Defaults to `global-operators` (all-ns) or `<name_space>-operatorgroup` (single-ns). |
| `state` | `present` (default) or `absent`. |
| `validate_certs` | TLS verification for API calls (`true` with a trusted CA; set `false` for lab/self-signed). |

### Auth via environment (optional)

| Variable | Description |
|---------|-------------|
| `KUBECONFIG` | Path to kubeconfig file (alternative to host+token). |
| `K8S_AUTH_HOST` | API server URL, e.g. `https://api.cluster:6443`. |
| `K8S_AUTH_API_KEY` | Bearer token for the API. |
| `K8S_AUTH_VERIFY_SSL` | `true`/`false` TLS verify toggle. |
| `K8S_AUTH_SSL_CA_CERT` | Path to CA bundle file when verifying TLS. |

---

## Examples

### Single-namespace OperatorGroup (most common)
```yaml
- hosts: localhost
  gather_facts: false
  roles:
    - role: ado.openshift.operatorgroup
      vars:
        name_space: my-app
        operatorgroup: my-app-operatorgroup
        validate_certs: true
```

### Remove the OperatorGroup (namespace may or may not still exist)
```yaml
- hosts: localhost
  gather_facts: false
  roles:
    - role: ado.openshift.operatorgroup
      vars:
        state: absent
        name_space: my-app
        validate_certs: true
```

### All-namespaces mode (shared OG in `openshift-operators`)
```yaml
- hosts: localhost
  gather_facts: false
  roles:
    - role: ado.openshift.operatorgroup
      vars:
        all_namespaces_install: true
        validate_certs: false
```

---

## Behavior Notes

- **Single Namespace** mode sets:
  ```yaml
  spec:
    targetNamespaces:
      - {{ name_space }}
  ```
- **All Namespaces** mode omits `targetNamespaces` (or leaves it empty).
- Delete path:
  - Checks if operator namespace exists; if missing, treats OG as absent.
  - Deletes only when OG is present; otherwise logs “already absent”.

---

## Molecule

A default Molecule scenario is included for this role and focuses on **single-namespace** behavior. It runs:

```
dependency → lint → syntax → create → converge → idempotence → destroy → verify
```

> If your cluster uses a self-signed cert, either provide a CA file and keep `k8s_validate_certs: true`, or temporarily set `K8S_AUTH_VERIFY_SSL=false` for tests.

---

## Author
- Chad Elliott (<chelliot@redhat.com>) 

---

## Repository layout (role)

```text
roles/
└─ operatorgroup/
   ├─ README.md                 # ← this file
   ├─ defaults/
   │  └─ main.yml
   ├─ tasks/
   │  ├─ main.yml               # imports present.yml/absent.yml
   │  ├─ present.yml            # create / reconcile
   │  └─ absent.yml             # safe, namespace-aware delete
   ├─ molecule/
   │  └─ default/
   │     ├─ converge.yml
   │     ├─ destroy.yml
   │     ├─ molecule.yml        # includes lint stage
   │     ├─ verify.yml
   │     └─ README.md           # per-scenario guide
   ├─ meta/
   │  └─ main.yml
   ├─ handlers/
   │  └─ main.yml               # (optional)
   └─ vars/
      └─ main.yml               # (optional)
```
