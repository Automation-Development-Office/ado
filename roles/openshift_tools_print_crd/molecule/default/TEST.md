# Role: ado.openshift.print_crd

Assemble and output an **ordered manifest** where all **CustomResourceDefinitions (CRDs)**
are listed **before** their dependent resources. This prevents “CRD not found” errors
during installs and makes operator/app bundles safe to apply in one shot.

- Splits a mixed YAML bundle into **CRDs first → then everything else**.
- Idempotent: stable ordering for repeated runs and CI.
- Works with kubeconfig **or** host+token auth; configurable TLS verification.

---

## Requirements

- OpenShift/Kubernetes API access (env or kubeconfig).
- `kubernetes.core` collection.

---

## Variables

| Variable | Description |
|---------|-------------|
| `manifest_docs` | **Required.** List of YAML docs (dicts) to order. Usually from `from_yaml_all`. |
| `validate_certs` | TLS verification for API calls (`true` with trusted CA; `false` for lab/self‑signed). |
| `output_path` | Optional file path to write the final, ordered manifest (YAML). If omitted, role prints to screen/log. |
| `apply_after_print` | If `true`, the role will also **apply** the ordered manifest to the cluster using `kubernetes.core.k8s`. Default: `false`. |

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

### Order a local bundle and print to STDOUT
```yaml
- hosts: localhost
  gather_facts: false
  roles:
    - role: ado.openshift.print_crd
      vars:
        manifest_docs: >-
          {{ lookup('file', 'bundle.yaml') | from_yaml_all | list }}
        validate_certs: true
```

### Order a bundle, save to file, and apply
```yaml
- hosts: localhost
  gather_facts: false
  roles:
    - role: ado.openshift.print_crd
      vars:
        manifest_docs: >-
          {{ lookup('file', 'bundle.yaml') | from_yaml_all | list }}
        output_path: ordered-bundle.yaml
        apply_after_print: true
        validate_certs: false
```

### Feed multiple sources (files, templates) into one ordered manifest
```yaml
- hosts: localhost
  gather_facts: false
  vars:
    parts:
      - "{{ lookup('file', 'operators.yaml') | from_yaml_all | list }}"
      - "{{ lookup('template', 'app.tmpl.yaml') | from_yaml_all | list }}"
  roles:
    - role: ado.openshift.print_crd
      vars:
        manifest_docs: "{{ parts | flatten(levels=1) }}"
        output_path: stitched.yaml
        validate_certs: true
```

---

## Behavior Notes

- **Ordering:** Anything with `kind: CustomResourceDefinition` is emitted first; all other kinds follow in read order.
- **Safety:** If no CRDs exist in input, the role outputs the non‑CRD resources unchanged.
- **Apply path:** When `apply_after_print: true`, resources are applied in the same ordered sequence using `kubernetes.core.k8s`.
- **Output:** With `output_path` set, the ordered manifest is written to disk; otherwise it’s printed/logged.
- **Idempotence:** The same input produces the same ordered output, supporting reproducible CI. 

---

## Molecule

A default Molecule scenario is included and focuses on ordering + idempotence:

```
dependency → lint → syntax → create → converge → idempotence → destroy → verify
```

> For clusters with self‑signed certs, either provide a CA file and keep `k8s_validate_certs: true`, or temporarily set `K8S_AUTH_VERIFY_SSL=false` for tests.

---

## Author
- Chad Elliott (<chelliot@redhat.com>)

---

## Repository layout (role)

```text
roles/
└─ print_crd/
   ├─ README.md                 # ← this file
   ├─ defaults/
   │  └─ main.yml
   ├─ tasks/
   │  ├─ main.yml               # imports present.yml/absent.yml or inline tasks
   │  ├─ order.yml              # split into CRD vs other kinds
   │  └─ apply.yml              # optional, gated by apply_after_print
   ├─ molecule/
   │  └─ default/
   │     ├─ converge.yml
   │     ├─ destroy.yml
   │     ├─ molecule.yml        # includes lint stage
   │     ├─ verify.yml
   │     └─ TEST.md             # per-scenario guide
   ├─ meta/
   │  └─ main.yml
   └─ vars/
      └─ main.yml               # (optional)
```
