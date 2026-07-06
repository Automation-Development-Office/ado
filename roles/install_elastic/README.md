# Role: infra.ado.install_elastic

Install Elastic automation role. Primary tasks include: ECK Set derived vars; ECK Ensure operator namespace exists; ECK Ensure operand namespace exists (only when creating CR).

## Role Author

Automation Development Office

## ✅ Role Requirements

- Ansible Core
- Required collections listed in `collections/requirements.yml`
- Inventory or extra variables appropriate for the target platform

## 📦 Role Variables

| Variable | Description |
|----------|-------------|
| `install_elastic_state` | Desired state used by role tasks when supported. |

## 🚀 Role Usage

```yaml
- name: Run install_elastic
  hosts: localhost
  gather_facts: false
  roles:
    - role: infra.ado.install_elastic
```

## 🧪 Role Molecule Testing

Run Molecule scenarios from the role directory when a scenario is available.

This role runs tasks such as:

- ECK Set derived vars
- ECK Ensure operator namespace exists
- ECK Ensure operand namespace exists (only when creating CR)
- ECK Install operator (openshift_tools_operator_groups + Subscription)

```bash
cd roles/install_elastic
molecule test
```

## 📁 Role Structure

```text
roles/install_elastic/
  README.md
  defaults/
  handlers/
  meta/
  tasks/
  tests/
  vars/
```
