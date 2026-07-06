# Role: infra.ado.ocp_discover_routes

Ocp Discover Routes automation role. Primary tasks include: Discover Routes | Gather all routes in cluster; Discover Routes | Start empty candidate list; Discover Routes | Append candidates (primary domain, not already -alt).

## Role Author

Automation Development Office

## ✅ Role Requirements

- Ansible Core
- Required collections listed in `collections/requirements.yml`
- Inventory or extra variables appropriate for the target platform

## 📦 Role Variables

| Variable | Description |
|----------|-------------|
| `ocp_discover_routes_primary_suffix` | Role input variable used to configure automation behavior. |
| `ocp_discover_routes_alt_suffix` | Role input variable used to configure automation behavior. |
| `ocp_discover_routes_filter_primary_suffix` | Role input variable used to configure automation behavior. |
| `ocp_discover_routes_exclude_namespaces` | OpenShift namespace value used by this role. |
| `ocp_discover_routes_alt_exclude_name_regex` | Resource name used by this role. |

## 🚀 Role Usage

```yaml
- name: Run ocp_discover_routes
  hosts: localhost
  gather_facts: false
  roles:
    - role: infra.ado.ocp_discover_routes
```

## 🧪 Role Molecule Testing

Run Molecule scenarios from the role directory when a scenario is available.

This role runs tasks such as:

- Discover Routes | Gather all routes in cluster
- Discover Routes | Start empty candidate list
- Discover Routes | Append candidates (primary domain, not already -alt)
- Discover Routes | Print summary

```bash
cd roles/ocp_discover_routes
molecule test
```

## 📁 Role Structure

```text
roles/ocp_discover_routes/
  README.md
  defaults/
  handlers/
  meta/
  tasks/
  tests/
  vars/
```
