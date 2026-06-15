# Role: infra.ado.rhbk_client

Manage Red Hat build of Keycloak (RHBK) clients by creating/updating or deleting
realm clients.

## Role Author

Chad Elliott / Automation Development Office.

## ✅ Role Requirements

- `community.general` collection for `community.general.keycloak_client`.
- Reachable RHBK/Keycloak endpoint.
- Credentials with permission to manage clients in the target realm.

## 📦 Role Variables

Main flow variable:

- `state` (`present` to create/update, `absent` to delete).

Common variables used by role tasks:

- `rhbk_admin_user`
- `rhbk_admin_password`
- `rhbk_realm`
- `rhbk_verify_ssl` (optional, boolean)

Create/update path (`state: present`) uses:

- `rhbk_hostname`
- `rhbk_client`
- Optional advanced settings such as `rhbk_client_secret`,
  `rhbk_redirect_uris`, `rhbk_web_origins`, `rhbk_protocol_mappers`,
  `rhbk_attributes`, and other `rhbk_*` client options in
  `tasks/rhbk_create_client.yml`.

Delete path (`state: absent`) uses:

- `rhbk_host`
- `rhbk_client_id`
- `rhbk_realm`
- `rhbk_admin_user`
- `rhbk_admin_password`

Note: `defaults/main.yml` does not currently define default variable values.

## 🚀 Role Usage

Create or update a client:

```yaml
- hosts: localhost
  gather_facts: false
  roles:
    - role: infra.ado.rhbk_client
      vars:
        state: present
        rhbk_hostname: rhbk.example.com
        rhbk_admin_user: admin
        rhbk_admin_password: "{{ vault_rhbk_admin_password }}"
        rhbk_realm: myrealm
        rhbk_client: my-client
        rhbk_verify_ssl: true
```

Delete a client:

```yaml
- hosts: localhost
  gather_facts: false
  roles:
    - role: infra.ado.rhbk_client
      vars:
        state: absent
        rhbk_host: rhbk.example.com
        rhbk_admin_user: admin
        rhbk_admin_password: "{{ vault_rhbk_admin_password }}"
        rhbk_realm: myrealm
        rhbk_client_id: my-client
        rhbk_verify_ssl: true
```

## 🧪 Role Molecule Testing

No extension-level Molecule scenario is currently defined for this role under
`extensions/molecule/integration_*`.

To verify this README format:

```bash
python scripts/verify_readme.py roles/rhbk_client/README.md --template docs/templates/role_readme_format_template.md
```

## 📁 Role Structure

```text
rhbk_client/
├── defaults/
│   └── main.yml
├── handlers/
│   └── main.yml
├── meta/
│   └── main.yml
├── README.md
├── tasks/
│   ├── main.yml
│   ├── rhbk_create_client.yml
│   └── rhbk_delete_client.yml
├── tests/
│   ├── inventory
│   └── test.yml
└── vars/
    └── main.yml
```
