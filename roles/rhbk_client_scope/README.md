# Role: infra.ado.rhbk_client_scope

Manage Red Hat build of Keycloak client scopes and their groups mapper.

## Role Author

Automation Development Office.

## ✅ Role Requirements

- Reachable Red Hat build of Keycloak API endpoint.
- Admin credentials with permission to manage client scopes.
- `ansible.builtin.uri` support from `ansible-core`.

## 📦 Role Variables

Required runtime variables used by tasks:

- `state` (`present` to create/update, `absent` to run deletion path).
- `rhbk_host` (host name for the RHBK instance, without scheme).
- `rhbk_admin_user` (admin username).
- `rhbk_admin_password` (admin password).
- `rhbk_realm` (target realm).
- `rhbk_client_scope_name` (client scope name to manage).
- `rhbk_verify_ssl` (`true`/`false` SSL validation toggle for API calls).

Notes:

- `defaults/main.yml` and `vars/main.yml` currently do not define defaults.
- Create flow ensures a `groups` protocol mapper exists on the target scope.

## 🚀 Role Usage

```yaml
- hosts: localhost
  gather_facts: false
  roles:
    - role: infra.ado.rhbk_client_scope
      vars:
        state: present
        rhbk_host: rhbk.example.com
        rhbk_admin_user: admin
        rhbk_admin_password: "{{ vault_rhbk_admin_password }}"
        rhbk_realm: myrealm
        rhbk_client_scope_name: groups
        rhbk_verify_ssl: false
```

## 🧪 Role Molecule Testing

There is no dedicated extension-level Molecule scenario for this role in the
current repository layout.

## 📁 Role Structure

```text
rhbk_client_scope/
├── defaults/
│   └── main.yml
├── handlers/
│   └── main.yml
├── meta/
│   └── main.yml
├── README.md
├── tasks/
│   ├── main.yml
│   ├── rhbk_create_client_scope.yml
│   └── rhbk_delete_client_scope.yml
└── vars/
    └── main.yml
```
