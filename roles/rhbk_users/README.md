# Role: infra.ado.rhbk_users

Manage Red Hat build of Keycloak users and user-group membership operations.

## Role Author

Automation Development Office.

## ✅ Role Requirements

- Reachable Red Hat build of Keycloak endpoint with admin API access.
- Realm admin credentials for user and group management.
- Current role implementation uses a mix of:
  - `community.general.keycloak_user` for create
  - direct `ansible.builtin.uri` calls for delete and group membership actions
- Red Hat collection path exists for equivalent operations:
  - `redhat.rhbk.keycloak_user`
  - `redhat.rhbk.keycloak_user_group_mapping`

## 📦 Role Variables

| Variable | Description |
| -------- | ----------- |
| `state` | Required. Supported values: `present`, `absent`, `add_user_to_group`, `remove_user_from_group`. |
| `rhbk_realm` | Required. Target realm. |
| `rhbk_verify_ssl` | Optional. SSL verification flag for URI-based calls. |
| `rhbk_user_username` | Required for `absent`, `add_user_to_group`, and `remove_user_from_group` paths. Username to look up. |
| `rhbk_group_name` | Required for `add_user_to_group` and `remove_user_from_group` paths. Group name to map/unmap. |
| `rhbk_host` | Required for URI-based paths. RHBK host used in REST endpoints. |
| `rhbk_admin_user` | Required for URI-based paths. Admin username for token acquisition. |
| `rhbk_admin_password` | Required for URI-based paths. Admin password for token acquisition. |
| `rhbk_hostname` | Required for `present` path. Keycloak URL passed to `community.general.keycloak_user`. |
| `rhbk_username` | Required for `present` path. Admin username passed to `community.general.keycloak_user`. |
| `rhbk_password` | Required for `present` path. Admin password passed to `community.general.keycloak_user`. |
| `rhbk_new_username` | Required for `present` path. Username of user to create. |
| `rhbk_new_firstname` | Optional for `present` path. First name for new user. |
| `rhbk_new_lastname` | Optional for `present` path. Last name for new user. |
| `rhbk_new_email` | Optional for `present` path. Email for new user. |
| `rhbk_user_enabled` | Optional for `present` path. Enable/disable user. |
| `rhbk_user_email_verified` | Optional for `present` path. Email verification flag. |
| `rhbk_new_user_pwd` | Required for `present` path. Initial user password value. |
| `rhbk_user_pwd_temporary` | Optional for `present` path. Temporary-password flag. |

## 🚀 Role Usage

```yaml
- hosts: localhost
  gather_facts: false
  roles:
    - role: infra.ado.rhbk_users
      vars:
        state: add_user_to_group
        rhbk_host: rhbk.example.com
        rhbk_admin_user: admin
        rhbk_admin_password: "{{ vault_rhbk_admin_password }}"
        rhbk_realm: myrealm
        rhbk_verify_ssl: false
        rhbk_user_username: user1
        rhbk_group_name: platform-admins
```

## 🧪 Role Molecule Testing

There is no dedicated extension-level Molecule scenario for this role in the current repository layout.

## 📁 Role Structure

```text
rhbk_users/
├── defaults/
│   └── main.yml
├── handlers/
│   └── main.yml
├── meta/
│   └── main.yml
├── README.md
├── tasks/
│   ├── main.yml
│   ├── rhbk_add_user_to_group.yml
│   ├── rhbk_create_user.yml
│   ├── rhbk_remove_user.yml
│   └── rhbk_remove_user_from_group.yml
└── vars/
    └── main.yml
```
