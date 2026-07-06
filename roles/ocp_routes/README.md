# Role: infra.ado.ocp_routes

Ocp Routes automation role. Primary tasks include: Get Routes for single namespace; Print all Route hostnames (single namespace); Get Routes for each namespace in routes list.

## Role Author

Automation Development Office

## ✅ Role Requirements

- Ansible Core
- Required collections listed in `collections/requirements.yml`
- Inventory or extra variables appropriate for the target platform

## 📦 Role Variables

| Variable | Description |
|----------|-------------|
| `ocp_routes_state` | Desired state used by role tasks when supported. |

## 🚀 Role Usage

```yaml
- name: Run ocp_routes
  hosts: localhost
  gather_facts: false
  roles:
    - role: infra.ado.ocp_routes
```

## 🧪 Role Molecule Testing

Run Molecule scenarios from the role directory when a scenario is available.

This role runs tasks such as:

- Get Routes for single namespace
- Print all Route hostnames (single namespace)
- Get Routes for each namespace in routes list
- Print all Route hostnames (multiple namespaces)

```bash
cd roles/ocp_routes
molecule test
```

## 📁 Role Structure

```text
roles/ocp_routes/
  README.md
  defaults/
  handlers/
  meta/
  tasks/
  tests/
  vars/
```
