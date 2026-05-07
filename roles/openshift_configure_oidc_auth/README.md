# Role: openshift_configure_oidc_auth

Configure OpenShift OAuth to use an OIDC identity provider.

---

## Requirements

- OpenShift/Kubernetes API access.
- `kubernetes.core` collection installed.
- OIDC client configuration and secrets available from inventory or vault.

---

## Variables

| Variable | Description |
|---------|-------------|
| `openshift_oidc_auth_config` | Primary caller-provided OIDC configuration structure consumed by the role. |
| `state` | Desired state for the OIDC configuration workflow. |
| `validate_certs` | TLS verification toggle when talking to the cluster or provider, where applicable. |

---

## Examples

```yaml
- hosts: localhost
  gather_facts: false
  roles:
    - role: openshift_configure_oidc_auth
      vars:
        state: present
        openshift_oidc_auth_config:
          idp_name: keycloak
          issuer_url: https://sso.example.com/realms/master
          client_id: openshift
          client_secret: "{{ vault_oidc_client_secret }}
```

---

## Behavior Notes

- Intended for managing OpenShift OAuth OIDC provider settings.
- Keep caller-provided secret values in vault and out of plain-text inventories.

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
`-- openshift_configure_oidc_auth/
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
