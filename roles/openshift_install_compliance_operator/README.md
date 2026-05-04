# Role: openshift_install_compliance_operator

Validate that Compliance Operator pods are present and at least one pod reaches the Running phase.

---

## Requirements

- OpenShift/Kubernetes API access.
- `kubernetes.core` collection installed.
- Compliance Operator already deployed in the target namespace.

---

## Variables

| Variable | Description |
|---------|-------------|
| `name_space` | Namespace to inspect. Defaults to `openshift-compliance`. |

---

## Examples

```yaml
- hosts: localhost
  gather_facts: false
  roles:
    - role: openshift_install_compliance_operator
      vars:
        name_space: openshift-compliance
```

---

## Behavior Notes

- Reads pods from the Compliance Operator namespace and records whether a Running pod exists.
- Use this role as a post-install validation step.

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
`-- openshift_install_compliance_operator/
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
