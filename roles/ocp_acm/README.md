# Role: infra.ado.ocp_acm

Ocp Acm automation role. Primary tasks include: Deploy MultiClusterHub CR; Install ACM operator.

## Role Author

Automation Development Office

## ✅ Role Requirements

- Ansible Core
- Required collections listed in `collections/requirements.yml`
- Inventory or extra variables appropriate for the target platform

## 📦 Role Variables

| Variable | Description |
|----------|-------------|
| `ocp_acm_state` | Desired state used by role tasks when supported. |

## 🚀 Role Usage

```yaml
- name: Run ocp_acm
  hosts: localhost
  gather_facts: false
  roles:
    - role: infra.ado.ocp_acm
```

## 🧪 Role Molecule Testing

Run Molecule scenarios from the role directory when a scenario is available.

This role runs tasks such as:

- Deploy MultiClusterHub CR
- Install ACM operator

```bash
cd roles/ocp_acm
molecule test
```

## 📁 Role Structure

```text
roles/ocp_acm/
  README.md
  defaults/
  handlers/
  meta/
  tasks/
  tests/
  vars/
```
