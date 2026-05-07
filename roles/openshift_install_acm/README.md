# Role: openshift_install_acm

Install or configure Red Hat Advanced Cluster Management by applying a `MultiClusterHub` resource.

---

## Requirements

- OpenShift/Kubernetes API access.
- `kubernetes.core` collection installed.
- ACM operator installed before this role runs.

---

## Variables

| Variable | Description |
|---------|-------------|
| `state` | Desired state. The current task file applies the install path when `state: present`. |
| `name_space` | Namespace where the `MultiClusterHub` resource is created. Required. |

---

## Examples

```yaml
- hosts: localhost
  gather_facts: false
  roles:
    - role: openshift_install_acm
      vars:
        state: present
        name_space: open-cluster-management
```

---

## Behavior Notes

- Imports `tasks/install-acm.yml` for the install workflow.
- Creates a `MultiClusterHub` resource named `multiclusterhub` in the target namespace.

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
`-- openshift_install_acm/
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
