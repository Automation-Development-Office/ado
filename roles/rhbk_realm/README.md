# Role: infra.ado.rhbk_realm

Create and delete realms in Red Hat build of Keycloak.

## Role Author

Automation Development Office.

## ✅ Role Requirements

- Reachable Red Hat build of Keycloak endpoint.
- Admin credentials with permission to manage realms.
- `community.general` collection for `community.general.keycloak_realm`.

## 📦 Role Variables

Required runtime variables:

- `state` (`present` to create/update, `absent` to delete).
- `rhbk_realm` (realm name).
- `rhbk_admin_user` (admin username).
- `rhbk_admin_password` (admin password).

Create path variables (`state: present`):

- `rhbk_hostname` (host name used by `community.general.keycloak_realm`).
- `rhbk_verify_ssl` (SSL validation flag used by create/delete tasks).
- Optional realm settings prefixed with `rhbk_` (for example `rhbk_enabled`, `rhbk_display_name`, token/session values, theme values, events, and flow bindings).

Delete path variables (`state: absent`):

- `rhbk_host` (host name used by delete URI API calls).
- `rhbk_verify_ssl` (SSL validation flag for URI calls).

Notes:

- `defaults/main.yml` defines `rhbk_realm_verify_ssl`, but current tasks use `rhbk_verify_ssl`.
- `vars/main.yml` currently does not define runtime variables.

## 🚀 Role Usage

```yaml
- hosts: localhost
  gather_facts: false
  roles:
    - role: infra.ado.rhbk_realm
      vars:
        state: present
        rhbk_realm: myrealm
        rhbk_hostname: rhbk.example.com
        rhbk_admin_user: admin
        rhbk_admin_password: "{{ vault_rhbk_admin_password }}"
        rhbk_verify_ssl: false
        rhbk_enabled: true
        rhbk_display_name: "My Realm"
```

## 🧪 Role Molecule Testing

There is no dedicated extension-level Molecule scenario for this role in the
current repository layout.

## 📁 Role Structure

```text
rhbk_realm/
├── defaults/
│   └── main.yml
├── handlers/
│   └── main.yml
├── meta/
│   └── main.yml
├── README.md
├── tasks/
│   ├── main.yml
│   ├── rhbk_create_realm.yml
│   └── rhbk_delete_realm.yml
└── vars/
    └── main.yml
```
