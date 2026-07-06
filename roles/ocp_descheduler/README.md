# Role: infra.ado.ocp_descheduler

Ocp Descheduler automation role. Primary tasks include: Create/Delete Kube Descheduler Instance; Kube descheduler task.

## Role Author

Automation Development Office

## ✅ Role Requirements

- Ansible Core
- Required collections listed in `collections/requirements.yml`
- Inventory or extra variables appropriate for the target platform

## 📦 Role Variables

| Variable | Description |
|----------|-------------|
| `ocp_descheduler_state` | Desired state used by role tasks when supported. |

## 🚀 Role Usage

```yaml
- name: Run ocp_descheduler
  hosts: localhost
  gather_facts: false
  roles:
    - role: infra.ado.ocp_descheduler
```

## 🧪 Role Molecule Testing

Run Molecule scenarios from the role directory when a scenario is available.

This role runs tasks such as:

- Create/Delete Kube Descheduler Instance
- Kube descheduler task

```bash
cd roles/ocp_descheduler
molecule test
```

## 📁 Role Structure

```text
roles/ocp_descheduler/
  README.md
  defaults/
  handlers/
  meta/
  tasks/
  tests/
  vars/
```
