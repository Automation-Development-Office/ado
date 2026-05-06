# Role: ado.openshift.lookup_operator_defaults

Lookup recommended **operator defaults** for a given application name (e.g., suggested operator package/channel/catalog settings).  
This role is **read-only** and does not create or modify any cluster resources.

- Deterministic lookup based on `app_name`
- Emits facts you can reuse in install/subscription roles
- Safe to run in CI (no side effects)

---

## Requirements

- Ansible 2.13+ (or compatible with your collection)
- No cluster access required (pure data lookup)

---

## Variables

| Variable   | Description                                   |
|------------|-----------------------------------------------|
| `app_name` | Application short name used for the lookup. **Required.** |

---

## Examples

### Basic usage
```yaml
- hosts: localhost
  gather_facts: false
  roles:
    - role: ado.openshift.lookup_operator_defaults
      vars:
        app_name: web-terminal


```

> The role sets a fact named `operator_defaults` (dict) with fields your collection defines (e.g., `operator_name`, `operator_channel`, `operator_source`, `operator_source_namespace`, etc.). Adjust consumers accordingly.

---

## Behavior Notes

- Pure lookup: the role should only set facts; it should **not** contact the cluster or create resources.
- If `app_name` is unknown, the role should fail clearly or return an empty/default structure (your choice—documented in your tasks).

---

## Molecule

A default Molecule scenario is included and validates:
```
dependency → syntax → create → converge → idempotence → verify
```
No `destroy` step is needed since the role is read-only.

---

## Author
- Chad Elliott (<chelliot@redhat.com>) 

---

## Repository layout (role)

```text
roles/
└─ lookup_operator_defaults/
   ├─ README.md                 # ← this file
   ├─ defaults/
   │  └─ main.yml               # maps app_name → defaults
   ├─ tasks/
   │  └─ main.yml               # sets operator_defaults fact
   ├─ molecule/
   │  └─ default/
   │     ├─ converge.yml
   │     ├─ molecule.yml
   │     ├─ verify.yml
   │     ├─ README.md           # scenario guide (optional)
   │     └─ TEST.md
   ├─ vars/
   │  └─ main.yml               # (optional)
   └─ tests/
      └─ inventory
```
