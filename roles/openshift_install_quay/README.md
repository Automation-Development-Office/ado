# Role: openshift_install_quay

Install or remove a Quay deployment including backing PostgreSQL, configuration secret, and route.

---

## Requirements

- OpenShift/Kubernetes API access.
- `kubernetes.core` collection installed.

---

## Variables

| Variable | Description |
|---------|-------------|
| `state` | Desired state: `present` installs resources and `absent` removes the namespace. |
| `name_space` | Namespace where Quay resources are managed. |
| `storage_size / storage` | PVC sizing and storage class inputs. |
| `quay_hostname` | External route host name for Quay. |
| `quay_admin_user / quay_admin_password` | Bootstrap admin credentials. |
| `quay_config_secret` | Secret name used for `config.yaml`. |
| `postgres_image` | Container image used for the PostgreSQL backing service. |

---

## Examples

```yaml
- hosts: localhost
  gather_facts: false
  roles:
    - role: openshift_install_quay
      vars:
        state: present
        name_space: quay-enterprise
        storage_size: 100Gi
        storage: gp3-csi
        quay_hostname: quay.apps.example.com
        quay_admin_user: admin
        quay_admin_password: "{{ vault_quay_password }}"
        quay_config_secret: quay-config
        postgres_image: registry.redhat.io/rhel8/postgresql-13
```

---

## Behavior Notes

- Install mode creates namespace, PVC, PostgreSQL, Quay deployment, and route resources.
- Absent mode removes the Quay namespace.

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
`-- openshift_install_quay/
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
