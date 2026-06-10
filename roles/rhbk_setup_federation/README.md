# Role: infra.ado.rhbk_setup_federation

Create and remove LDAP federation providers in Red Hat build of Keycloak.

## Role Author

Automation Development Office.

## ✅ Role Requirements

- Reachable Red Hat build of Keycloak endpoint.
- Admin credentials with permission to manage realm federation components.
- `redhat.rhbk` collection for `redhat.rhbk.keycloak_user_federation`.

## 📦 Role Variables

Required runtime variables:

- `state` (`present` to create federation, `absent` to remove federation).
- `rhbk_host` (RHBK host used by federation module calls).
- `rhbk_admin_user` (admin username).
- `rhbk_admin_password` (admin password).
- `rhbk_realm` (target realm name).
- `rhbk_verify_ssl` (`true`/`false` SSL validation flag).

Create path variables (`state: present`):

- `rhbk_federation_name` (name of the LDAP federation provider to ensure).
- `ldap_config` (LDAP provider configuration dictionary).

Delete path behavior (`state: absent`):

- Removes the LDAP federation provider named by `rhbk_federation_name`.
- Uses the same `redhat.rhbk.keycloak_user_federation` module flow as create path.

Notes:

- `defaults/main.yml` and `vars/main.yml` currently do not define role defaults.

## 🚀 Role Usage

```yaml
- hosts: localhost
  gather_facts: false
  roles:
    - role: infra.ado.rhbk_setup_federation
      vars:
        state: present
        rhbk_host: rhbk.example.com
        rhbk_admin_user: admin
        rhbk_admin_password: "{{ vault_rhbk_admin_password }}"
        rhbk_realm: myrealm
        rhbk_verify_ssl: false
        rhbk_federation_name: IDM
        ldap_config:
          enabled: true
```

## 🧪 Role Molecule Testing

There is no dedicated extension-level Molecule scenario for this role in the
current repository layout.

## 📁 Role Structure

```text
rhbk_setup_federation/
├── defaults/
│   └── main.yml
├── handlers/
│   └── main.yml
├── meta/
│   └── main.yml
├── README.md
├── tasks/
│   ├── main.yml
│   ├── rhbk_setup_ldap_federation.yml
│   └── rhbk_remove_ldap_federation.yml
└── vars/
    └── main.yml
```
