# Role: infra.ado.rhbk_realm

Rhbk Realm automation role. Primary tasks include: Create RHBK realm; Delete RHBK realm; Create or update Keycloak realm.

## Role Author

Automation Development Office

## ✅ Role Requirements

- Ansible Core
- Required collections listed in `collections/requirements.yml`
- Inventory or extra variables appropriate for the target platform

## 📦 Role Variables

| Variable | Description |
|----------|-------------|
| `rhbk_realm_verify_ssl` | Validation or TLS verification setting used by this role. |

## 🚀 Role Usage

```yaml
- name: Run rhbk_realm
  hosts: localhost
  gather_facts: false
  roles:
    - role: infra.ado.rhbk_realm
```

## 🧪 Role Molecule Testing

Run Molecule scenarios from the role directory when a scenario is available.

This role runs tasks such as:

- Create RHBK realm
- Delete RHBK realm
- Create or update Keycloak realm
- Login to RHBK and get admin token

```bash
cd roles/rhbk_realm
molecule test
```

## 📁 Role Structure

```text
roles/rhbk_realm/
  README.md
  defaults/
  handlers/
  meta/
  tasks/
  tests/
  vars/
```
