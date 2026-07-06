# Role: infra.ado.ocp_devspaces

Ocp Devspaces automation role. Primary tasks include: Delete Devspaces instance using Operator; Resolve DevSpaces namespaces; Wait for Dev Spaces CSV to reach 'Succeeded.

## Role Author

Automation Development Office

## ✅ Role Requirements

- Ansible Core
- Required collections listed in `collections/requirements.yml`
- Inventory or extra variables appropriate for the target platform

## 📦 Role Variables

| Variable | Description |
|----------|-------------|
| `ocp_devspaces_state` | Desired state used by role tasks when supported. |

## 🚀 Role Usage

```yaml
- name: Run ocp_devspaces
  hosts: localhost
  gather_facts: false
  roles:
    - role: infra.ado.ocp_devspaces
```

## 🧪 Role Molecule Testing

Run Molecule scenarios from the role directory when a scenario is available.

This role runs tasks such as:

- Delete Devspaces instance using Operator
- Resolve DevSpaces namespaces
- Wait for Dev Spaces CSV to reach 'Succeeded
- Ensure DevSpaces app namespace exists

```bash
cd roles/ocp_devspaces
molecule test
```

## 📁 Role Structure

```text
roles/ocp_devspaces/
  README.md
  defaults/
  handlers/
  meta/
  tasks/
  tests/
  vars/
```
