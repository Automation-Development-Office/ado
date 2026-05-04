# Role: openshift_configure_ldap_auth

Append an LDAP identity provider to the cluster OAuth configuration without disturbing existing providers.

---

## Requirements

- OpenShift/Kubernetes API access.
- `kubernetes.core` collection installed.
- A `ldap_config` structure available from vault or inventory.

---

## Variables

| Variable | Description |
|---------|-------------|
| `ldap_config` | Source-of-truth structure containing connection URL, bind DN, password, and user search details. Required. |
| `openshift_ldap_auth_config` | Optional override structure merged on top of the derived LDAP configuration. |
| `openshift_ldap_no_log` | Controls log redaction for sensitive values. Defaults to true when defined by caller. |

---

## Examples

```yaml
- hosts: localhost
  gather_facts: false
  roles:
    - role: openshift_configure_ldap_auth
      vars:
        ldap_config:
          connectionUrl: ldaps://ldap.example.com:636
          bindDn: cn=admin,dc=example,dc=com
          bindCredential: "{{ vault_ldap_password }}"
          usersDn: ou=people,dc=example,dc=com
          usernameLDAPAttribute: uid
```

---

## Behavior Notes

- Builds a derived LDAP configuration and stores the bind password in a secret in `openshift-config`.
- Appends the LDAP provider only if it is not already present in the OAuth object.

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
`-- openshift_configure_ldap_auth/
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
