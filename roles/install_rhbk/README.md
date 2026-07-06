# Role: infra.ado.install_rhbk

Install Rhbk automation role. Primary tasks include: Delete Keycloak Custom Resource; Delete PostgreSQL Service; Delete PostgreSQL StatefulSet.

## Role Author

Automation Development Office

## ✅ Role Requirements

- Ansible Core
- Required collections listed in `collections/requirements.yml`
- Inventory or extra variables appropriate for the target platform

## 📦 Role Variables

| Variable | Description |
|----------|-------------|
| `install_rhbk_state` | Desired state used by role tasks when supported. |

## 🚀 Role Usage

```yaml
- name: Run install_rhbk
  hosts: localhost
  gather_facts: false
  roles:
    - role: infra.ado.install_rhbk
```

## 🧪 Role Molecule Testing

Run Molecule scenarios from the role directory when a scenario is available.

This role runs tasks such as:

- Delete Keycloak Custom Resource
- Delete PostgreSQL Service
- Delete PostgreSQL StatefulSet
- Delete PVC from StatefulSet

```bash
cd roles/install_rhbk
molecule test
```

## 📁 Role Structure

```text
roles/install_rhbk/
  README.md
  defaults/
  handlers/
  meta/
  tasks/
  tests/
  vars/
```
