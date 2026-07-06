# Role: infra.ado.ocp_component_route

Ocp Component Route automation role. Primary tasks include: Validate required framework vars; Resolve component hostname var names; Resolve primary route host from flattened vars.

## Role Author

Automation Development Office

## ✅ Role Requirements

- Ansible Core
- Required collections listed in `collections/requirements.yml`
- Inventory or extra variables appropriate for the target platform

## 📦 Role Variables

| Variable | Description |
|----------|-------------|
| `ocp_component_route_state` | Desired state used by role tasks when supported. |

## 🚀 Role Usage

```yaml
- name: Run ocp_component_route
  hosts: localhost
  gather_facts: false
  roles:
    - role: infra.ado.ocp_component_route
```

## 🧪 Role Molecule Testing

Run Molecule scenarios from the role directory when a scenario is available.

This role runs tasks such as:

- Validate required framework vars
- Resolve component hostname var names
- Resolve primary route host from flattened vars
- Resolve alt route host (only if app_domain_alt is set)

```bash
cd roles/ocp_component_route
molecule test
```

## 📁 Role Structure

```text
roles/ocp_component_route/
  README.md
  defaults/
  handlers/
  meta/
  tasks/
  tests/
  vars/
```
