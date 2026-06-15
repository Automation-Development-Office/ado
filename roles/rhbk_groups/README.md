# Role: infra.ado.rhbk_groups

Create and delete groups in Red Hat build of Keycloak realms.

## Role Author

Automation Development Office.

## ✅ Role Requirements

- Reachable Red Hat build of Keycloak endpoint and realm.
- Credentials with permission to manage groups.
- `community.general` collection for `community.general.keycloak_group` in create flow.

## 📦 Role Variables

Required runtime variables used by role tasks:

- `state` (`present` to create, `absent` to delete).
- `rhbk_group_name` (group name to manage).
- `rhbk_realm` (target realm).
- `rhbk_verify_ssl` (`true`/`false` SSL validation toggle).

Create path variables (`state: present`):

- `rhbk_hostname` (Keycloak base URL for `community.general.keycloak_group`).
- `rhbk_username` (admin username for create flow).
- `rhbk_password` (admin password for create flow).

Delete path variables (`state: absent`):

- `rhbk_host` (host used by delete flow API URI tasks).
- `rhbk_admin_user` (admin username for token request).
- `rhbk_admin_password` (admin password for token request).

Notes:

- `defaults/main.yml` and `vars/main.yml` currently do not define defaults.
- The create and delete task files currently use different auth variable names.

## 🚀 Role Usage

```yaml
- hosts: localhost
  gather_facts: false
  roles:
    - role: infra.ado.rhbk_groups
      vars:
        state: present
        rhbk_group_name: platform-admins
        rhbk_realm: myrealm
        rhbk_verify_ssl: false
        rhbk_hostname: "https://rhbk.example.com"
        rhbk_username: admin
        rhbk_password: "{{ vault_rhbk_password }}"
```

## 🧪 Role Molecule Testing

There is no dedicated extension-level Molecule scenario for this role in the
current repository layout.

## 📁 Role Structure

```text
rhbk_groups/
├── defaults/
│   └── main.yml
├── handlers/
│   └── main.yml
├── meta/
│   └── main.yml
├── README.md
├── tasks/
│   ├── main.yml
│   ├── rhbk_create_group.yml
│   └── rhbk_remove_group.yml
└── vars/
    └── main.yml
```
