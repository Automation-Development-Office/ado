# Role: infra.ado.ocp_operatorgroups

Ocp Operatorgroups automation role. Primary tasks include: Derive operator namespace and openshift_tools_operator_groups name; Guard — require name_space when not in AllNamespaces mode; Manage openshift_tools_operator_groups with module defaults.

## Role Author

Automation Development Office

## ✅ Role Requirements

- Ansible Core
- Required collections listed in `collections/requirements.yml`
- Inventory or extra variables appropriate for the target platform

## 📦 Role Variables

| Variable | Description |
|----------|-------------|
| `ocp_operatorgroups_state` | Desired state used by role tasks when supported. |

## 🚀 Role Usage

```yaml
- name: Run ocp_operatorgroups
  hosts: localhost
  gather_facts: false
  roles:
    - role: infra.ado.ocp_operatorgroups
```

## 🧪 Role Molecule Testing

Run Molecule scenarios from the role directory when a scenario is available.

This role runs tasks such as:

- Derive operator namespace and openshift_tools_operator_groups name
- Guard — require name_space when not in AllNamespaces mode
- Manage openshift_tools_operator_groups with module defaults
- Check if operator namespace exists (delete guard)

```bash
cd roles/ocp_operatorgroups
molecule test
```

## 📁 Role Structure

```text
roles/ocp_operatorgroups/
  README.md
  defaults/
  handlers/
  meta/
  tasks/
  tests/
  vars/
```
