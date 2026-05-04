# Role: openshift_install_rhbk

Install or remove a Red Hat Build of Keycloak deployment with PostgreSQL and TLS configuration.

---

## Requirements

- OpenShift/Kubernetes API access.
- `kubernetes.core` collection installed.
- RHBK operator installed before the custom resource is created.

---

## Variables

| Variable | Description |
|---------|-------------|
| `state` | Desired state: `present` or `absent`. |
| `name_space` | Namespace where Keycloak and PostgreSQL resources are managed. |
| `rhbk_hostname` | External host name for Keycloak. Required. |
| `rhbk_admin_user / rhbk_admin_password` | Bootstrap admin credentials. |
| `rhbk_db_user / rhbk_db_password` | Database credentials stored in the generated secret. |
| `cert_manager` | Boolean toggle to use cert-manager instead of manual TLS secret creation. |
| `rhbk_issuer_name / rhbk_issuer_kind` | Issuer reference used when `cert_manager: true`. |
| `tls_crt / tls_key` | Manual TLS values used when `cert_manager: false`. |

---

## Examples

```yaml
- hosts: localhost
  gather_facts: false
  roles:
    - role: openshift_install_rhbk
      vars:
        state: present
        name_space: rhbk
        rhbk_hostname: sso.apps.example.com
        rhbk_admin_user: admin
        rhbk_admin_password: "{{ vault_rhbk_admin_password }}"
        rhbk_db_user: keycloak
        rhbk_db_password: "{{ vault_rhbk_db_password }}"
        cert_manager: false
        tls_crt: "{{ vault_rhbk_tls_crt }}"
        tls_key: "{{ vault_rhbk_tls_key }}
```

---

## Behavior Notes

- Creates supporting secrets and PostgreSQL objects before creating the Keycloak custom resource.
- Delete mode removes the custom resource and supporting secrets, services, and stateful resources.

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
`-- openshift_install_rhbk/
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
