# Role: openshift_tools_update_pull_secrets

Add or remove a registry authentication entry inside the cluster pull secret.

---

## Requirements

- OpenShift/Kubernetes API access.
- `kubernetes.core` collection installed.
- Access to the `openshift-config/pull-secret` secret or an alternate target provided by variables.

---

## Variables

| Variable | Description |
|---------|-------------|
| `state` | Desired state: `present` or `absent`. Required. |
| `update_pull_secret_name / update_pull_secret_namespace` | Target pull secret name and namespace. Defaults to `pull-secret` in `openshift-config`. |
| `registry_host` | Registry host to add or remove. Required. |
| `registry_username / registry_password` | Registry credentials required when `state: present`. |
| `registry_email` | Optional email stored with the registry auth entry. |

---

## Examples

```yaml
- hosts: localhost
  gather_facts: false
  roles:
    - role: openshift_tools_update_pull_secrets
      vars:
        state: present
        registry_host: registry.example.com
        registry_username: svc-account
        registry_password: "{{ vault_registry_password }}"
        registry_email: ops@example.com
```

---

## Behavior Notes

- Reads, decodes, updates, and patches the `.dockerconfigjson` content in place.
- Only writes the secret back when the rendered auth document actually changes.

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
`-- openshift_tools_update_pull_secrets/
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
