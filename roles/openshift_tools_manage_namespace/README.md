# Role: ado.openshift.namespace

Ensure an OpenShift **Namespace** is present or absent.

- Idempotent creation/update of a namespace (labels/annotations optional)
- Safe deletion path (handles “already gone” cleanly)
- Works with kubeconfig **or** host+token auth

---

## Requirements

- OpenShift/Kubernetes API access (via kubeconfig or env vars)
- `kubernetes.core` collection installed

---

## Variables

| Variable | Description |
|---------|-------------|
| `name_space` | Namespace name to ensure present/absent. **Required**. |
| `state` | Desired state: `present` (default) or `absent`. |
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

### Ensure a namespace exists
```yaml
- hosts: localhost
  gather_facts: false
  roles:
    - role: ado.openshift.namespace
      vars:
        name_space: my-app
        state: present
        validate_certs: true
```

### Delete a namespace (ignore if already gone)
```yaml
- hosts: localhost
  gather_facts: false
  roles:
    - role: ado.openshift.namespace
      vars:
        name_space: my-app
        state: absent
        validate_certs: true
```

---

## Behavior Notes

- Creation uses `kubernetes.core.k8s` with `state: present`; deletion uses `state: absent`.
- When `state: present`, labels/annotations are **merged** with existing metadata where supported.
- Delete path is tolerant of “NotFound” and logs an informational message.
- For clusters with self-signed certs, either provide a CA file and keep `k8s_validate_certs: true`, or set `K8S_AUTH_VERIFY_SSL=false` for tests/labs.

---

## Molecule

A default Molecule scenario is included for this role. It runs:

```
dependency → lint → syntax → create → converge → idempotence → destroy → verify
```

- Creates the test namespace during **converge**
- Re-runs converge expecting **changed=0** (**idempotence**)
- Deletes the namespace during **destroy**
- Performs README and basic checks during **verify**

> Remember to export either kubeconfig or host+token variables before running tests.

---

## Author
- Chad Elliott (<chelliot@redhat.com>) 

---

## Repository layout (role)

```text
roles/
└─ namespace/
   ├─ README.md                 # ← this file
   ├─ defaults/
   │  └─ main.yml
   ├─ tasks/
   │  ├─ main.yml
   │  ├─ present.yml            # (optional)
   │  └─ absent.yml             # (optional)
   ├─ molecule/
   │  └─ default/
   │     ├─ converge.yml
   │     ├─ destroy.yml
   │     ├─ molecule.yml        # includes lint stage
   │     ├─ verify.yml
   │     └─ README.md           # per-scenario guide
   ├─ vars/
   │  └─ main.yml               # (optional)
   ├─ handlers/
   │  └─ main.yml               # (optional)
   ├─ templates/                # (optional)
   └─ files/                    # (optional)
```
