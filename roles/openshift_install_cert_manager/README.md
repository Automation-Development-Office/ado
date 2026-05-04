# Role: openshift_install_cert_manager

Create cert-manager CA issuer resources and optionally generate intermediate CA material from AWS PCA.

---

## Requirements

- OpenShift/Kubernetes API access.
- `kubernetes.core` collection installed.
- cert-manager installed in the target cluster.
- When AWS PCA mode is enabled, `openssl` and the AWS CLI must be available on the control node.

---

## Variables

| Variable | Description |
|---------|-------------|
| `state` | Desired state. Use `present` for the current install path. |
| `name_space` | Namespace used for the TLS secret and namespaced issuer resources. |
| `cert_manager_root_ca_secret_name` | Name of the TLS secret that stores the CA certificate and key. |
| `cert_manager_root_ca_issuer_name` | Issuer or ClusterIssuer name to create. |
| `cert_manager_root_ca_is_cluster_issuer` | Boolean toggle to create a `ClusterIssuer` instead of an `Issuer`. |
| `cert_manager_tls_crt / cert_manager_tls_key` | Manual CA certificate and key values. |
| `cert_manager_root_ca_awspca_enabled` | Enable AWS PCA workflow for generating CA material. |

---

## Examples

```yaml
- hosts: localhost
  gather_facts: false
  roles:
    - role: openshift_install_cert_manager
      vars:
        state: present
        name_space: cert-manager
        cert_manager_root_ca_secret_name: root-ca-secret
        cert_manager_root_ca_issuer_name: root-ca-issuer
        cert_manager_root_ca_is_cluster_issuer: true
        cert_manager_tls_crt: "{{ vault_ca_crt }}"
        cert_manager_tls_key: "{{ vault_ca_key }}
```

---

## Behavior Notes

- Creates the TLS secret first, then creates an Issuer or ClusterIssuer.
- When AWS PCA mode is enabled, the role can generate intermediate CA material before creating the secret.

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
`-- openshift_install_cert_manager/
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
