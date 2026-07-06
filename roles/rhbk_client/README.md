# Role: infra.ado.rhbk_client

Rhbk Client automation role. Primary tasks include: Create RHBK Client; Delete RHBK client; Assert required inputs are set.

## Role Author

Automation Development Office

## ✅ Role Requirements

- Ansible Core
- Required collections listed in `collections/requirements.yml`
- Inventory or extra variables appropriate for the target platform

## 📦 Role Variables

| Variable | Description |
|----------|-------------|
| `rhbk_client_state` | Desired state used by role tasks when supported. |

## 🚀 Role Usage

```yaml
- name: Run rhbk_client
  hosts: localhost
  gather_facts: false
  roles:
    - role: infra.ado.rhbk_client
```

## 🧪 Role Molecule Testing

Run Molecule scenarios from the role directory when a scenario is available.

This role runs tasks such as:

- Create RHBK Client
- Delete RHBK client
- Assert required inputs are set
- Build Keycloak base URL

```bash
cd roles/rhbk_client
molecule test
```

## 📁 Role Structure

```text
roles/rhbk_client/
  README.md
  defaults/
  handlers/
  meta/
  tasks/
  tests/
  vars/
```
