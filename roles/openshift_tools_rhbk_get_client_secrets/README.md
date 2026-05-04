# Role: openshift_tools_rhbk_get_client_secrets

Look up a Red Hat Build of Keycloak client secret through the admin API and publish the result as Ansible facts.

---

## Requirements

- Network access to the RHBK admin endpoint.
- Valid admin credentials available from variables, vault, or component defaults.

---

## Variables

| Variable | Description |
|---------|-------------|
| `rhbk_component_name_effective` | Component key used to resolve the effective RHBK configuration. Defaults to `rhbk` in the surrounding workflow. |
| `rhbk_secret_client_id / rhbk_secret_client_key` | Client identifier or component-map key used to locate the client. One is required. |
| `rhbk_secret_realm` | Optional realm override. Otherwise the role uses the component default realm. |
| `rhbk_secret_admin_user / rhbk_secret_admin_password` | Optional admin credentials used for the Keycloak token request. |
| `rhbk_secret_target_var` | Optional fact name to receive the fetched client secret value. |

---

## Examples

```yaml
- hosts: localhost
  gather_facts: false
  roles:
    - role: openshift_tools_rhbk_get_client_secrets
      vars:
        rhbk_secret_client_id: grafana
        rhbk_secret_realm: master
        rhbk_secret_target_var: grafana_oidc_client_secret
```

---

## Behavior Notes

- Renders the shared component registry to resolve effective RHBK settings before calling the admin API.
- Publishes the discovered secret value and related metadata as facts for downstream roles.

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
`-- openshift_tools_rhbk_get_client_secrets/
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
