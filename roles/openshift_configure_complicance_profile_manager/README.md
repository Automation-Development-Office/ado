# Role: openshift_configure_complicance_profile_manager

Create or delete a Compliance Operator `ComplianceProfile` resource.

---

## Requirements

- OpenShift/Kubernetes API access.
- `kubernetes.core` collection installed.
- Compliance Operator CRDs installed in the target cluster.

---

## Variables

| Variable | Description |
|---------|-------------|
| `manage_profile` | Action selector. Use `create` or `delete`. |
| `compliance_profile` | Profile resource name. |
| `compliance_profile_title` | Human-readable title used when creating the profile. |
| `compliance_profile_description` | Description used when creating the profile. |
| `compliance_operator_namespace` | Namespace for the ComplianceProfile resource. Defaults to `openshift-compliance`. |

---

## Examples

```yaml
- hosts: localhost
  gather_facts: false
  roles:
    - role: openshift_configure_complicance_profile_manager
      vars:
        manage_profile: create
        compliance_profile: custom-hardening
        compliance_profile_title: Custom Hardening Profile
        compliance_profile_description: Site-specific compliance profile
        compliance_operator_namespace: openshift-compliance
```

---

## Behavior Notes

- Creates a profile when `manage_profile` is `create`.
- Deletes the named profile when `manage_profile` is `delete`.

---

## Molecule

Use the same README layout as the working collection roles so Molecule/README validation sees the expected sections and ordering.

```
dependency -> lint -> syntax -> create -> converge -> idempotence -> destroy -> verify
```

---

## License

GPL-3.0-or-later

---

## Author

Chad Elliott

---

## Repository layout (role)

```text
roles/
`-- openshift_configure_complicance_profile_manager/
    |-- README.md
    |-- defaults/
    |   `-- main.yml
    |-- tasks/
    |   `-- main.yml
    |-- vars/
    |   `-- main.yml
    |-- handlers/
    |   `-- main.yml
    |-- meta/
    |   `-- main.yml
    |-- templates/                # optional
    |-- files/                    # optional
    `-- tests/
        |-- inventory
        `-- test.yml               # optional
```
