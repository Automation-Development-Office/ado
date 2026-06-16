# Role: infra.ado.rhbk_setup_mapper

Manage LDAP group mapper components in Red Hat build of Keycloak.

## Role Author

Automation Development Office.

## ✅ Role Requirements

- Reachable Red Hat build of Keycloak endpoint and admin API.
- Realm admin credentials with permission to manage components.
- Input variables for mapper and federation selection.

## 📦 Role Variables

| Variable | Description |
| -------- | ----------- |
| `state` | Required. Use `present` to create mapper and `absent` to delete mapper. |
| `rhbk_host` | Required. RHBK host name used for admin API calls. |
| `rhbk_realm` | Required. Realm where LDAP mapper is managed. |
| `rhbk_admin_user` | Required. Admin username for token acquisition. |
| `rhbk_admin_password` | Required. Admin password for token acquisition. |
| `rhbk_verify_ssl` | Optional. Boolean SSL verification flag for API requests. |
| `rhbk_federation_name` | Required for `present`. LDAP federation component name to attach mapper to. |
| `ldap_group_config` | Required for `present`. Mapper configuration dictionary sent as component config. |

## 🚀 Role Usage

```yaml
- hosts: localhost
  gather_facts: false
  roles:
    - role: infra.ado.rhbk_setup_mapper
      vars:
        state: present
        rhbk_host: rhbk.example.com
        rhbk_realm: demo
        rhbk_admin_user: admin
        rhbk_admin_password: "{{ vault_rhbk_admin_password }}"
        rhbk_verify_ssl: false
        rhbk_federation_name: IDM
        ldap_group_config:
          groups.dn:
            - "ou=Groups,dc=example,dc=com"
          mode:
            - "LDAP_ONLY"
          membership.ldap.attribute:
            - "member"
```

## 🧪 Role Molecule Testing

There is no dedicated extension-level Molecule scenario for this role in the current repository layout.

## 📁 Role Structure

```text
rhbk_setup_mapper/
├── defaults/
│   └── main.yml
├── handlers/
│   └── main.yml
├── meta/
│   └── main.yml
├── README.md
├── tasks/
│   ├── main.yml
│   ├── rhbk_setup_group_mapper.yml
│   └── rhbk_remove_group_mapper.yml
└── vars/
    └── main.yml
```
