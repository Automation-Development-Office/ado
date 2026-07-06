# Role: infra.ado.rhel_sat_reg

Rhel Sat Reg automation role. Primary tasks include: Gathering facts; Fail if OS version earlier than 8 is detected (Out of Support); Unregister from Satellite via subscription-manager.

## Role Author

Automation Development Office

## ✅ Role Requirements

- Ansible Core
- Required collections listed in `collections/requirements.yml`
- Inventory or extra variables appropriate for the target platform

## 📦 Role Variables

| Variable | Description |
|----------|-------------|
| `rhel_sat_reg_validate_certs` | Validation or TLS verification setting used by this role. |
| `rhel_sat_reg_insights_enabled` | Role input variable used to configure automation behavior. |
| `rhel_sat_reg_update_packages` | Role input variable used to configure automation behavior. |
| `rhel_sat_reg_insecure` | Role input variable used to configure automation behavior. |
| `rhel_sat_reg_action` | Role input variable used to configure automation behavior. |

## 🚀 Role Usage

```yaml
- name: Run rhel_sat_reg
  hosts: localhost
  gather_facts: false
  roles:
    - role: infra.ado.rhel_sat_reg
```

## 🧪 Role Molecule Testing

Run Molecule scenarios from the role directory when a scenario is available.

This role runs tasks such as:

- Gathering facts
- Fail if OS version earlier than 8 is detected (Out of Support)
- Unregister from Satellite via subscription-manager
- Clean local subscription-manager configs

```bash
cd roles/rhel_sat_reg
molecule test
```

## 📁 Role Structure

```text
roles/rhel_sat_reg/
  README.md
  defaults/
  handlers/
  meta/
  tasks/
  tests/
  vars/
```
